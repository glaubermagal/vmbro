from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import uuid

app = Flask(__name__)
driver = dict()

@app.route('/open-browser')
def open_browser():
    global driver

    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")  # For Linux users
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-local-file-accesses")

    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    
    uid = str(uuid.uuid4())
    driver[uid] = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    driver[uid].get("about:blank")

    return jsonify({
        "uid": uid
    })

@app.route('/close-browser/<path:uid>')
def close_browser(uid):
    global driver
    if uid in driver.keys():
        driver[uid].quit()
        del driver[uid]
    return jsonify({"status": "closed"})

if __name__ == '__main__':
    app.run(debug=True, port=5002)
