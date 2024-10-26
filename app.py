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

    # if driver is None:
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")  # For Linux users
    options.add_argument("--disable-dev-shm-usage")
    
    uid = str(uuid.uuid4())
    driver[uid] = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        
    # Open a specific URL
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
        # driver[uid] = None
    return jsonify({"status": "Browser closed"})

if __name__ == '__main__':
    app.run(debug=True, port=5002)
