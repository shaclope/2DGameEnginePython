from PyQt5.QtWidgets import QGraphicsItem, QMenu, QColorDialog, QFileDialog
from PyQt5.QtGui import QColor, QBrush, QPen, QPixmap, QPainter
from PyQt5.QtCore import Qt, QRectF, QPointF, QTimer

class CustomImageItem(QGraphicsItem):
    def __init__(self, x, y, width, height, image_path):
        super().__init__()
        self.rect = QRectF(0, 0, width, height)
        self.image_path = image_path
        self.pixmap = QPixmap(image_path)
        self.setPos(x, y)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.attribute = None

         # Variables pour le mouvement de l'ennemi
        self.target = None  # Position cible (par exemple, la position du joueur)
        self.move_speed = 2  # Vitesse de déplacement de l'ennemi
        self.direction = QPointF(0, 0)  # Direction actuelle de déplacement

    def boundingRect(self):
        return self.rect

    def paint(self, painter, option, widget):
        painter.drawPixmap(self.rect.toRect(), self.pixmap, self.pixmap.rect())

    def contextMenuEvent(self, event):
        menu = QMenu()
        changeImageAction = menu.addAction("Changer l'image")
        propertiesAction = menu.addAction("Propriétés")
        deleteAction = menu.addAction("Supprimer")
        setPlatformAction = menu.addAction("Définir comme Plateforme")
        setPlayerAction = menu.addAction("Définir comme Joueur")
        setEnemyAction = menu.addAction("Définir comme Ennemi")
        setRondeAction = menu.addAction("Définir comme Mouvement de Ronde")

        action = menu.exec_(event.screenPos())
        if action == changeImageAction:
            self.changeImage()
        elif action == propertiesAction:
            self.showProperties()
        elif action == deleteAction:
            self.deleteItem()
        elif action == setPlatformAction:
            self.attribute = 'plateforme'
        elif action == setPlayerAction:
            self.attribute = 'joueur'
        elif action == setEnemyAction:
            self.attribute = 'ennemi'
        elif action == setRondeAction:
            self.attribute = 'ronde'
            self.startRonde()

    def changeImage(self):
        image_path, _ = QFileDialog.getOpenFileName(None, "Choisir une image", "", "Images (*.png *.xpm *.jpg)")
        if image_path:
            self.image_path = image_path
            self.pixmap = QPixmap(image_path)
            self.update()

    def showProperties(self):
        dialog = PropertiesDialog(self)
        dialog.exec_()

    def deleteItem(self):
        self.scene().removeItem(self)
        del self

    def startRonde(self):
        self.target_point = QPointF(self.pos().x() + 100, self.pos().y())
        self.original_point = self.pos()
        self.direction = 1
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateRonde)
        self.timer.start(50)

    def updateRonde(self):
        if self.attribute == 'ronde':
            new_x = self.pos().x() + (self.direction * 2)
            if new_x >= self.target_point.x() or new_x <= self.original_point.x():
                self.direction *= -1
            self.setPos(new_x, self.pos().y())

    def keyPressEvent(self, event):
        if self.attribute == 'joueur':
            if event.key() == Qt.Key_Left:
                self.setPos(self.pos().x() - 10, self.pos().y())
            elif event.key() == Qt.Key_Right:
                self.setPos(self.pos().x() + 10, self.pos().y())
            elif event.key() == Qt.Key_Up:
                self.setPos(self.pos().x(), self.pos().y() - 10)
            elif event.key() == Qt.Key_Down:
                self.setPos(self.pos().x(), self.pos().y() + 10)

    def updateEnemyPosition(self, target_position):
        # Mettre à jour la position de l'ennemi en fonction de la position cible (par exemple, joueur)
        if self.attribute == 'ennemi':
            self.target = target_position

    def update(self):
        # Méthode update pour le mouvement de l'ennemi
        if self.attribute == 'ennemi' and self.target:
            # Calculer la direction vers la cible
            direction = self.target - self.pos()
            direction_normalized = direction.normalized()

            # Calculer le déplacement en fonction de la vitesse
            movement = direction_normalized * self.move_speed

            # Mettre à jour la position
            new_position = self.pos() + movement
            self.setPos(new_position)