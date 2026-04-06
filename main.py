import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
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
        self.sandwich_history = []

        self.setWindowTitle("Sandwich Simulator Pro")
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

        # Stacked Widget für die verschiedenen Screens
        self.stacked_widget = QStackedWidget()
        self.layout.addWidget(self.stacked_widget)

        # 0. Hauptmenü
        self.menu_page = QWidget()
        menu_layout = QVBoxLayout(self.menu_page)
        menu_layout.setAlignment(Qt.AlignCenter)
        
        btn_new = QPushButton("🥪 Neues Sandwich erstellen")
        btn_collection = QPushButton("📚 Meine Sandwich-Sammlung")
        btn_settings = QPushButton("⚙️ Einstellungen")
        btn_quit = QPushButton("❌ Beenden")
        
        for btn in [btn_new, btn_collection, btn_settings, btn_quit]:
            btn.setFixedWidth(250)
            btn.setFixedHeight(40)
            menu_layout.addWidget(btn)

        btn_new.clicked.connect(self.start_game)
        btn_collection.clicked.connect(self.show_collection)
        btn_settings.clicked.connect(self.show_settings)
        btn_quit.clicked.connect(self.close)
        
        self.stacked_widget.addWidget(self.menu_page)

        # 1. Auswahl-Screen
        self.selection_page = QWidget()
        self.selection_layout = QVBoxLayout(self.selection_page)
        self.stacked_widget.addWidget(self.selection_page)

        # 2. Ergebnis-Screen
        self.result_page = QWidget()
        self.result_layout = QVBoxLayout(self.result_page)
        self.stacked_widget.addWidget(self.result_page)

        # 3. Einstellungen & 4. Sammlung
        self.settings_page = QWidget()
        self.settings_layout = QVBoxLayout(self.settings_page)
        
        self.collection_page = QWidget()
        self.collection_layout = QVBoxLayout(self.collection_page)

        self.stacked_widget.addWidget(self.settings_page)
        self.stacked_widget.addWidget(self.collection_page)

        self.stacked_widget.setCurrentIndex(0)

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self.clear_layout(child.layout())

    def show_main_menu(self):
        self.stacked_widget.setCurrentIndex(0)

    def start_game(self):
        self.current_step = 0
        self.current_sandwich = []
        self.show_category_selection()

    def show_category_selection(self):
        self.clear_layout(self.selection_layout)

        category = self.categories[self.current_step]
        
        step_label = QLabel(f"Schritt {self.current_step + 1}: {category}")
        step_label.setFont(QFont("Arial", 14, QFont.Bold))
        step_label.setAlignment(Qt.AlignCenter)
        self.selection_layout.addWidget(step_label)

        # Buttons für die Auswahl
        options = self.menu[category]
        for item in options:
            btn = QPushButton(item)
            btn.clicked.connect(lambda checked=False, i=item: self.handle_selection(i))
            self.selection_layout.addWidget(btn)

        # Manuelle Eingabe
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText(f"Oder tippe dein {category} hier...")
        self.input_field.returnPressed.connect(self.handle_input_submission)
        self.selection_layout.addWidget(self.input_field)
        
        self.stacked_widget.setCurrentIndex(1)
        self.input_field.setFocus()

    def handle_selection(self, item):
        self.current_sandwich.append(item)
        self.current_step += 1
        
        if self.current_step < len(self.categories):
            self.show_category_selection()
        else:
            # Sandwich zur Historie hinzufügen
            self.sandwich_history.append(", ".join(self.current_sandwich))
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
            QMessageBox.warning(self, "Ungültige Wahl", f"'{user_input}' steht nicht auf der Liste.")

    def show_finish_screen(self):
        self.clear_layout(self.result_layout)

        finish_label = QLabel("Dein Meisterwerk ist fertig!")
        finish_label.setFont(QFont("Arial", 14, QFont.Bold))
        finish_label.setAlignment(Qt.AlignCenter)
        self.result_layout.addWidget(finish_label)

        summary = "\n".join([f"• {item}" for item in self.current_sandwich])
        summary_label = QLabel(summary)
        summary_label.setAlignment(Qt.AlignCenter)
        self.result_layout.addWidget(summary_label)

        btn_back = QPushButton("Zurück zum Hauptmenü")
        btn_back.clicked.connect(self.show_main_menu)
        self.result_layout.addWidget(btn_back)
        
        self.stacked_widget.setCurrentIndex(2)

    def show_settings(self):
        self.clear_layout(self.settings_layout)
        
        self.settings_layout.addWidget(QLabel("<h2>Einstellungen</h2>"))
        self.settings_layout.addWidget(QLabel("Hier könnten Sound- oder Design-Optionen stehen."))
        
        btn_back = QPushButton("Zurück")
        btn_back.clicked.connect(self.show_main_menu)
        self.settings_layout.addWidget(btn_back)
        
        self.stacked_widget.setCurrentIndex(3)

    def show_collection(self):
        self.clear_layout(self.collection_layout)
        
        self.collection_layout.addWidget(QLabel("<h2>Deine Sandwich-Sammlung</h2>"))
        
        if not self.sandwich_history:
            self.collection_layout.addWidget(QLabel("Du hast noch keine Sandwiches erstellt."))
        else:
            list_widget = QListWidget()
            list_widget.addItems(self.sandwich_history)
            self.collection_layout.addWidget(list_widget)
            
        btn_back = QPushButton("Zurück")
        btn_back.clicked.connect(self.show_main_menu)
        self.collection_layout.addWidget(btn_back)
        
        self.stacked_widget.setCurrentIndex(4)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SandwichSimulator()
    window.show()
    sys.exit(app.exec())