import sys
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QAction, QMenu, QFileDialog, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QColor, QKeyEvent
from PyQt5.QtCore import Qt, QTimer

from items import CustomImageItem

class GraphicsView(QGraphicsView):
    def __init__(self, scene):
        super().__init__(scene)
        self.keysPressed = []

    def keyPressEvent(self, event):
        if event.key() not in self.keysPressed:
            self.keysPressed.append(event.key())

    def keyReleaseEvent(self, event):
        if event.key() in self.keysPressed:
            self.keysPressed.remove(event.key())

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Éditeur de Scène")

        self.scene = QGraphicsScene()
        self.view = GraphicsView(self.scene)  # Utilisation de GraphicsView au lieu de QGraphicsView
        self.setCentralWidget(self.view)

        self.createActions()
        self.createMenus()

        self.setGeometry(100, 100, 800, 600)

        # Ajout d'un bouton pour lancer la scène
        startButton = QPushButton("Lancer la scène")
        startButton.clicked.connect(self.startScene)

        # Création d'un widget pour contenir le bouton et la vue de la scène
        centralWidget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(startButton)
        layout.addWidget(self.view)
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

        self.player = None
        self.show()

    def createActions(self):
        self.addImageAction = QAction("Ajouter Image", self)
        self.addImageAction.triggered.connect(self.addImage)

        self.saveSceneAction = QAction("Sauvegarder Scène", self)
        self.saveSceneAction.triggered.connect(self.saveScene)

        self.loadSceneAction = QAction("Charger Scène", self)
        self.loadSceneAction.triggered.connect(self.loadScene)

    def createMenus(self):
        self.menuBar().addAction(self.addImageAction)
        self.menuBar().addAction(self.saveSceneAction)
        self.menuBar().addAction(self.loadSceneAction)

    def addImage(self):
        image_path, _ = QFileDialog.getOpenFileName(self, "Choisir une image", "", "Images (*.png *.xpm *.jpg)")
        if image_path:
            image = CustomImageItem(300, 100, 100, 100, image_path)
            self.scene.addItem(image)

    def saveScene(self):
        save_path, _ = QFileDialog.getSaveFileName(self, "Sauvegarder Scène", "", "JSON Files (*.json)")
        if save_path:
            items = []
            for item in self.scene.items():
                if isinstance(item, CustomImageItem):
                    items.append({
                        'type': 'image',
                        'x': item.pos().x(),
                        'y': item.pos().y(),
                        'width': item.boundingRect().width(),
                        'height': item.boundingRect().height(),
                        'image_path': item.image_path,
                        'attribute': item.attribute
                    })
            with open(save_path, 'w') as file:
                json.dump(items, file)

    def loadScene(self):
        load_path, _ = QFileDialog.getOpenFileName(self, "Charger Scène", "", "JSON Files (*.json)")
        if load_path:
            with open(load_path, 'r') as file:
                items = json.load(file)
                self.scene.clear()
                for item_data in items:
                    if item_data['type'] == 'image':
                        image = CustomImageItem(0, 0, item_data['width'], item_data['height'], item_data['image_path'])
                        image.setPos(item_data['x'], item_data['y'])
                        image.attribute = item_data.get('attribute')
                        self.scene.addItem(image)

    def startScene(self):
        self.player = None
        self.enemies = []
        self.platforms = []

        for item in self.scene.items():
            if isinstance(item, CustomImageItem) and item.attribute == 'joueur':
                self.player = item
                break

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateGame)
        self.timer.start(50)

    def updateGame(self):
        self.updatePlayer()
        self.updateEnemies()
        self.checkCollisions()

    def updatePlayer(self):
        if self.player:
            keys_pressed = self.view.keysPressed
            if Qt.Key_Left in keys_pressed:
                self.player.setPos(self.player.pos().x() - 10, self.player.pos().y())
            elif Qt.Key_Right in keys_pressed:
                self.player.setPos(self.player.pos().x() + 10, self.player.pos().y())
            elif Qt.Key_Up in keys_pressed:
                self.player.setPos(self.player.pos().x(), self.player.pos().y() - 10)
            elif Qt.Key_Down in keys_pressed:
                self.player.setPos(self.player.pos().x(), self.player.pos().y() + 10)

    def updateEnemies(self):
        for enemy in self.enemies:
            if self.player:
                enemy.updateEnemyPosition(self.player.pos())

    def checkCollisions(self):
        if self.player:
            for platform in self.platforms:
                if self.player.collidesWithItem(platform):
                    self.player.setPos(self.player.pos().x(), platform.pos().y() - self.player.boundingRect().height())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())
