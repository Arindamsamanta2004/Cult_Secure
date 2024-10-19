import os
import requests
from flask import Flask, request, render_template, jsonify, send_from_directory
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from datasets import load_dataset
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pandas as pd
import pdfkit
import schedule
import time
import threading
import logging
from datetime import datetime
import subprocess

app = Flask(__name__)

# Set up logging
logging.basicConfig(filename='vulnerability_scanner.log', level=logging.INFO)

# Load and prepare data
try:
    dataset = load_dataset("jcordon5/cybersecurity-rules")
    df = pd.DataFrame(dataset['train'])
    
    print("Dataset columns:", df.columns)
    print("\nFirst few rows of the dataset:")
    print(df.head())

    # Use the correct column names based on the output
    X = df['instruction']  # This column seems to contain the cybersecurity rules or questions
    y = df['output']  # This column likely contains the categories or responses
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Vectorize and train model
    vectorizer = TfidfVectorizer()
    X_train_tfidf = vectorizer.fit_transform(X_train)
    model = LogisticRegression()
    model.fit(X_train_tfidf, y_train)

    print("Model training completed successfully.")
except Exception as e:
    print(f"Error in loading dataset or training model: {str(e)}")
    raise

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    url = request.form['url']
    
    try:
        # Run Lighthouse analysis and get the report filename
        report_filename = run_lighthouse(url)
        
        if report_filename is None:
            return jsonify({'error': 'Failed to generate Lighthouse report.'}), 500
        
        # Analyze headers
        headers = analyze_headers(url)
        
        # Scan for vulnerabilities
        vulnerabilities = scan_for_vulnerabilities(url) or []  # Ensure this is an array
        
        logging.info(f"Generated report filename: {report_filename}")  # Log the filename
        
        return jsonify({
            'message': "Scanning completed",
            'report': report_filename,
            'vulnerabilities': vulnerabilities  # Ensure this is always an array
        })
    except Exception as e:
        logging.error(f"Error in scan: {str(e)}")
        return jsonify({'error': str(e)}), 500

def run_lighthouse(url):
    try:
        # Generate a unique report filename
        report_filename = f"lighthouse_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        # Run Lighthouse with the --view flag
        os.system(f"lighthouse {url} --output json --output html --output-path ./reports/{report_filename} --view")
        return report_filename  # Return the report filename for further use
    except Exception as e:
        logging.error(f"Error in running Lighthouse: {str(e)}")
        return None

def analyze_headers(url):
    try:
        response = requests.get(url)
        return response.headers
    except Exception as e:
        logging.error(f"Error in analyzing headers: {str(e)}")
        return {}

def scan_for_vulnerabilities(url):
    vulnerabilities = []
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Check for forms without CSRF protection
        forms = soup.find_all('form')
        for form in forms:
            if not form.find('input', {'name': 'csrf_token'}):
                vulnerabilities.append("Form without CSRF protection detected")
        
        # Check for potential XSS vulnerabilities
        scripts = soup.find_all('script')
        for script in scripts:
            if script.string and "document.write" in script.string:
                vulnerabilities.append("Potential XSS vulnerability detected")
        
        # Add more vulnerability checks here
    except Exception as e:
        logging.error(f"Error in scanning for vulnerabilities: {str(e)}")
    
    return vulnerabilities

def simulate_user(url):
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        service = Service('path/to/chromedriver')  # Update this path
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(url)
        # Add interactions here
        driver.quit()
    except Exception as e:
        logging.error(f"Error in simulating user: {str(e)}")

def generate_report(data, filename="vulnerability_report.pdf"):
    try:
        df = pd.DataFrame(data)
        html = df.to_html()
        pdfkit.from_string(html, f"reports/{filename}")  # Ensure the 'reports' directory exists
    except Exception as e:
        logging.error(f"Error in generating report: {str(e)}")

def scheduled_scan(url):
    logging.info(f"Running scheduled scan for {url}")
    vulnerabilities = scan_for_vulnerabilities(url)
    report_data = {
        "URL": [url],
        "Scan Time": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        "Vulnerabilities": [', '.join(vulnerabilities)]
    }
    generate_report(report_data, f"scheduled_scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        rule = request.json.get('rule')
        rule_tfidf = vectorizer.transform([rule])
        prediction = model.predict(rule_tfidf)
        return jsonify({'category': prediction[0]})
    except Exception as e:
        logging.error(f"Error in prediction: {str(e)}")
        return jsonify({'error': str(e)}), 500

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    # Schedule scans (example: scan example.com every day at 2:30 AM)
    schedule.every().day.at("02:30").do(scheduled_scan, "http://example.com")
    
    # Run the scheduling in a separate thread
    schedule_thread = threading.Thread(target=run_schedule)
    schedule_thread.start()
    
    app.run(debug=True)

# Ensure the reports directory exists
if not os.path.exists('reports'):
    os.makedirs('reports')

@app.route('/reports/<path:filename>')
def send_report(filename):
    return send_from_directory('reports', filename)

##easteregg