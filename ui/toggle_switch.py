"""Animated toggle switch."""
__author__ = "Trever Stewart"
__version__ = 1.0

from PyQt6.QtCore import (Qt, QSize, QPoint, QPointF, QRectF, QEasingCurve,
                          QPropertyAnimation, QSequentialAnimationGroup,
                          pyqtSlot, pyqtProperty)
from PyQt6.QtWidgets import QCheckBox, QApplication
from PyQt6.QtGui import QColor, QBrush, QPen, QPaintEvent, QPainter

class QToggleSwitch(QCheckBox):
    _transparent_pen = QPen(Qt.GlobalColor.transparent)
    _light_gray_pen = QPen(Qt.GlobalColor.lightGray)

    def __init__(self, parent=None,
                 text_color="#000000",
                 unchecked_color="#444444",
                 checked_color="#00b0ff",
                 pulse_animation=False):
        super().__init__(parent)

        # Save the color properties and update from the stylesheet
        self._text_color = text_color
        self._unchecked_color = unchecked_color
        self._checked_color = checked_color

        # app = QApplication.instance()
        # app.setStyleSheet(app.styleSheet())

        self.updateBrushes()

        self.setContentsMargins(8, 0, 8, 0)
        self._handle_position = 0

        self._pulse_radius = 0

        self.animation = QPropertyAnimation(self, b"handle_position", self)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.animation.setDuration(200)  # Time in ms

        self.animations_group = QSequentialAnimationGroup()
        self.animations_group.addAnimation(self.animation)

        self._pulse_animation = pulse_animation
        if self._pulse_animation:
            self.pulse_anim = QPropertyAnimation(self, b"pulse_radius", self)
            self.pulse_anim.setDuration(350)  # Time in ms
            self.pulse_anim.setStartValue(20)
            self.pulse_anim.setEndValue(10)
            self.animations_group.addAnimation(self.pulse_anim)

        self.stateChanged.connect(self.setup_animation)

    def updateBrushes(self):
        self._text_pen = QPen(QColor(self._text_color))

        self._bar_brush = QBrush(QColor(self._unchecked_color).lighter())
        self._bar_checked_brush = QBrush(QColor(self._checked_color).lighter())

        self._handle_brush = QBrush(QColor(self._unchecked_color))
        self._handle_checked_brush = QBrush(QColor(self._checked_color))

        pulse_unchecked_color = (self._unchecked_color[:1] +
                                 "44" + self._unchecked_color[1:])
        pulse_checked_color = (self._checked_color[:1] +
                               "44" + self._checked_color[1:])
        self._pulse_unchecked_animation = QBrush(QColor(pulse_unchecked_color))
        self._pulse_checked_animation = QBrush(QColor(pulse_checked_color))

    def sizeHint(self):
        return QSize(58, 45)

    def hitButton(self, pos : QPoint):
        return self.contentsRect().contains(pos)

    @pyqtSlot(int)
    def setup_animation(self, value):
        self.animations_group.stop()
        if value:
            self.animation.setEndValue(1)
        else:
            self.animation.setEndValue(0)
        self.animations_group.start()

    def paintEvent(self, e: QPaintEvent):
        text_width = self.fontMetrics().boundingRect(self.text()).width()

        # Determine the height of the box that holds the toggle switch
        toggle_size = min(self.width(), self.height())

        # Define the bounding rectangle for the toggle switch
        toggle_rect = QRectF(self.rect().left(),
                             self.rect().center().y() - toggle_size / 2,
                             toggle_size + 30,
                             toggle_size)

        # Calculate the radius of the hande base on the toggle box size
        handle_radius = round(0.24 * toggle_rect.height())

        # Define the shape of the bar the handle travels on
        bar_rect = QRectF(toggle_rect.left(),
                          toggle_rect.top(),
                          handle_radius * 3,
                          handle_radius * 2 * 0.7)
        bar_rect.moveCenter(QPointF(toggle_rect.center()))
        bar_rounding = bar_rect.height() / 2

        # Define how far the handle will travel
        trail_length = bar_rect.width()

        # Calculate the X coordinate of the handle
        xPos = bar_rect.x() + trail_length * self._handle_position

        # Initialize the painter object
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing |
                        QPainter.RenderHint.TextAntialiasing)

        p.setPen(self._transparent_pen)

        # Run the pulse animation if enabled
        if (self._pulse_animation and
                self.pulse_anim.state() == QPropertyAnimation.State.Running):
            p.setBrush(self._pulse_checked_animation if self.isChecked() else
                       self._pulse_unchecked_animation)
            p.drawEllipse(QPointF(xPos, bar_rect.center().y()),
                          self._pulse_radius, self._pulse_radius)

        # Draw the bar
        if self.isChecked():
            p.setBrush(self._bar_checked_brush)
            p.drawRoundedRect(bar_rect, bar_rounding, bar_rounding)
            p.setBrush(self._handle_checked_brush)
        else:
            p.setBrush(self._bar_brush)
            p.drawRoundedRect(bar_rect, bar_rounding, bar_rounding)
            p.setPen(self._light_gray_pen)
            p.setBrush(self._handle_brush)

        # Draw the handle
        p.drawEllipse(QPointF(xPos, bar_rect.center().y()),
                      handle_radius, handle_radius)

        # Draw the text
        p.setPen(QPen(QColor(self._text_color)))
        text_rect = QRectF(toggle_rect.right() + 3,
                           self.rect().center().y() - toggle_size / 4,
                           text_width + 10,
                           toggle_size * 0.6)
        p.drawText(text_rect,
                   Qt.AlignmentFlag.AlignLeft |
                   Qt.AlignmentFlag.AlignVCenter, self.text())

        # Make sure the text stays visible
        self.setMinimumWidth(int(toggle_rect.width() + text_rect.width()))

        p.end()

    @pyqtProperty(float)
    def handle_position(self):
        return self._handle_position

    @handle_position.setter
    def handle_position(self, pos):
        self._handle_position = pos
        self.update()

    @pyqtProperty(float)
    def pulse_radius(self):
        return self._pulse_radius

    @pulse_radius.setter
    def pulse_radius(self, radius):
        self._pulse_radius = radius
        self.update()

    @pyqtProperty(str)
    def text_color(self):
        return self._text_color

    @text_color.setter
    def text_color(self, color):
        self._text_color = color
        self.updateBrushes()
        self.update()

    @pyqtProperty(str)
    def unchecked_color(self):
        return self._unchecked_color

    @unchecked_color.setter
    def unchecked_color(self, color):
        self._unchecked_color = color
        self.updateBrushes()
        self.update()

    @pyqtProperty(str)
    def checked_color(self):
        return self._checked_color

    @checked_color.setter
    def checked_color(self, color):
        self._checked_color = color
        self.updateBrushes()
        self.update()


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

    app = QApplication(sys.argv)

    window = QWidget()

    mainToggle = QToggleSwitch(pulse_animation=True,
                               checked_color="#ff6600")
    secondaryToggle = QToggleSwitch(checked_color="#00b0ff",
                                    unchecked_color="#00ff00")

    mainToggle.setFixedSize(mainToggle.sizeHint())
    secondaryToggle.setFixedSize(secondaryToggle.sizeHint())

    window.setLayout(QVBoxLayout())
    window.layout().addWidget(QLabel("Main Toggle"))
    window.layout().addWidget(mainToggle)
    window.layout().addWidget(QLabel("Secondary Toggle"))
    window.layout().addWidget(secondaryToggle)

    mainToggle.stateChanged.connect(secondaryToggle.setChecked)

    window.show()
    sys.exit(app.exec())
