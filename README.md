
# AI-Powered Web Vulnerability Scanner

Develop a machine learning-based web vulnerability scanner "Cult Secure" that analyzes traffic, identifies risks, suggests real-time fixes, and generates user-friendly reports to enhance penetration testing speed and accuracy.
## Features

- **Header Analysis**: Analyzes HTTP headers for security misconfigurations.
- **Vulnerability Detection**: Detects CSRF issues, XSS vulnerabilities, and other common web vulnerabilities.
- **Lighthouse Integration**: Runs Google Lighthouse for a complete performance and security report.
- **Scheduled Scans**: Allows automated, scheduled vulnerability scans.
- **Machine Learning-based Classification**: Classifies cybersecurity rules using a pre-trained machine learning model.
- **PDF Report Generation**: Generates PDF reports summarizing scan results.
- **Simulates User Interactions**: Uses Selenium to automate web page interactions.

## Implementation

### Tech Stack

- **Backend Framework**: Flask
- **Web Scraping**: BeautifulSoup, Requests
- **Automated Browser Interaction**: Selenium (with ChromeDriver)
- **Machine Learning**: Scikit-learn, Hugging Face Datasets
- **Scheduling**: Python `schedule` library
- **Logging**: Python `logging` module
- **Performance & Security Audits**: Google Lighthouse
- **Data Handling**: Pandas
- **Model Training**: TfidfVectorizer, LogisticRegression

### Dataset

The machine learning component uses the **Cybersecurity Rules Dataset** from Hugging Face, which contains labeled cybersecurity rules and questions to train the classification model.

**Dataset Link**: [Cybersecurity Rules Dataset](https://huggingface.co/datasets/jcordon5/cybersecurity-rules)

#### Web App Interface
![WhatsApp Image 2024-10-20 at 03 52 26_86e4ad97](https://github.com/user-attachments/assets/e7090f5f-b7af-4306-92d0-4bb4082eaff6)
![WhatsApp Image 2024-10-20 at 03 53 35_fe308981](https://github.com/user-attachments/assets/237fc513-c0fc-4df7-8fab-851ea62acf12)
![WhatsApp Image 2024-10-20 at 03 53 53_a32f224b](https://github.com/user-attachments/assets/9b9aa2fb-dce0-4fb2-b0c5-0cf282bb216a)




