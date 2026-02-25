#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QHBoxLayout,
    QLabel, QGraphicsView, QGraphicsScene, QGraphicsItem,
    QGraphicsEllipseItem, QGraphicsLineItem, QFileDialog,
    QMessageBox, QMenuBar
)
from PySide6.QtGui import QAction, QPen, QColor, QBrush
from PySide6.QtCore import Qt, QPointF
import sys, json

# =============================================================
#  FUNÇÕES LÓGICAS BÁSICAS
# =============================================================

def gate_and(inputs): return int(all(inputs))
def gate_or(inputs): return int(any(inputs))
def gate_not(inputs): return int(not inputs[0])
def gate_xor(inputs): return int(inputs[0] != inputs[1])
def gate_nand(inputs): return int(not all(inputs))
def gate_nor(inputs): return int(not any(inputs))

# Dicionário com os tipos de portas disponíveis
GATE_TYPES = {
    "AND": gate_and,
    "OR": gate_or,
    "NOT": gate_not,
    "XOR": gate_xor,
    "NAND": gate_nand,
    "NOR": gate_nor
}

# =============================================================
#  CLASSE DE ÂNCORAS (PONTOS DE LIGAÇÃO)
# =============================================================

class Anchor(QGraphicsEllipseItem):
    """Pequeno círculo que representa ponto de ligação."""
    def __init__(self, parent, x_offset, y_offset, is_output=False):
        super().__init__(-5, -5, 10, 10, parent)
        self.setBrush(QBrush(Qt.green))
        self.setFlag(QGraphicsItem.ItemSendsScenePositionChanges)
        self.is_output = is_output
        self.parent_gate = parent
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.connected_wires = []

    def scenePos(self):
        """Retorna a posição absoluta da âncora na cena."""
        parent_pos = self.parentItem().scenePos()
        return QPointF(parent_pos.x() + self.x_offset, parent_pos.y() + self.y_offset)

# =============================================================
#  CLASSE DE PORTA LÓGICA
# =============================================================

class GateItem(QGraphicsItem):
    """Representa graficamente uma porta lógica."""
    def __init__(self, gate_type="AND"):
        super().__init__()
        self.gate_type = gate_type
        self.width = 80
        self.height = 50
        self.value = None

        # Criar âncoras (1 ou 2 entradas + 1 saída)
        self.inputs = []
        if gate_type == "NOT":
            self.inputs.append(Anchor(self, -10, 25, is_output=False))
        else:
            self.inputs.append(Anchor(self, -10, 15, is_output=False))
            self.inputs.append(Anchor(self, -10, 35, is_output=False))
        self.output = Anchor(self, 90, 25, is_output=True)

        self.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)

    def boundingRect(self):
        return Qt.QRectF(0, 0, self.width, self.height)

    def paint(self, painter, option, widget):
        painter.setPen(Qt.black)
        painter.setBrush(Qt.lightGray)
        painter.drawRect(0, 0, self.width, self.height)
        painter.drawText(25, 30, self.gate_type)
        # Mostrar valor lógico se já simulado
        if self.value is not None:
            painter.drawText(60, 45, str(self.value))

# =============================================================
#  CLASSE DE FIO
# =============================================================

class WireItem(QGraphicsLineItem):
    """Liga duas âncoras (saída → entrada)."""
    def __init__(self, output_anchor, input_anchor):
        super().__init__()
        self.output_anchor = output_anchor
        self.input_anchor = input_anchor
        pen = QPen(Qt.blue, 2)
        self.setPen(pen)
        self.updatePosition()
        output_anchor.connected_wires.append(self)
        input_anchor.connected_wires.append(self)

    def updatePosition(self):
        """Actualiza a posição do fio quando as portas se movem."""
        start = self.output_anchor.scenePos()
        end = self.input_anchor.scenePos()
        self.setLine(start.x(), start.y(), end.x(), end.y())

# =============================================================
#  CENA LÓGICA (QGraphicsScene)
# =============================================================

