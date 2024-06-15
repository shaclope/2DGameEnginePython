from PyQt5.QtWidgets import QDialog, QLineEdit, QPushButton, QFormLayout
from PyQt5.QtCore import Qt, QRectF  # Assurez-vous que QRectF est importé

class PropertiesDialog(QDialog):
    def __init__(self, item):
        super().__init__()
        self.item = item
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Propriétés de l'objet")
        layout = QFormLayout()

        self.xInput = QLineEdit(str(self.item.pos().x()))
        self.yInput = QLineEdit(str(self.item.pos().y()))
        self.widthInput = QLineEdit(str(self.item.boundingRect().width()))
        self.heightInput = QLineEdit(str(self.item.boundingRect().height()))

        layout.addRow("Position X:", self.xInput)
        layout.addRow("Position Y:", self.yInput)
        layout.addRow("Largeur:", self.widthInput)
        layout.addRow("Hauteur:", self.heightInput)

        applyButton = QPushButton("Appliquer")
        applyButton.clicked.connect(self.applyChanges)
        layout.addWidget(applyButton)

        self.setLayout(layout)

    def applyChanges(self):
        x = float(self.xInput.text())
        y = float(self.yInput.text())
        width = float(self.widthInput.text())
        height = float(self.heightInput.text())

        self.item.setPos(x, y)
        self.item.prepareGeometryChange()
        self.item.rect = QRectF(0, 0, width, height)  # Utilisation de QRectF
        self.item.update()
        self.accept()
