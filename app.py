import os
import time
import threading
from flask import Flask, request, render_template_string, redirect, url_for, flash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-me")

# -----------------------------
# Task registry (in-memory)
# -----------------------------
# tasks = {
#   task_id: {
#       "stop": threading.Event(),
#       "status": "idle/running/stopped/done/error",
#       "log": [str, ...],
#   }
# }
tasks = {}
task_lock = threading.Lock()

# -----------------------------
# HTML (similar layout to the site)
# -----------------------------
HTML = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Nonstop Server — Safe Demo</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body{background:#0b0b11;color:#fff;font-family:system-ui,Segoe UI,Arial,sans-serif;}
    .wrap{max-width:920px;margin:40px auto;padding:24px;border-radius:16px;background:#141421;box-shadow:0 10px 40px rgba(0,0,0,.3)}
    h1{font-weight:800;letter-spacing:.5px;text-align:center;margin-bottom:8px}
    .sub{opacity:.8;text-align:center;margin-bottom:24px}
    .cardx{background:#1b1b2d;border:1px solid #2a2a40;border-radius:16px;padding:16px;margin-bottom:16px}
    .glow{box-shadow:0 0 0 1px #3cf inset, 0 0 24px #3cf22a1f}
    label{font-weight:600}
    .small{font-size:.9rem;opacity:.8}
    .btn-wide{width:100%}
    .pill{border-radius:999px}
    .footer{opacity:.6;text-align:center;margin-top:24px}
    a, a:visited{color:#5cf}
    .badge{background:#222;border:1px solid #444}
    code{background:#111;padding:2px 6px;border-radius:6px}
    .log-box{background:#0f0f18;border:1px solid #24243a;border-radius:12px;padding:12px;max-height:240px;overflow:auto;font-family:ui-monospace, SFMono-Regular, Menlo, monospace;}
  </style>
</head>
<body>
  <div class="wrap">
    <h1>メ Nonstop Server — Safe Demo</h1>
    <div class="sub">Single Token / Token File • Upload TXT messages • Start ➜ Task ID • Stop by Task ID<br>
    <span class="small">⚠️ Demo “sends” only to logs. Don’t use for spam/harassment. Integrate only with compliant APIs.</span></div>

    {% with messages = get_flashed_messages() %}
      {% if messages %}
      <div class="alert alert-warning">{{ messages[0] }}</div>
      {% endif %}
    {% endwith %}

    <form class="cardx glow" action="{{ url_for('run_task') }}" method="post" enctype="multipart/form-data">
      <div class="row g-3">
        <div class="col-md-6">
          <label class="form-label">Select Token Option</label>
          <select name="token_mode" class="form-select">
            <option value="single" selected>Single Token</option>
            <option value="file">Token File (.txt, one per line)</option>
          </select>
        </div>
        <div class="col-md-6">
          <label class="form-label">Hater/Prefix Name (prepended to each line)</label>
          <input name="prefix" class="form-control" placeholder="e.g., Muddassir">
        </div>

        <div class="col-md-6">
          <label class="form-label">Enter Single Token</label>
          <input name="single_token" class="form-control" placeholder="Only if 'Single Token' selected">
        </div>
        <div class="col-md-6">
          <label class="form-label">Choose Token File (.txt)</label>
          <input type="file" name="token_file" accept=".txt" class="form-control">
        </div>

        <div class="col-md-6">
          <label class="form-label">Enter Inbox/Convo UID</label>
          <input name="thread_id" class="form-control" placeholder="t_123456... (demo only)">
        </div>
        <div class="col-md-3">
          <label class="form-label">Time (seconds)</label>
          <input type="number" name="interval" class="form-control" value="3" min="1">
        </div>
        <div class="col-md-3">
          <label class="form-label">Choose Your TXT File (messages)</label>
          <input type="file" name="msg_file" accept=".txt" class="form-control" required>
        </div>

        <div class="col-12">
          <button class="btn btn-success btn-wide pill" type="submit">▶ Run</button>
        </div>
      </div>
      <div class="small mt-2">Note: This demo doesn’t call Facebook. It just logs “would-send” lines. Replace the <code>simulate_send()</code> with compliant API calls if you have opt-in and permissions.</div>
    </form>

    <form class="cardx" action="{{ url_for('stop_task') }}" method="post">
      <div class="row g-3">
        <div class="col-md-9">
          <label class="form-label">Enter Task ID to Stop</label>
          <input name="task_id" class="form-control" placeholder="e.g., TASK-172345...">
        </div>
        <div class="col-md-3">
          <label class="form-label">&nbsp;</label>
          <button class="btn btn-danger btn-wide pill" type="submit">■ Stop</button>
        </div>
      </div>
      <div class="small mt-2">Running tasks & live status are listed below.</div>
    </form>

    <div class="cardx">
      <h5 class="mb-2">Active/Recent Tasks</h5>
      {% if tasks %}
        {% for tid, t in tasks.items() %}
          <div class="mb-3">
            <span class="badge">ID: {{ tid }}</span>
            <span class="badge">Status: {{ t['status'] }}</span>
            <div class="log-box mt-2">
              {% for line in t['log'][-100:] %}
                <div>{{ line }}</div>
              {% endfor %}
            </div>
          </div>
        {% endfor %}
      {% else %}
        <div class="small">No tasks yet.</div>
      {% endif %}
    </div>

    <div class="footer">© 2025 Safe Demo • Build for learning, not spamming.</div>
  </div>
</body>
</html>
"""

# -----------------------------
# Helpers
# -----------------------------
def read_tokens(token_mode, single_token, token_file_storage):
    tokens = []
    if token_mode == "single":
        if single_token:
            tokens = [single_token.strip()]
    elif token_mode == "file" and token_file_storage:
        content = token_file_storage.read().decode("utf-8", errors="ignore")
        tokens = [line.strip() for line in content.splitlines() if line.strip()]
    return tokens

def read_messages(msg_file_storage):
    content = msg_file_storage.read().decode("utf-8", errors="ignore")
    msgs = [line.strip() for line in content.splitlines() if line.strip()]
    return msgs

def simulate_send(token, thread_id, text):
    """
    SAFE DEMO:
    Yahan par koi external API call nahi hoti.
    Sirf return True/False simulate kiya jaata hai.
    TODO: Yahi par aap compliant API (e.g., Facebook Page Send API with opt-in) integrate kar sakte ho.
    """
    time.sleep(0.05)  # tiny delay to mimic network
    # Simulate random success
    return True, "ok"

def worker(task_id, tokens, thread_id, prefix, messages, interval):
    with task_lock:
        t = tasks.get(task_id)
        if not t:
            return
        t["status"] = "running"
        t["log"].append("Task started.")

    try:
        if not tokens:
            with task_lock:
                tasks[task_id]["log"].append("⚠ No tokens provided; using demo-mode only.")
        rounds = 0
        while not tasks[task_id]["stop"].is_set():
            rounds += 1
            for msg in messages:
                if tasks[task_id]["stop"].is_set():
                    break
                for token in (tokens or ["DEMO_TOKEN"]):
                    payload = f"{(prefix or '').strip()} {msg}".strip()
                    ok, info = simulate_send(token, thread_id, payload)
                    with task_lock:
                        if ok:
                            tasks[task_id]["log"].append(f"✅ [round {rounds}] {payload}")
                        else:
                            tasks[task_id]["log"].append(f"❌ [round {rounds}] {payload} :: {info}")
                    # Respect interval between sends
                    for _ in range(interval):
                        if tasks[task_id]["stop"].is_set():
                            break
                        time.sleep(1)
                if tasks[task_id]["stop"].is_set():
                    break
            # For demo, don’t loop forever — stop after 1 full pass
            break

        with task_lock:
            if tasks[task_id]["stop"].is_set():
                tasks[task_id]["status"] = "stopped"
                tasks[task_id]["log"].append("🟥 Task stopped.")
            else:
                tasks[task_id]["status"] = "done"
                tasks[task_id]["log"].append("🟩 Task finished (demo one-pass).")
    except Exception as e:
        with task_lock:
            tasks[task_id]["status"] = "error"
            tasks[task_id]["log"].append(f"💥 Error: {e}")

# -----------------------------
# Routes
# -----------------------------
@app.route("/", methods=["GET"])
def home():
    with task_lock:
        snapshot = {k: {"status": v["status"], "log": list(v["log"])} for k, v in tasks.items()}
    return render_template_string(HTML, tasks=snapshot)

@app.route("/run", methods=["POST"])
def run_task():
    token_mode   = request.form.get("token_mode", "single")
    single_token = request.form.get("single_token", "").strip()
    token_file   = request.files.get("token_file")
    thread_id    = request.form.get("thread_id", "").strip()
    prefix       = request.form.get("prefix", "").strip()
    interval     = int(request.form.get("interval") or 3)
    msg_file     = request.files.get("msg_file")

    if not msg_file:
        flash("Please upload a TXT file with messages.")
        return redirect(url_for("home"))

    tokens = read_tokens(token_mode, single_token, token_file)
    messages = read_messages(msg_file)

    # Create task
    task_id = f"TASK-{int(time.time()*1000)}"
    evt = threading.Event()
    with task_lock:
        tasks[task_id] = {"stop": evt, "status": "idle", "log": []}

    # Start worker
    th = threading.Thread(target=worker, args=(task_id, tokens, thread_id, prefix, messages, interval), daemon=True)
    th.start()

    flash(f"Started! Your Task ID: {task_id}")
    return redirect(url_for("home"))

@app.route("/stop", methods=["POST"])
def stop_task():
    task_id = request.form.get("task_id", "").strip()
    with task_lock:
        t = tasks.get(task_id)
        if not t:
            flash("Task ID not found.")
            return redirect(url_for("home"))
        t["stop"].set()
        t["log"].append("Stop signal received.")
    flash(f"Stop signal sent to {task_id}.")
    return redirect(url_for("home"))

# -----------------------------
# Entry (Render uses $PORT)
# -----------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
