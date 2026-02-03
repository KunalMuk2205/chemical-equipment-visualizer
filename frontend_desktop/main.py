import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, 
                             QPushButton, QFileDialog, QLabel, QTableWidget, QTableWidgetItem)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class DesktopApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chemical Equipment Visualizer (Desktop)")
        self.setGeometry(100, 100, 800, 600)
        self.layout = QVBoxLayout()

        self.label = QLabel("Upload a CSV to start analysis")
        self.layout.addWidget(self.label)

        self.btn = QPushButton("Select CSV File")
        self.btn.clicked.connect(self.upload_file)
        self.layout.addWidget(self.btn)

        # Placeholder for the chart
        self.canvas = None
        
        self.setLayout(self.layout)

    def upload_file(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open file', '', "CSV files (*.csv)")
        if fname:
            files = {'file': open(fname, 'rb')}
            try:
                # Send data to Django
                r = requests.post(
                    'http://127.0.0.1:8000/api/upload/', 
                    files=files, 
                    auth=('Kunal2205', 'Kunal') 
                )
                data = r.json()
                self.display_results(data)
            except Exception as e:
                self.label.setText(f"Error: Make sure Django is running! {e}")

    def display_results(self, data):
        self.label.setText(f"Total: {data['total_count']} | Avg Temp: {data['avg_temp']}°C | Avg Pressure: {data['avg_pressure']}")
        
        # Remove old chart if it exists
        if self.canvas:
            self.layout.removeWidget(self.canvas)

        # Create Matplotlib Chart
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        types = list(data['type_distribution'].keys())
        counts = list(data['type_distribution'].values())
        ax.bar(types, counts, color='skyblue')
        ax.set_title("Equipment Type Distribution")

        self.canvas = FigureCanvas(fig)
        self.layout.addWidget(self.canvas)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DesktopApp()
    ex.show()
    sys.exit(app.exec_())