class LogicScene(QGraphicsScene):
    """Cena principal onde são colocadas as portas e fios."""
    def __init__(self):
        super().__init__()
        self.current_gate_type = None
        self.pending_output = None
        self.wires = []

    def setGateType(self, gate_type):
        self.current_gate_type = gate_type

    def mousePressEvent(self, event):
        if self.current_gate_type:
            gate = GateItem(self.current_gate_type)
            gate.setPos(event.scenePos())
            self.addItem(gate)
            self.current_gate_type = None
        else:
            super().mousePressEvent(event)

    def addWire(self, output_anchor, input_anchor):
        wire = WireItem(output_anchor, input_anchor)
        self.addItem(wire)
        self.wires.append(wire)

    def evaluate(self):
        """Executa simulação lógica do circuito."""
        # Obter todas as portas
        gates = [item for item in self.items() if isinstance(item, GateItem)]
        values = {}
        changed = True
        while changed:
            changed = False
            for g in gates:
                inputs_values = []
                for inp in g.inputs:
                    v = None
                    for wire in inp.connected_wires:
                        if wire.output_anchor.parent_gate in values:
                            v = values[wire.output_anchor.parent_gate]
                    if v is not None:
                        inputs_values.append(v)
                if len(inputs_values) == len(g.inputs):
                    new_value = GATE_TYPES[g.gate_type](inputs_values)
                    if g not in values or values[g] != new_value:
                        values[g] = new_value
                        changed = True
        # Actualizar visual
        for g, v in values.items():
            g.value = v
            g.update()

# =============================================================
#  JANELA PRINCIPAL
# =============================================================

class LogicSimulator(QMainWindow):
    """Janela principal do simulador."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simulador de Portas Lógicas — PySide6")
        self.resize(900, 600)

        # Cena e vista gráfica
        self.scene = LogicScene()
        self.view = QGraphicsView(self.scene)

        # Botões de controlo
        layout_buttons = QHBoxLayout()
        for gate_name in GATE_TYPES.keys():
            btn = QPushButton(gate_name)
            btn.clicked.connect(lambda _, n=gate_name: self.scene.setGateType(n))
            layout_buttons.addWidget(btn)

        btn_run = QPushButton("Executar Simulação")
        btn_run.clicked.connect(self.scene.evaluate)
        layout_buttons.addWidget(btn_run)

        layout_main = QVBoxLayout()
        layout_main.addLayout(layout_buttons)
        layout_main.addWidget(self.view)

        container = QWidget()
        container.setLayout(layout_main)
        self.setCentralWidget(container)

        # Criar menu
        self.createMenuBar()

    # -------------------------------------------------------------
    def createMenuBar(self):
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)

        # Menu Ficheiro
        menu_file = menu_bar.addMenu("Ficheiro")
        act_save = QAction("Guardar", self)
        act_load = QAction("Carregar", self)
        act_exit = QAction("Sair", self)
        act_save.triggered.connect(self.saveProject)
        act_load.triggered.connect(self.loadProject)
        act_exit.triggered.connect(self.close)
        menu_file.addActions([act_save, act_load, act_exit])

        # Menu Simulação
        menu_sim = menu_bar.addMenu("Simulação")
        act_run = QAction("Executar", self)
        act_run.triggered.connect(self.scene.evaluate)
        menu_sim.addAction(act_run)

        # Menu Ajuda
        menu_help = menu_bar.addMenu("Ajuda")
        act_about = QAction("Sobre", self)
        act_about.triggered.connect(self.showAbout)
        menu_help.addAction(act_about)

    # -------------------------------------------------------------
    def showAbout(self):
        QMessageBox.information(
            self, "Sobre",
            "Simulador de Portas Lógicas\n"
            "Feito em Python + PySide6\n"
            "Compatível com Windows, Ubuntu e macOS."
        )

    # -------------------------------------------------------------
    def saveProject(self):
        path, _ = QFileDialog.getSaveFileName(self, "Guardar Projeto", "", "JSON (*.json)")
        if not path:
            return
        data = []
        for item in self.scene.items():
            if isinstance(item, GateItem):
                data.append({
                    "type": "gate",
                    "gate_type": item.gate_type,
                    "x": item.pos().x(),
                    "y": item.pos().y()
                })
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
        QMessageBox.information(self, "Guardado", "Projeto guardado com sucesso.")

    # -------------------------------------------------------------
    def loadProject(self):
        path, _ = QFileDialog.getOpenFileName(self, "Carregar Projeto", "", "JSON (*.json)")
        if not path:
            return
        self.scene.clear()
        with open(path, "r") as f:
            data = json.load(f)
        for item in data:
            if item["type"] == "gate":
                gate = GateItem(item["gate_type"])
                gate.setPos(item["x"], item["y"])
                self.scene.addItem(gate)
        QMessageBox.information(self, "Carregado", "Projeto carregado com sucesso.")

# =============================================================
#  PONTO DE ENTRADA
# =============================================================

def main():
    app = QApplication(sys.argv)
    window = LogicSimulator()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
