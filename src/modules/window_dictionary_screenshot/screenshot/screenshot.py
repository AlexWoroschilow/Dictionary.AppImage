# -*- coding: utf-8 -*-
# Copyright 2015 Alex Woroschilow (alex.woroschilow@gmail.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt


class Screenshot(QtWidgets.QGraphicsView):
    actionScreenshot = QtCore.pyqtSignal(QtGui.QImage)
    actionClosed = QtCore.pyqtSignal()

    @staticmethod
    def take_screenshot():
        loop = QtCore.QEventLoop()
        shooter = Screenshot()
        shooter.actionClosed.connect(loop.exit)
        shooter.show()
        loop.exec()

        return shooter.image

    def __init__(self, parent=None):
        super().__init__(parent)

        self.selection = QtCore.QRect()
        self.selectionRaw = QtCore.QRect()
        self.font = QtGui.QFont('Verdana', 10)
        self.brush = QtGui.QBrush(Qt.white, Qt.SolidPattern)
        self.pen = QtGui.QPen(Qt.white, 1)

        self.items_to_remove = []
        self.mousePressed = False
        self.pixbuf = None

        position = self.cursor().pos()
        if not position: raise Exception('Position unknown')

        # Init window
        self.pixbuf = self.getscreenshot()
        if not self.pixbuf: raise Exception('Empty screenshot')

        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setContentsMargins(0, 0, 0, 0)
        self.setMouseTracking(True)

        self.setStyleSheet("QGraphicsView { border-style: none; }")

        self.graphics_scene = QtWidgets.QGraphicsScene(0, 0, self.pixbuf.width(), self.pixbuf.height())
        self.setScene(self.graphics_scene)

        self.show()
        self.windowHandle().setScreen(QtGui.QGuiApplication.screenAt(position))
        self.scale = self.get_scale()
        if not self.scale: raise Exception('Empty scale')

        self.setFixedSize(self.pixbuf.width(), self.pixbuf.height())
        self.setGeometry(QtGui.QGuiApplication.screenAt(position).geometry())
        self.showFullScreen()

        QtWidgets.QShortcut(QtGui.QKeySequence('esc'), self).activated.connect(self.close)
        self.actionScreenshot.connect(self.close)

        self.redraw(QtCore.QPoint(position.x(), position.y()))

    def getscreenshot(self):
        screen = QtGui.QGuiApplication.screenAt(QtGui.QCursor.pos())
        if not screen: raise Exception('Empty QScreen')
        return screen.grabWindow(0)

    def mousePressEvent(self, event):
        if event.button() != Qt.LeftButton:
            return super(Screenshot, self).mousePressEvent(event)
        self.mousePressed = True

        self.selection = QtCore.QRect()
        self.selection.setTopLeft(QtCore.QPoint(event.x(), event.y()))
        self.selection.setBottomRight(QtCore.QPoint(event.x(), event.y()))
        self.redraw(QtCore.QPoint(event.x(), event.y()))

        return super(Screenshot, self).mousePressEvent(event)

    def mouseMoveEvent(self, event: QtGui.QMouseEvent):

        if not self.mousePressed:
            return self.redraw(QtCore.QPoint(event.x(), event.y()))

        point = QtCore.QPoint(event.x(), event.y())
        self.selection.setBottomRight(point)

        self.redraw(QtCore.QPoint(event.x(), event.y()))

        return super(Screenshot, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() != Qt.LeftButton:
            return super(Screenshot, self).mouseReleaseEvent(event)
        self.mousePressed = False

        self.selection.setBottomRight(QtCore.QPoint(event.x(), event.y()))
        self.selectionRaw = QtCore.QRect(self.selection)

        self.redraw(QtCore.QPoint(event.x(), event.y()))

        self.saveScreenshot()
        return super(Screenshot, self).mouseReleaseEvent(event)

    def drawMagnifier(self, position=None):
        if not position: return None

        watch_area_width = 16
        watch_area_height = 16

        watch_area = QtCore.QRect(
            QtCore.QPoint(position.x() - watch_area_width / 2, position.y() - watch_area_height / 2),
            QtCore.QPoint(position.x() + watch_area_width / 2, position.y() + watch_area_height / 2))
        if watch_area.left() < 0:
            watch_area.moveLeft(0)
            watch_area.moveRight(watch_area_width)
        if position.x() + watch_area_width / 2 >= self.pixbuf.width():
            watch_area.moveRight(self.pixbuf.width() - 1)
            watch_area.moveLeft(watch_area.right() - watch_area_width)
        if position.y() - watch_area_height / 2 < 0:
            watch_area.moveTop(0)
            watch_area.moveBottom(watch_area_height)
        if position.y() + watch_area_height / 2 >= self.pixbuf.height():
            watch_area.moveBottom(self.pixbuf.height() - 1)
            watch_area.moveTop(watch_area.bottom() - watch_area_height)

        # tricks to solve the hidpi impact on QtGui.QCursor.pos()
        watch_area.setTopLeft(QtCore.QPoint(watch_area.topLeft().x() * self.scale, watch_area.topLeft().y() * self.scale))
        watch_area.setBottomRight(QtCore.QPoint(watch_area.bottomRight().x() * self.scale, watch_area.bottomRight().y() * self.scale))
        watch_area_pixmap = self.pixbuf.copy(watch_area)

        # second, calculate the magnifier area
        magnifier_area_width = watch_area_width * 10
        magnifier_area_height = watch_area_height * 10
        font_area_height = 40

        cursor_size = 24
        magnifier_area = QtCore.QRectF(
            QtCore.QPoint(position.x() + cursor_size, position.y() + cursor_size),
            QtCore.QPoint(position.x() + cursor_size + magnifier_area_width, position.y() + cursor_size + magnifier_area_height))
        if magnifier_area.right() >= self.pixbuf.width():
            magnifier_area.moveLeft(position.x() - magnifier_area_width - cursor_size / 2)
        if magnifier_area.bottom() + font_area_height >= self.pixbuf.height():
            magnifier_area.moveTop(position.y() - magnifier_area_height - cursor_size / 2 - font_area_height)

        # third, draw the watch area to magnifier area
        watch_area_scaled = watch_area_pixmap.scaled(
            QtCore.QSize(magnifier_area_width * self.scale, magnifier_area_height * self.scale))
        magnifier_pixmap = self.graphics_scene.addPixmap(watch_area_scaled)
        magnifier_pixmap.setOffset(magnifier_area.topLeft())

        # then draw lines and text
        self.graphics_scene.addRect(QtCore.QRectF(magnifier_area), QtGui.QPen(QtGui.QColor(0, 0, 0, 100), 2))
        self.graphics_scene.addLine(QtCore.QLineF(QtCore.QPointF(magnifier_area.center().x(), magnifier_area.top()),
                                                  QtCore.QPointF(magnifier_area.center().x(), magnifier_area.bottom())),
                                    QtGui.QPen(QtGui.QColor(0, 0, 0, 100), 2))
        self.graphics_scene.addLine(QtCore.QLineF(QtCore.QPointF(magnifier_area.left(), magnifier_area.center().y()),
                                                  QtCore.QPointF(magnifier_area.right(), magnifier_area.center().y())),
                                    QtGui.QPen(QtGui.QColor(0, 0, 0, 100), 2))

        # get the rgb of mouse point
        point_rgb = QtGui.QColor(self.pixbuf.toImage().pixel(position))

        # draw information
        self.graphics_scene.addRect(
            QtCore.QRectF(magnifier_area.bottomLeft(), magnifier_area.bottomRight() +
                          QtCore.QPoint(0, font_area_height + 30)),
            QtGui.QColor(0, 0, 0, 100),
            QtGui.QBrush(QtGui.QColor(0, 0, 0, 100)))

        text = ' Rgb: ({0}, {1}, {2})'.format(point_rgb.red(), point_rgb.green(), point_rgb.blue())

        rgb_info = self.graphics_scene.addSimpleText(text, self.font)
        rgb_info.setPos(magnifier_area.bottomLeft() + QtCore.QPoint(0, 5))
        rgb_info.setBrush(self.brush)
        rgb_info.setPen(self.pen)

        rect = self.selection.normalized()

        text = ' Size: {0} x {1}'.format(rect.width() * self.scale, rect.height() * self.scale)
        size_info = self.graphics_scene.addSimpleText(text, self.font)
        size_info.setPos(magnifier_area.bottomLeft() + QtCore.QPoint(0, 15) + QtCore.QPoint(0, font_area_height / 2))
        size_info.setBrush(self.brush)
        size_info.setPen(self.pen)

    def get_scale(self):
        return self.devicePixelRatio()

    def saveScreenshot(self):
        fullWindow = QtCore.QRect(0, 0, self.width() - 1, self.height() - 1)
        selected = QtCore.QRect(self.selection)
        if selected.left() < 0:
            selected.setLeft(0)
        if selected.right() >= self.width():
            selected.setRight(self.width() - 1)
        if selected.top() < 0:
            selected.setTop(0)
        if selected.bottom() >= self.height():
            selected.setBottom(self.height() - 1)

        source = (fullWindow & selected)
        source.setTopLeft(QtCore.QPoint(source.topLeft().x() * self.scale, source.topLeft().y() * self.scale))
        source.setBottomRight(
            QtCore.QPoint(source.bottomRight().x() * self.scale, source.bottomRight().y() * self.scale))

        self.image = self.pixbuf.copy(source)
        self.actionScreenshot.emit(QtGui.QImage(self.image))

    def redraw(self, position=None):
        self.graphics_scene.clear()

        # draw screenshot
        self.graphics_scene.addPixmap(self.pixbuf)

        # prepare for drawing selected area
        rect = QtCore.QRectF(self.selection)
        rect = rect.normalized()

        top_left_point = rect.topLeft()
        top_right_point = rect.topRight()
        bottom_left_point = rect.bottomLeft()
        bottom_right_point = rect.bottomRight()
        top_middle_point = (top_left_point + top_right_point) / 2
        left_middle_point = (top_left_point + bottom_left_point) / 2
        bottom_middle_point = (bottom_left_point + bottom_right_point) / 2
        right_middle_point = (top_right_point + bottom_right_point) / 2

        # draw the picture mask
        mask = QtGui.QColor(0, 0, 0, 155)

        if self.selection == QtCore.QRect():
            self.graphics_scene.addRect(0, 0, self.pixbuf.width(), self.pixbuf.height(), QtGui.QPen(Qt.NoPen), mask)
        else:
            self.graphics_scene.addRect(0, 0, self.pixbuf.width(), top_right_point.y(), QtGui.QPen(Qt.NoPen), mask)
            self.graphics_scene.addRect(0, top_left_point.y(), top_left_point.x(), rect.height(), QtGui.QPen(Qt.NoPen),
                                        mask)
            self.graphics_scene.addRect(top_right_point.x(), top_right_point.y(),
                                        self.pixbuf.width() - top_right_point.x(),
                                        rect.height(),
                                        QtGui.QPen(Qt.NoPen),
                                        mask)
            self.graphics_scene.addRect(0, bottom_left_point.y(),
                                        self.pixbuf.width(), self.pixbuf.height() - bottom_left_point.y(),
                                        QtGui.QPen(Qt.NoPen), mask)

        if self.selection != QtCore.QRect():
            self.items_to_remove = []

            # draw the selected rectangle
            pen = QtGui.QPen(QtGui.QColor(0, 255, 0), 2)
            self.items_to_remove.append(self.graphics_scene.addRect(rect, pen))

            # draw the drag point
            radius = QtCore.QPoint(3, 3)
            brush = QtGui.QBrush(QtGui.QColor(0, 255, 0))
            self.items_to_remove.append(
                self.graphics_scene.addEllipse(QtCore.QRectF(top_left_point - radius, top_left_point + radius), pen,
                                               brush))
            self.items_to_remove.append(
                self.graphics_scene.addEllipse(QtCore.QRectF(top_middle_point - radius, top_middle_point + radius), pen,
                                               brush))
            self.items_to_remove.append(
                self.graphics_scene.addEllipse(QtCore.QRectF(top_right_point - radius, top_right_point + radius), pen,
                                               brush))
            self.items_to_remove.append(
                self.graphics_scene.addEllipse(QtCore.QRectF(left_middle_point - radius, left_middle_point + radius),
                                               pen,
                                               brush))
            self.items_to_remove.append(
                self.graphics_scene.addEllipse(QtCore.QRectF(right_middle_point - radius, right_middle_point + radius),
                                               pen,
                                               brush))
            self.items_to_remove.append(
                self.graphics_scene.addEllipse(QtCore.QRectF(bottom_left_point - radius, bottom_left_point + radius),
                                               pen,
                                               brush))
            self.items_to_remove.append(
                self.graphics_scene.addEllipse(
                    QtCore.QRectF(bottom_middle_point - radius, bottom_middle_point + radius), pen,
                    brush))
            self.items_to_remove.append(
                self.graphics_scene.addEllipse(QtCore.QRectF(bottom_right_point - radius, bottom_right_point + radius),
                                               pen,
                                               brush))

        self.drawMagnifier(position)
        if not self.mousePressed: return None
        self.drawSizeInfo(position)

    # draw the size information on the top left corner
    def drawSizeInfo(self, positionGlobal):
        sizeInfoAreaWidth = 200
        sizeInfoAreaHeight = 30
        spacing = 5
        rect = self.selection.normalized()
        sizeInfoArea = QtCore.QRect(rect.left(), rect.top() - spacing - sizeInfoAreaHeight,
                                    sizeInfoAreaWidth, sizeInfoAreaHeight)

        if sizeInfoArea.top() < 0:
            sizeInfoArea.moveTopLeft(rect.topLeft() + QtCore.QPoint(spacing, spacing))
        if sizeInfoArea.right() >= self.pixbuf.width():
            sizeInfoArea.moveTopLeft(rect.topLeft() - QtCore.QPoint(spacing, spacing) - QtCore.QPoint(sizeInfoAreaWidth, 0))
        if sizeInfoArea.left() < spacing: sizeInfoArea.moveLeft(spacing)
        if sizeInfoArea.top() < spacing: sizeInfoArea.moveTop(spacing)

        self.items_to_remove.append(
            self.graphics_scene.addRect(
                QtCore.QRectF(sizeInfoArea),
                QtGui.QColor(0, 0, 0, 100),
                QtGui.QBrush(QtGui.QColor(0, 0, 0, 100))
            )
        )

        text = '  {0} x {1}'.format(rect.width() * self.scale, rect.height() * self.scale)
        sizeInfo = self.graphics_scene.addSimpleText(text, self.font)
        sizeInfo.setPos(sizeInfoArea.topLeft() + QtCore.QPoint(0, 2))
        sizeInfo.setBrush(self.brush)
        sizeInfo.setPen(self.pen)
        self.items_to_remove.append(sizeInfo)

    def close(self):
        self.actionClosed.emit()
        return super().close()
