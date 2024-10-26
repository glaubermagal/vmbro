from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)
driver = None

@app.route('/open-browser')
def open_browser():
    global driver
    if driver is None:
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")  # For Linux users
        options.add_argument("--disable-dev-shm-usage")
        
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        
    # Open a specific URL
    driver.get("about://blank")
    page_title = driver.title

    return jsonify({"title": page_title})

@app.route('/close-browser')
def close_browser():
    global driver
    if driver:
        driver.quit()
        driver = None
    return jsonify({"status": "Browser closed"})

if __name__ == '__main__':
    app.run(debug=True, port=5002)
