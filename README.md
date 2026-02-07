# ⚗️ Chem-Analytics Pro: Chemical Equipment Visualizer
### Hybrid Web + Desktop Application with Intelligence Core
This repository contains a Hybrid Full-Stack Application designed for chemical engineers to visualize and analyze equipment parameters. It features a centralized Django REST API that serves both a React.js Web Dashboard and a PyQt5 Desktop Client.

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.0+-green.svg)](https://www.djangoproject.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB.svg)](https://reactjs.org/)

This repository contains a **Hybrid Full-Stack Application** designed for chemical engineers to visualize and analyze equipment parameters. It features a centralized **Django REST API** that serves both a **React.js Web Dashboard** and a **PyQt5 Desktop Client**.

---

## 📖 Table of Contents
* [Architecture](#architecture)
* [Intelligence Engine](#intelligence)
* [Tech Stack](#tech-stack)
* [Key Features](#key-features)
* [Installation & Setup](#installation--setup)
* [Usage](#usage)
* [Author](#author)

---

## 🏗️ Architecture
The project follows a **Client-Server architecture**:
1. **Backend:** Processes CSV data using **Pandas**, calculates statistics, and stores history in **SQLite3**.
2. **Web Client:** Built with **React**, providing a browser-based dashboard with **Chart.js**.
3. **Desktop Client:** Built with **PyQt5**, offering a native experience using **Matplotlib** for graphing.

---
## 🧠 Intelligence Engine

Unlike standard visualizers, this tool includes an Anomaly Detection Engine:

1. **Statistical Analysis:** The backend calculates the Mean and Standard Deviation for all equipment parameters.
2. **Outlier Detection:**  Using the Z-Score method, any equipment with temperature $> (\mu + 2\sigma)$ is flagged as a "Warning."
3. **Alert Sync:** These alerts are highlighted in red on the dashboard and included in the PDF summary report.
   
---
## 🛠️ Tech Stack
| Component | Technologies |
| :--- | :--- |
| **Backend** | Django, Django REST Framework, Pandas, ReportLab |
| **Frontend (Web)** | React.js, Axios, Chart.js |
| **Frontend (Desktop)** | PyQt5, Matplotlib, Requests |
| **Database** | SQLite3 |

---

## ✨ Key Features
- ✅ **CSV Data Processing:** Upload and parse complex equipment datasets.
- ✅ **Real-time Analytics:** Instant calculation of Total Counts, Average Temperature, and Average Pressure.
- ✅ **Dynamic Visualization:** Bar charts showing equipment type distribution.
- ✅ **Persistent History:** Automatically stores the last 5 analysis reports.
- ✅ **Security:** API endpoints secured with **Basic Authentication**.
- ✅ **PDF Export:** Generate downloadable summary reports via ReportLab.

---

## 🚀 Installation & Setup

### 1. Backend Setup
```bash
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install django djangorestframework django-cors-headers pandas reportlab
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
### 2. Web Frontend Setup
```bash
cd frontend_web
npm install
npm start
```
### 3. Desktop Frontend Setup
```bash
cd frontend_desktop
python -m venv .venv
.\.venv\Scripts\activate
pip install PyQt5 matplotlib requests
python main.py
```
### 📊 Usage

1. Ensure the Django server is running at http://127.0.0.1:8000.

2. Use the provided sample_equipment_data.csv for testing.

3. Login using the Superuser credentials created during the setup.

4. Upload the file on either platform to see synchronized data visualization.

### 👤 Author
Kunal Mukherjee
Full Stack Developer Intern Candidate 
Project: FOSSEE Intern Screening Task – Hybrid Web + Desktop Application


### 🛠️ How to apply this fix:
1. Open **VS Code**.
2. Open your `README.md` file.
3. Press **Ctrl + A** to select all, then **Backspace** to delete the old messy text.
4. **Paste** the code block above.
5. Save the file (**Ctrl + S**).
6. In your terminal, run:
   ```powershell
   git add README.md
   git commit -m "Fixed README formatting"
   git push origin main

