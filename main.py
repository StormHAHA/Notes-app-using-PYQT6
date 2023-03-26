import sys

from PyQt6.QtWidgets import QApplication, QPushButton, QLineEdit, QWidget, QGridLayout, QCheckBox, QDialog, QTabWidget,\
    QVBoxLayout, QHBoxLayout, QComboBox
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSettings
from qt_material import apply_stylesheet


class Main(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Notes")
        self.tab_wd = QTabWidget()
        self.tab_wd.addTab(NoteApp(), "Notes")
        self.tab_wd.addTab(Sets(), "Settings")
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tab_wd)
        self.setLayout(self.layout)
        self.setGeometry(0, 0, 900, 1000)
        self.setWindowIcon(QIcon("note.png"))


    def closeEvent(self, event):
        # Save the data for the current active tab (if it's an instance of NoteApp)
        current_tab = self.tab_wd.currentWidget()
        if isinstance(current_tab, NoteApp):
            current_tab.closeEvent(event)


class NoteApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 1000, 1000)
        self.btn = QPushButton("+", self)
        self.vbox = QGridLayout()
        self.setLayout(self.vbox)
        self.vbox.setContentsMargins(100, 100, 100, 100)
        self.btn.clicked.connect(self.button_click)
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.btn)
        self.vbox.addLayout(self.button_layout, 0, 2)
        self.vbox.setRowStretch(100, 10)
        self.btn.setFixedWidth(30)
        self.vbox.setColumnStretch(2, 6)
        self.x = 1              # 0
        self.y = 2             # 1
        self.i_counter = 0
        self.settings = QSettings("Notes", "StormHAHA", self)
        self.setWindowTitle("Notes")
        self.widgets = []

        # Load saved data if available
        saved_data = self.settings.value("data")
        if saved_data:
            # Create QLineEdit and QCheckBox widgets for each saved item
            for item in saved_data:
                text = item["text"]
                checked = item["checked"]
                widget = self.create_widget(text, checked)
                self.widgets.append(widget)

    def create_widget(self, text="", checked=False):
        # Create a QLineEdit, QCheckBox, and QPushButton widget and add them to the grid layout
        text_widget = QLineEdit(text)
        check_widget = QCheckBox()
        check_widget.setChecked(checked)
        button_widget = QPushButton('-')
        button_widget.clicked.connect(lambda: self.delete_row(button_widget))
        self.vbox.addWidget(text_widget, self.x, 0)
        self.vbox.addWidget(check_widget, self.x, 1)
        self.vbox.addWidget(button_widget, self.x, 2)
        self.y += 1
        self.x += 1
        # return the widgets along with the button widget
        return {"text": text, "checked": checked, "text_widget": text_widget, "check_widget": check_widget, "button_widget": button_widget}

    def button_click(self):
        widget = self.create_widget()
        self.widgets.append(widget)

    def delete_row(self, button):
        pos = self.vbox.getItemPosition(self.vbox.indexOf(button))
        # Get the row number
        row = pos[0]
        widget_text = self.vbox.itemAtPosition(row, 0).widget()
        widget_checkbox = self.vbox.itemAtPosition(row, 1).widget()
        widget_button = self.vbox.itemAtPosition(row, 2).widget()
        self.vbox.removeWidget(widget_button)
        self.vbox.removeWidget(widget_text)
        self.vbox.removeWidget(widget_checkbox)
        widget_text.deleteLater()
        widget_checkbox.deleteLater()
        widget_button.deleteLater()
        self.widgets[row - 1] = ""

    def closeEvent(self, event):
        # Save the data for all widgets in the grid layout
        data = []
        for widget in self.widgets:
            if widget == "":
                continue
            data.append({"text": widget["text_widget"].text(), "checked": widget["check_widget"].isChecked()})
        self.settings.setValue("data", data)


class Sets(QWidget):
    def __init__(self):
        super().__init__()
        self.themes_list = QComboBox(self)
        self.vbox = QVBoxLayout(self)
        self.themes_arr = ['dark_amber.xml', 'dark_blue.xml',
         'dark_cyan.xml', 'dark_lightgreen.xml',
         'dark_pink.xml', 'dark_purple.xml',
         'dark_red.xml', 'dark_teal.xml',
         'dark_yellow.xml', 'light_amber.xml',
         'light_blue.xml', 'light_cyan.xml',
         'light_cyan_500.xml', 'light_lightgreen.xml',
         'light_pink.xml', 'light_purple.xml',
         'light_red.xml', 'light_teal.xml',
         'light_yellow.xml']
        for i in self.themes_arr:
            self.themes_list.addItem(i[0:-4].replace("_", " "))
        self.themes_list.currentIndexChanged.connect(self.sets_button)
        self.settings = QSettings("Notes", "Themes", self)
        self.vbox.addWidget(self.themes_list)
        self.apply_theme()

    def apply_theme(self):
        apply_stylesheet(app, theme=self.settings.value("current_theme").replace(" ", "_")+".xml")
        self.themes_list.setCurrentText(self.settings.value("combobox_text"))

    def sets_button(self):
        theme_name = self.themes_list.currentText()
        apply_stylesheet(app, theme=str(theme_name.replace(" ", "_")) + ".xml")
        self.themes_list.setCurrentText(theme_name)

    def changeEvent(self, event):
        self.settings.setValue("current_theme", self.themes_list.currentText())
        self.settings.setValue("combobox_text", self.themes_list.currentText())


app = QApplication(sys.argv)
apply_stylesheet(app, theme="dark_teal.xml")
window = Main()
window.show()
sys.exit(app.exec())