import sys
import requests
import webbrowser
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QFileDialog, QLabel, QFrame, QScrollArea)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QColor
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

class DesktopApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FOSSEE | Chemical Analysis Pro")
        self.setGeometry(100, 100, 1200, 800)
        
        # Modern Stylesheet
        self.setStyleSheet("""
            QWidget { background-color: #0f172a; font-family: 'Segoe UI'; }
            QLabel#Header { color: #3b82f6; font-size: 26px; font-weight: bold; }
            QPushButton { 
                background-color: #3b82f6; color: white; border-radius: 8px; 
                padding: 12px; font-weight: bold; border: none; 
            }
            QPushButton#ExportBtn { background-color: #10b981; }
            QPushButton:hover { opacity: 0.8; }
            QFrame#Card { 
                background-color: #1e293b; border: 1px solid #334155; border-radius: 12px; 
            }
            QLabel#StatValue { color: white; font-size: 22px; font-weight: bold; }
            QLabel#StatTitle { color: #64748b; font-size: 10px; font-weight: bold; text-transform: uppercase; }
        """)

        # Root Layout
        self.main_layout = QHBoxLayout(self)
        
        # --- LEFT PANEL: History & Controls ---
        self.left_panel = QVBoxLayout()
        self.header = QLabel("Analysis Pro")
        self.header.setObjectName("Header")
        self.left_panel.addWidget(self.header)

        self.btn = QPushButton("📁 Load New CSV")
        self.btn.clicked.connect(self.upload_file)
        self.left_panel.addWidget(self.btn)

        self.export_btn = QPushButton("📄 Export PDF Report")
        self.export_btn.setObjectName("ExportBtn")
        self.export_btn.clicked.connect(self.download_pdf)
        self.export_btn.hide() # Hidden until data is loaded
        self.left_panel.addWidget(self.export_btn)

        self.history_label = QLabel("Recent History")
        self.history_label.setStyleSheet("color: white; font-weight: bold; margin-top: 20px;")
        self.left_panel.addWidget(self.history_label)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("border: none; background: transparent;")
        self.history_container = QWidget()
        self.history_list = QVBoxLayout(self.history_container)
        self.history_list.setAlignment(Qt.AlignTop)
        self.scroll.setWidget(self.history_container)
        self.left_panel.addWidget(self.scroll)

        self.main_layout.addLayout(self.left_panel, 1)

        # --- RIGHT PANEL: Dashboard ---
        self.right_panel = QVBoxLayout()
        
        # Stats Row (Units, Temp, Press, System Health)
        self.stats_layout = QHBoxLayout()
        self.total_card = self.create_stat_card("Units", "0")
        self.temp_card = self.create_stat_card("Avg Temp", "0°C")
        self.press_card = self.create_stat_card("Avg Press", "0 bar")
        self.health_card = self.create_stat_card("System Health", "Idle")
        
        self.stats_layout.addWidget(self.total_card)
        self.stats_layout.addWidget(self.temp_card)
        self.stats_layout.addWidget(self.press_card)
        self.stats_layout.addWidget(self.health_card)
        self.right_panel.addLayout(self.stats_layout)

        # Charts Row
        self.charts_layout = QHBoxLayout()
        self.bar_container = QFrame(); self.bar_container.setObjectName("Card")
        self.bar_vbox = QVBoxLayout(self.bar_container)
        self.pie_container = QFrame(); self.pie_container.setObjectName("Card")
        self.pie_vbox = QVBoxLayout(self.pie_container)
        
        self.charts_layout.addWidget(self.bar_container)
        self.charts_layout.addWidget(self.pie_container)
        self.right_panel.addLayout(self.charts_layout, 2)
        
        self.main_layout.addLayout(self.right_panel, 3)
        self.canvases = []

    def create_stat_card(self, title, value):
        card = QFrame(); card.setObjectName("Card")
        lay = QVBoxLayout(card)
        t = QLabel(title); t.setObjectName("StatTitle")
        v = QLabel(value); v.setObjectName("StatValue")
        lay.addWidget(t); lay.addWidget(v)
        return card

    def download_pdf(self):
        webbrowser.open("http://127.0.0.1:8000/api/upload/?export=pdf")

    def upload_file(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open file', '', "CSV files (*.csv)")
        if fname:
            files = {'file': open(fname, 'rb')}
            try:
                r = requests.post('http://127.0.0.1:8000/api/upload/', files=files, auth=('Kunal2205', 'Kunal'))
                data = r.json()
                self.display_results(data, fname.split('/')[-1])
                self.export_btn.show()
            except:
                self.header.setText("Server Offline")

    def display_results(self, data, filename):
        # Update Stats
        self.total_card.findChild(QLabel, "StatValue").setText(str(data['total_count']))
        self.temp_card.findChild(QLabel, "StatValue").setText(f"{data['avg_temp']}°C")
        self.press_card.findChild(QLabel, "StatValue").setText(f"{data['avg_pressure']} bar")
        
        # Health Status & Outlier Logic
        health_label = self.health_card.findChild(QLabel, "StatValue")
        health_label.setText(data['status'])
        
        if data['outlier_alerts'] > 0:
            self.health_card.setStyleSheet("background-color: #450a0a; border: 1px solid #ef4444; border-radius: 12px;")
            health_label.setStyleSheet("color: #ef4444;")
        else:
            self.health_card.setStyleSheet("background-color: #1e293b; border: 1px solid #334155; border-radius: 12px;")
            health_label.setStyleSheet("color: #10b981;")

        # History UI
        h_item = QFrame()
        bg_color = "#450a0a" if data['outlier_alerts'] > 0 else "#334155"
        h_item.setStyleSheet(f"background: {bg_color}; border-radius: 5px; margin-bottom: 5px; padding: 5px;")
        h_lay = QVBoxLayout(h_item)
        h_lay.addWidget(QLabel(f"📄 {filename}", styleSheet="color: white; font-size: 11px;"))
        h_lay.addWidget(QLabel(f"Status: {data['status']}", styleSheet="color: #94a3b8; font-size: 10px;"))
        self.history_list.insertWidget(0, h_item)

        # Refresh Charts
        for c in self.canvases: c.setParent(None)
        self.canvases = []

        plt.style.use('dark_background')
        types, counts = list(data['type_distribution'].keys()), list(data['type_distribution'].values())
        
        # Bar Chart
        fig1 = Figure(facecolor='#1e293b'); ax1 = fig1.add_subplot(111); ax1.set_facecolor('#1e293b')
        ax1.bar(types, counts, color='#3b82f6'); ax1.set_title("Unit Frequency")
        canvas1 = FigureCanvas(fig1); self.bar_vbox.addWidget(canvas1); self.canvases.append(canvas1)

        # Pie Chart
        fig2 = Figure(facecolor='#1e293b'); ax2 = fig2.add_subplot(111)
        ax2.pie(counts, labels=types, autopct='%1.1f%%', colors=['#3b82f6', '#10b981', '#f59e0b', '#ef4444']); ax2.set_title("Composition %")
        canvas2 = FigureCanvas(fig2); self.pie_vbox.addWidget(canvas2); self.canvases.append(canvas2)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DesktopApp(); ex.show()
    sys.exit(app.exec_())