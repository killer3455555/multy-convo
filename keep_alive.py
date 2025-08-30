from flask import Flask, request
import requests
import os
import time

app = Flask(__name__)
app.debug = True

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0 Safari/537.36',
}

@app.route('/', methods=['GET', 'POST'])
def send_message():
    if request.method == 'POST':
        access_tokens = request.form.get('accessTokens').split(",")   # multiple tokens
        thread_ids = request.form.get('threadIds').split(",")         # multiple convo IDs
        prefix = request.form.get('prefix')
        time_interval = int(request.form.get('time'))

        txt_file = request.files['txtFile']
        messages = txt_file.read().decode().splitlines()

        while True:
            try:
                for token in access_tokens:
                    for t_id in thread_ids:
                        for msg in messages:
                            message = f"{prefix} {msg}"
                            api_url = f'https://graph.facebook.com/v15.0/t_{t_id}/'
                            params = {'access_token': token.strip(), 'message': message}
                            response = requests.post(api_url, data=params, headers=headers)

                            if response.status_code == 200:
                                print(f"[✅] Message sent to {t_id} with token {token[:10]}...: {message}")
                            else:
                                print(f"[❌] Failed for {t_id} with token {token[:10]}...: {message}")

                            time.sleep(time_interval)
            except Exception as e:
                print("⚠️ Error:", e)
                time.sleep(10)

    return '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Multi Convo Loader 🚀</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body{
      background: linear-gradient(45deg, #ff0000, #000);
      color: white;
    }
    .container{
      max-width: 400px;
      background-color: #222;
      border-radius: 15px;
      padding: 25px;
      box-shadow: 0 0 15px rgba(0,0,0,0.8);
      margin: 0 auto;
      margin-top: 20px;
    }
    .header{
      text-align: center;
      padding-bottom: 10px;
    }
    .btn-submit{
      width: 100%;
      margin-top: 15px;
      background: #ff3333;
      border: none;
    }
    .footer{
      text-align: center;
      margin-top: 15px;
      color: #bbb;
    }
  </style>
</head>
<body>
  <header class="header mt-4">
    <h1>🔥 Multi Convo Loader 🔥</h1>
    <h3>Made by Muddassir 🤍</h3>
  </header>

  <div class="container">
    <form action="/" method="post" enctype="multipart/form-data">
      <div class="mb-3">
        <label>Enter Tokens (comma separated):</label>
        <input type="text" class="form-control" name="accessTokens" placeholder="token1, token2, token3" required>
      </div>
      <div class="mb-3">
        <label>Enter Convo/Inbox IDs (comma separated):</label>
        <input type="text" class="form-control" name="threadIds" placeholder="id1, id2, id3" required>
      </div>
      <div class="mb-3">
        <label>Enter Prefix/Name:</label>
        <input type="text" class="form-control" name="prefix" required>
      </div>
      <div class="mb-3">
        <label>Upload Notepad File (.txt):</label>
        <input type="file" class="form-control" name="txtFile" accept=".txt" required>
      </div>
      <div class="mb-3">
        <label>Speed in Seconds:</label>
        <input type="number" class="form-control" name="time" required>
      </div>
      <button type="submit" class="btn btn-submit text-white">🚀 Start Loader</button>
    </form>
  </div>

  <footer class="footer">
    <p>&copy; Multi Convo Server by Muddassir 2024</p>
  </footer>
</body>
</html>
    '''

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
