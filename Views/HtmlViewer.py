from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl
from bs4 import BeautifulSoup
import csv
from pathlib import Path


class HtmlViewer(QWidget):
    def __init__(self, html_file, save_path, div_id, parent=None):
        super().__init__(parent)
        self.html_file = html_file
        self.save_path = Path(save_path)
        self.div_id = div_id
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # WebEngineView to render the HTML
        self.web_view = QWebEngineView(self)
        self.web_view.load(QUrl.fromLocalFile(str(Path(self.html_file).resolve())))
        layout.addWidget(self.web_view)

        # "Done" button to extract the table and navigate to the next page
        self.done_button = QPushButton('Done', self)
        self.done_button.clicked.connect(self.extract_table_and_next)
        layout.addWidget(self.done_button)

        self.setLayout(layout)

    def extract_table_and_next(self):
        # JavaScript to get the innerHTML of the table div
        js_code = f'document.getElementById("{self.div_id}").innerHTML;'

        # Run JavaScript in the QWebEngineView
        self.web_view.page().runJavaScript(js_code, self.handle_table_extraction)

    def handle_table_extraction(self, table_html):
        if table_html:
            # Parse the HTML using BeautifulSoup
            soup = BeautifulSoup(table_html, "html.parser")
            table = soup.find("table")

            if table:
                # Convert the table to a CSV file
                self.save_table_as_csv(table)

        # Navigate to the next page
        self.parent().next_page()

    def save_table_as_csv(self, table):
        # Create the save path if it doesn't exist
        self.save_path.mkdir(parents=True, exist_ok=True)
        save_file = self.save_path / f"{Path(self.html_file).stem}_table.csv"

        # Extract rows and columns from the table
        rows = []
        for tr in table.find_all("tr"):
            row = [td.get_text(strip=True) for td in tr.find_all(["td", "th"])]
            rows.append(row)

        # Save the table as a CSV file
        with open(save_file, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerows(rows)

        print(f"Table data saved to {save_file}")
