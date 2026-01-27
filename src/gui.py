import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
    QTableWidget, QTableWidgetItem, QPushButton, QFileDialog, 
    QMessageBox, QHeaderView, QAbstractItemView
)
from PyQt6.QtCore import Qt

# --- Add build directory to Python path ---
# Get the directory where gui.py is located
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
build_dir = os.path.join(parent_dir, "build")

# Add build directory to Python path to find the compiled module
build_lib_dirs = []
if os.path.exists(build_dir):
    for item in os.listdir(build_dir):
        if item.startswith('lib.'):  # Platform-specific build directory
            build_lib_dirs.append(os.path.join(build_dir, item))

# Try to add each build directory to path
for lib_dir in build_lib_dirs:
    if os.path.exists(lib_dir):
        sys.path.insert(0, lib_dir)
        break

# Also add the build directory itself
sys.path.insert(0, build_dir)

try:
    from datamanager import DataManager
except ImportError as e:
    print(f"Error: Could not import DataManager module. Please build it first.")
    print(f"Build command: cd {parent_dir} && python -m pip install ./src")
    print(f"Or: cd src && python setup.py build_ext --inplace")
    sys.exit(1)

class DataManagerGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DMB DataManager GUI")
        self.resize(800, 600)

        self.dm = DataManager()  # Instance of your backend
        
        # Set up data directory relative to project root
        self.data_dir = os.path.join(parent_dir, "data")
        os.makedirs(self.data_dir, exist_ok=True)  # Create if doesn't exist

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Top buttons
        btn_layout = QHBoxLayout()
        self.load_btn = QPushButton("Load .dmb")
        self.save_btn = QPushButton("Save .dmb")
        self.add_section_btn = QPushButton("Add Section")
        btn_layout.addWidget(self.load_btn)
        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.add_section_btn)
        self.layout.addLayout(btn_layout)

        # Tabs for sections
        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)

        # Connect buttons
        self.load_btn.clicked.connect(self.load_file)
        self.save_btn.clicked.connect(self.save_file)
        self.add_section_btn.clicked.connect(self.add_section)

    # ---------------- LOAD FILE ----------------
    def load_file(self):
        # Set default directory to data folder
        path, _ = QFileDialog.getOpenFileName(
            self, 
            "Open .dmb File", 
            self.data_dir,  # Default to data folder
            "DMB Files (*.dmb)"
        )
        if path:
            if self.dm.load(path):
                self.refresh_tabs()
            else:
                QMessageBox.critical(self, "Error", "Failed to load file!")

    # ---------------- SAVE FILE ----------------
    def save_file(self):
        # Set default directory to data folder
        path, _ = QFileDialog.getSaveFileName(
            self, 
            "Save .dmb File", 
            self.data_dir,  # Default to data folder
            "DMB Files (*.dmb)"
        )
        if path:
            if not path.endswith(".dmb"):
                path += ".dmb"
            if not self.dm.save(path):
                QMessageBox.critical(self, "Error", "Failed to save file!")

    # ---------------- REFRESH TABS ----------------
    def refresh_tabs(self):
        self.tabs.clear()
        for section in self.dm.listSections():
            # Create container widget for table + buttons
            container = QWidget()
            container_layout = QVBoxLayout()
            container.setLayout(container_layout)
            
            # Create table widget
            table = QTableWidget()
            table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
            table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
            
            keys = self.dm.listKeys(section)
            table.setRowCount(len(keys))
            table.setColumnCount(2)
            table.setHorizontalHeaderLabels(["Key", "Value"])
            
            # Make columns stretch
            header = table.horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
            header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
            
            # Fill table with data
            for i, key in enumerate(keys):
                table.setItem(i, 0, QTableWidgetItem(key))
                table.setItem(i, 1, QTableWidgetItem(self.dm.getValue(section, key)))
            
            # Connect cell changes
            table.cellChanged.connect(lambda row, col, sec=section, tbl=table: self.cell_updated(sec, tbl, row, col))
            
            # Create section control buttons
            btn_layout = QHBoxLayout()
            add_row_btn = QPushButton("Add Row")
            delete_row_btn = QPushButton("Delete Selected Row")
            delete_section_btn = QPushButton("Delete Section")
            
            # Connect buttons to functions with stored section name
            add_row_btn.clicked.connect(lambda checked, sec=section, tbl=table: self.add_row(sec, tbl))
            delete_row_btn.clicked.connect(lambda checked, sec=section, tbl=table: self.delete_row(sec, tbl))
            delete_section_btn.clicked.connect(lambda checked, sec=section: self.delete_section(sec))
            
            btn_layout.addWidget(add_row_btn)
            btn_layout.addWidget(delete_row_btn)
            btn_layout.addWidget(delete_section_btn)
            
            # Add table and buttons to container
            container_layout.addWidget(table)
            container_layout.addLayout(btn_layout)
            
            # Store section name in container widget
            container.section_name = section
            
            # Add container as tab
            self.tabs.addTab(container, section)

    # ---------------- HANDLE CELL EDIT ----------------
    def cell_updated(self, section, table, row, col):
        if col == 1:  # Value column
            key_item = table.item(row, 0)
            val_item = table.item(row, 1)
            if key_item and val_item:
                key = key_item.text().strip()
                value = val_item.text()
                if key:  # Only update if key is not empty
                    self.dm.setValue(section, key, value)
                else:
                    QMessageBox.warning(self, "Warning", "Key cannot be empty!")
                    # Refresh to restore original key
                    self.refresh_tabs()

    # ---------------- ADD SECTION ----------------
    def add_section(self):
        section_num = len(self.dm.listSections()) + 1
        new_section = f"Section{section_num}"
        
        # Make sure section name is unique
        while new_section in self.dm.listSections():
            section_num += 1
            new_section = f"Section{section_num}"
        
        self.dm.setValue(new_section, "new_key", "value")
        self.refresh_tabs()

    # ---------------- ADD ROW ----------------
    def add_row(self, section, table):
        # Add new row to table
        row_count = table.rowCount()
        table.insertRow(row_count)
        
        # Set default values
        table.setItem(row_count, 0, QTableWidgetItem("new_key"))
        table.setItem(row_count, 1, QTableWidgetItem("value"))
        
        # Update backend
        self.dm.setValue(section, "new_key", "value")

    # ---------------- DELETE ROW ----------------
    def delete_row(self, section, table):
        selected_rows = table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Warning", "Please select a row to delete!")
            return
        
        # Get confirmation
        reply = QMessageBox.question(
            self, 
            "Confirm Delete", 
            "Are you sure you want to delete the selected row?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Delete from backend first
            for index in selected_rows:
                key_item = table.item(index.row(), 0)
                if key_item:
                    key = key_item.text()
                    self.dm.removeKey(section, key)
            
            # Remove from table
            for index in reversed(selected_rows):
                table.removeRow(index.row())

    # ---------------- DELETE SECTION ----------------
    def delete_section(self, section):
        # Get confirmation
        reply = QMessageBox.question(
            self, 
            "Confirm Delete", 
            f"Are you sure you want to delete section '{section}'? This will remove all its data.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Remove from backend
            self.dm.removeSection(section)
            
            # Refresh tabs
            self.refresh_tabs()

# ---------------- RUN ----------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = DataManagerGUI()
    gui.show()
    sys.exit(app.exec())