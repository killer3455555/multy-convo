from threading import Thread
from flask import Flask
import requests
import time

# yeh tumhara local flask app run karega
def run():
    import app
    app.app.run(host="0.0.0.0", port=5000)

# apna app ko baar baar ping karega taki sleep na ho
def ping():
    while True:
        try:
            requests.get("https://YOUR-APP-NAME.onrender.com/")
        except:
            pass
        time.sleep(60)  # har 1 min baad ping karega

def keep_alive():
    t = Thread(target=run)
    t.start()
    ping()

if __name__ == "__main__":
    keep_alive()
