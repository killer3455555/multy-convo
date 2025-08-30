<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Convo Server — Muddassir</title>

  <!-- Bootstrap CSS -->
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">

  <style>
    body {
      background: linear-gradient(135deg, #0f1724 0%, #001219 100%);
      color: #e6eef8;
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: Inter, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;
    }

    .card {
      width: 420px;
      border-radius: 14px;
      box-shadow: 0 8px 30px rgba(2,6,23,0.6);
      background: linear-gradient(180deg, rgba(255,255,255,0.03), rgba(255,255,255,0.01));
      padding: 18px;
    }

    h1 {
      font-size: 20px;
      margin-bottom: 6px;
      color: #fff;
      letter-spacing: .4px;
    }

    .muted {
      color: #98a4b3;
      font-size: 13px;
    }

    .btn-start {
      background: linear-gradient(90deg,#06b6d4,#3b82f6);
      border: none;
      color: #04283a;
      font-weight: 700;
    }

    .btn-stop {
      background: linear-gradient(90deg,#ff6b6b,#ff3b3b);
      border: none;
      color: #fff;
      font-weight: 700;
    }

    .small-note {
      font-size: 12px;
      color: #9fb0c8;
    }

    .log-area {
      background: rgba(0,0,0,0.35);
      border-radius: 10px;
      padding: 10px;
      height: 110px;
      overflow: auto;
      color: #dfeffb;
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, "Roboto Mono", monospace;
      font-size: 13px;
    }
  </style>
</head>
<body>

  <div class="card">
    <div class="mb-2">
      <h1>⚡ Convo Loader</h1>
      <div class="muted">Enter token(s), convo id(s) and upload your messages file (.txt)</div>
    </div>

    <!-- START / SUBMIT FORM -->
    <form id="startForm" method="post" action="/" enctype="multipart/form-data" class="mb-3">
      <div class="mb-2">
        <label class="form-label small-note">Access Token(s)</label>
        <input name="accessTokens" id="accessTokens" class="form-control form-control-sm" placeholder="token1, token2 (comma separated)" required>
      </div>

      <div class="mb-2">
        <label class="form-label small-note">Convo/Inbox ID(s)</label>
        <input name="threadIds" id="threadIds" class="form-control form-control-sm" placeholder="id1, id2 (comma separated)" required>
      </div>

      <div class="mb-2">
        <label class="form-label small-note">Prefix / Name</label>
        <input name="prefix" id="prefix" class="form-control form-control-sm" placeholder="e.g. Muddassir">
      </div>

      <div class="mb-2">
        <label class="form-label small-note">Messages file (.txt)</label>
        <input type="file" name="txtFile" id="txtFile" accept=".txt" class="form-control form-control-sm" required>
      </div>

      <div class="row gx-2">
        <div class="col-6 mb-2">
          <label class="form-label small-note">Interval (seconds)</label>
          <input type="number" name="time" id="time" class="form-control form-control-sm" value="3" min="1" required>
        </div>
        <div class="col-6 mb-2">
          <label class="form-label small-note">Mode</label>
          <select class="form-select form-select-sm" id="mode" name="mode">
            <option value="multi">Multi Convo (loop tokens × convos)</option>
            <option value="single">Single pass</option>
          </select>
        </div>
      </div>

      <div class="d-grid gap-2 mt-2">
        <button type="submit" class="btn btn-start btn-sm">▶ Start</button>
      </div>
    </form>

    <!-- STOP FORM -->
    <form id="stopForm" method="post" action="/stop" class="mb-3">
      <div class="mb-2">
        <label class="form-label small-note">Stop Task ID (leave empty to stop all demo jobs)</label>
        <input name="task_id" id="task_id" class="form-control form-control-sm" placeholder="TASK-1234567890">
      </div>
      <div class="d-grid gap-2">
        <button type="submit" class="btn btn-stop btn-sm">■ Stop</button>
      </div>
    </form>

    <div class="mt-3 small-note mb-2">Logs (latest):</div>
    <div id="log" class="log-area">No logs yet.</div>

    <div class="mt-3 d-flex justify-content-between">
      <div class="small-note">Made by Muddassir</div>
      <div class="small-note">Local / Render ready</div>
    </div>
  </div>

  <!-- Optional JS: show logs + handle responses nicely -->
  <script>
    const logEl = document.getElementById('log');

    function addLog(text){
      const line = document.createElement('div');
      line.textContent = '[' + new Date().toLocaleTimeString() + '] ' + text;
      logEl.appendChild(line);
      logEl.scrollTop = logEl.scrollHeight;
    }

    // Intercept start form and show preview (then submit)
    document.getElementById('startForm').addEventListener('submit', async function(e){
      // show simple preview and then allow real submit
      addLog('Start request submitted — preparing file upload...');

      // let default form submission happen (no AJAX) so it works with plain Flask
      // if you prefer AJAX, uncomment below and handle fetch to "/" endpoint.
    });

    // Intercept stop form to show confirmation
    document.getElementById('stopForm').addEventListener('submit', function(e){
      addLog('Stop request submitted.');
      // allow normal submission
    });

    // Optional: poll server status endpoint (if you implement /status)
    // setInterval(async ()=>{
    //   try {
    //     const res = await fetch('/status');
    //     if(res.ok){
    //       const data = await res.json();
    //       // update log or status UI
    //     }
    //   } catch(e){
    //     // ignore
    //   }
    // }, 5000);

  </script>

</body>
</html>
