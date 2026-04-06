import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QLabel, QPushButton, QStackedWidget, QHBoxLayout)
                             QLabel, QPushButton, QStackedWidget, QHBoxLayout,
                             QLineEdit, QListWidget, QMessageBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class SandwichSimulator(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Datenmodell
        self.menu = {
            "Brot": ["Vollkorn", "Baguette", "Ciabatta", "Toast"],
            "Protein": ["Hähnchen", "Tofu", "Salami", "Schinken", "Kein Protein"],
            "Gemüse": ["Salat", "Tomaten", "Gurken", "Zwiebeln", "Paprika"],
            "Saucen": ["Mayonnaise", "Senf", "Scharfe Sauce", "Hausdressing"]
        }
        self.categories = list(self.menu.keys())
        self.current_step = 0
        self.current_sandwich = []

        self.setWindowTitle("Sandwich-Maker 2024")
        self.setMinimumSize(400, 500)
        self.init_ui()

    def init_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Titel
        self.title_label = QLabel("🥪 Sandwich Simulator")
        self.title_label.setFont(QFont("Arial", 18, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title_label)

        # Stacked Widget für die Phasen (Start -> Auswahl -> Ergebnis)
        self.stacked_widget = QStackedWidget()
        self.layout.addWidget(self.stacked_widget)

        # 1. Start-Screen
        self.start_page = QWidget()
        start_layout = QVBoxLayout(self.start_page)
        start_btn = QPushButton("Neues Sandwich erstellen")
        start_btn.clicked.connect(self.start_game)
        start_layout.addWidget(start_btn, 0, Qt.AlignCenter)
        self.stacked_widget.addWidget(self.start_page)

        # 2. Auswahl-Screen (wird dynamisch befüllt)
        self.selection_page = QWidget()
        self.selection_layout = QVBoxLayout(self.selection_page)
        
        # Wir bereiten den Eingabebereich vor, damit wir ihn später leichter ansprechen können
        self.input_field = QLineEdit()
        self.input_field.returnPressed.connect(self.handle_input_submission)
        self.stacked_widget.addWidget(self.selection_page)

        # 3. Ergebnis-Screen
        self.result_page = QWidget()
        self.result_layout = QVBoxLayout(self.result_page)
        self.stacked_widget.addWidget(self.result_page)

        self.stacked_widget.setCurrentIndex(0)

    def start_game(self):
        self.current_step = 0
        self.current_sandwich = []
        self.show_category_selection()

    def show_category_selection(self):
        # Layout leeren
        for i in reversed(range(self.selection_layout.count())): 
            self.selection_layout.itemAt(i).widget().setParent(None)

        category = self.categories[self.current_step]
        label = QLabel(f"Wähle dein {category}:")
        label.setFont(QFont("Arial", 12))
        label.setAlignment(Qt.AlignCenter)
        self.selection_layout.addWidget(label)
        
        # Haupt-Titel für den Schritt
        step_label = QLabel(f"Schritt {self.current_step + 1}: {category}")
        step_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.selection_layout.addWidget(step_label)

        # Horizontales Layout für Sidebar + Eingabe
        content_layout = QHBoxLayout()
        
        # Linke Seite: Liste der Möglichkeiten
        sidebar_layout = QVBoxLayout()
        sidebar_layout.addWidget(QLabel("Verfügbare Optionen:"))
        self.options_list = QListWidget()
        options = self.menu[category]
        for item in options:
            btn = QPushButton(item)
            btn.clicked.connect(lambda checked=False, i=item: self.handle_selection(i))
            self.selection_layout.addWidget(btn)
        self.options_list.addItems(options)
        self.options_list.setFixedWidth(150)
        sidebar_layout.addWidget(self.options_list)
        content_layout.addLayout(sidebar_layout)

        # Rechte Seite: Eingabe
        interaction_layout = QVBoxLayout()
        interaction_layout.setAlignment(Qt.AlignTop)
        
        category = self.categories[self.current_step]
        interaction_layout.addWidget(QLabel(f"Was für ein(e) {category} möchtest du?"))
        
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Hier tippen...")
        self.input_field.returnPressed.connect(self.handle_input_submission)
        interaction_layout.addWidget(self.input_field)

        submit_btn = QPushButton("Hinzufügen")
        submit_btn.clicked.connect(self.handle_input_submission)
        interaction_layout.addWidget(submit_btn)
        
        content_layout.addLayout(interaction_layout)
        self.selection_layout.addLayout(content_layout)

        self.stacked_widget.setCurrentIndex(1)
        self.input_field.setFocus()

    def handle_selection(self, item):
        self.current_sandwich.append(item)
        self.current_step += 1
        
        if self.current_step < len(self.categories):
            self.show_category_selection()
        else:
            self.show_finish_screen()

    def handle_input_submission(self):
        user_input = self.input_field.text().strip()
        category = self.categories[self.current_step]
        valid_options = self.menu[category]

        # Prüfung, ob die Eingabe in den Optionen existiert (Ignoriert Groß-/Kleinschreibung)
        match = next((opt for opt in valid_options if opt.lower() == user_input.lower()), None)

        if match:
            self.handle_selection(match)
        else:
            QMessageBox.warning(self, "Ungültige Wahl", f"'{user_input}' steht nicht auf der Liste. Bitte wähle etwas aus der Sidebar.")

    def show_finish_screen(self):
        for i in reversed(range(self.result_layout.count())): 
            self.result_layout.itemAt(i).widget().setParent(None)

        finish_label = QLabel("Dein Meisterwerk ist fertig!")
        finish_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.result_layout.addWidget(finish_label)

        summary = "\n".join([f"• {item}" for item in self.current_sandwich])
        self.result_layout.addWidget(QLabel(summary))

        restart_btn = QPushButton("Noch eins machen!")
        restart_btn.clicked.connect(self.start_game)
        self.result_layout.addWidget(restart_btn)
        
        self.stacked_widget.setCurrentIndex(2)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SandwichSimulator()
    window.show()
    sys.exit(app.exec())