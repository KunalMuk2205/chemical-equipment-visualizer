⚗️ Chemical Equipment Parameter VisualizerHybrid Web + Desktop ApplicationThis repository contains a Hybrid Full-Stack Application designed for chemical engineers to visualize and analyze equipment parameters. It features a centralized Django REST API that serves both a React.js Web Dashboard and a PyQt5 Desktop Client.📖 Table of ContentsArchitectureTech StackKey FeaturesInstallation & SetupUsageContact🏗️ ArchitectureThe project follows a Client-Server architecture where:Backend: Processes CSV data using Pandas, calculates statistics, and stores history in SQLite3.Web Client: Built with React, provides a modern browser-based dashboard with Chart.js.Desktop Client: Built with PyQt5, offers a native Windows experience using Matplotlib for graphing.🛠️ Tech StackComponentTechnologiesBackendDjango, Django REST Framework, Pandas, ReportLabFrontend (Web)React.js, Axios, Chart.jsFrontend (Desktop)PyQt5, Matplotlib, RequestsDatabaseSQLite3✨ Key Features✅ CSV Data Processing: Upload and parse complex equipment datasets.✅ Real-time Analytics: Instant calculation of Total Counts, Average Temperature, and Average Pressure.✅ Dynamic Visualization: Bar charts showing equipment type distribution.✅ Persistent History: Automatically stores the last 5 analysis reports.✅ Security: API endpoints secured with Basic Authentication.✅ PDF Export: Generate downloadable summary reports.🚀 Installation & Setup1. Backend SetupBashcd backend
python -m venv venv
.\venv\Scripts\activate
pip install django djangorestframework django-cors-headers pandas reportlab
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser  # Set your API credentials
python manage.py runserver
2. Web Frontend SetupBashcd frontend_web
npm install
npm start
3. Desktop Frontend SetupBashcd frontend_desktop
python -m venv .venv
.\.venv\Scripts\activate
pip install PyQt5 matplotlib requests
python main.py
📊 UsageEnsure the Django server is running at http://127.0.0.1:8000.Use the provided sample_equipment_data.csv for testing.Login using the credentials created during the createsuperuser step.Upload the file on either platform to see the synchronized data visualization.👤 AuthorKunal MukherjeeRole: Full Stack Developer Intern CandidateProject: FOSSEE Screening TaskFinal Check for Kunal: