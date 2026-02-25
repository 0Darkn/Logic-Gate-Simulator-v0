#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QHBoxLayout,
    QLabel, QGraphicsView, QGraphicsScene, QGraphicsItem, QGraphicsEllipseItem,
    QGraphicsLineItem, QFileDialog, QMessageBox, QMenuBar
)
from PySide6.QtGui import QAction, QPen, QBrush
from PySide6.QtCore import Qt, QPointF, QRectF
import sys, json

# =============================================================
#  FUNÇÕES LÓGICAS
# =============================================================

def gate_and(inputs): return int(all(inputs))
def gate_or(inputs): return int(any(inputs))
def gate_not(inputs): return int(not inputs[0])
def gate_xor(inputs): return int(inputs[0] != inputs[1])
def gate_nand(inputs): return int(not all(inputs))
def gate_nor(inputs): return int(not any(inputs))

GATE_TYPES = {
    "AND": gate_and,
    "OR": gate_or,
    "NOT": gate_not,
    "XOR": gate_xor,
    "NAND": gate_nand,
    "NOR": gate_nor,
    "INPUT": lambda _: None,   # valor definido pelo utilizador
    "OUTPUT": lambda x: x[0] if x else 0
}

# =============================================================
#  ÂNCORA (Ponto de ligação)
# =============================================================

class Anchor(QGraphicsEllipseItem):
    """Representa um ponto de ligação (entrada ou saída)."""
    def __init__(self, parent, x_offset, y_offset, is_output=False):
        super().__init__(-5, -5, 10, 10, parent)
        self.setBrush(QBrush(Qt.darkGreen))
        self.is_output = is_output
        self.parent_gate = parent
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.connected_wires = []

    def scenePos(self):
        """Posição absoluta da âncora."""
        p = self.parent_gate.scenePos()
        return QPointF(p.x() + self.x_offset, p.y() + self.y_offset)

# =============================================================
#  PORTA LÓGICA
# =============================================================

class GateItem(QGraphicsItem):
    """Porta lógica com âncoras de entrada e saída."""
    def __init__(self, gate_type="AND"):
        super().__init__()
        self.gate_type = gate_type
        self.width, self.height = 80, 50
        self.value = 0

        # Criar âncoras
        self.inputs = []
        self.output = None

        if gate_type == "NOT":
            self.inputs.append(Anchor(self, -10, 25, False))
            self.output = Anchor(self, 90, 25, True)
        elif gate_type == "INPUT":
            self.output = Anchor(self, 90, 25, True)
        elif gate_type == "OUTPUT":
            self.inputs.append(Anchor(self, -10, 25, False))
        else:
            self.inputs.append(Anchor(self, -10, 15, False))
            self.inputs.append(Anchor(self, -10, 35, False))
            self.output = Anchor(self, 90, 25, True)

        self.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)

    def boundingRect(self):
        return QRectF(0, 0, self.width, self.height)

    def paint(self, painter, option, widget):
        painter.setPen(Qt.black)
        painter.setBrush(Qt.lightGray)
        painter.drawRect(0, 0, self.width, self.height)
        painter.drawText(20, 30, self.gate_type)
        if self.gate_type in ("INPUT", "OUTPUT") or self.value is not None:
            painter.drawText(50, 45, str(self.value))

    def mouseDoubleClickEvent(self, event):
        """Duplo clique no INPUT alterna entre 0 e 1."""
        if self.gate_type == "INPUT":
            self.value = 0 if self.value == 1 else 1
            self.update()
        super().mouseDoubleClickEvent(event)

# =============================================================
#  FIO (Wire)
# =============================================================

class WireItem(QGraphicsLineItem):
    """Liga duas âncoras."""
    def __init__(self, out_anchor, in_anchor):
        super().__init__()
        self.out_anchor = out_anchor
        self.in_anchor = in_anchor
        self.setPen(QPen(Qt.blue, 2))
        self.updatePosition()
        out_anchor.connected_wires.append(self)
        in_anchor.connected_wires.append(self)

    def updatePosition(self):
        start = self.out_anchor.scenePos()
        end = self.in_anchor.scenePos()
        self.setLine(start.x(), start.y(), end.x(), end.y())

# =============================================================
#  CENA PRINCIPAL
# =============================================================

class LogicScene(QGraphicsScene):
    """Cena onde são colocadas portas e fios."""
    def __init__(self):
        super().__init__()
        self.current_gate_type = None
        self.pending_output_anchor = None
        self.wires = []

    def setGateType(self, gate_type):
        self.current_gate_type = gate_type

    def mousePressEvent(self, event):
        item = self.itemAt(event.scenePos(), self.views()[0].transform())

        # Clique numa âncora → gerir ligação automática
        if isinstance(item, Anchor):
            if item.is_output:
                # Selecionou saída (primeiro clique)
                self.pending_output_anchor = item
            elif self.pending_output_anchor:
                # Selecionou entrada (segundo clique)
                self.addWire(self.pending_output_anchor, item)
                self.pending_output_anchor = None
            return

        # Criar nova porta
        if self.current_gate_type:
            gate = GateItem(self.current_gate_type)
            gate.setPos(event.scenePos())
            self.addItem(gate)
            self.current_gate_type = None
        else:
            super().mousePressEvent(event)

    def addWire(self, output_anchor, input_anchor):
        """Cria fio entre saída e entrada."""
        wire = WireItem(output_anchor, input_anchor)
        self.addItem(wire)
        self.wires.append(wire)

    def evaluate(self):
        """Executa simulação lógica completa."""
        gates = [i for i in self.items() if isinstance(i, GateItem)]
        values = {}
        changed = True

        while changed:
            changed = False
            for g in gates:
                if g.gate_type == "INPUT":
                    values[g] = g.value
                else:
                    inputs = []
                    for inp in g.inputs:
                        v = None
                        for w in inp.connected_wires:
                            if w.out_anchor.parent_gate in values:
                                v = values[w.out_anchor.parent_gate]
                        if v is not None:
                            inputs.append(v)
                    if len(inputs) == len(g.inputs):
                        new_val = GATE_TYPES[g.gate_type](inputs)
                        if g not in values or values[g] != new_val:
                            values[g] = new_val
                            changed = True

        # Actualizar valores
        for g, v in values.items():
            g.value = v
            g.update()

# =============================================================
#  JANELA PRINCIPAL
# =============================================================

class LogicSimulator(QMainWindow):
    """Interface principal."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simulador de Portas Lógicas — PySide6")
        self.resize(1000, 700)

        self.scene = LogicScene()
        self.view = QGraphicsView(self.scene)

        # Botões
        layout_btns = QHBoxLayout()
        for gate in GATE_TYPES.keys():
            btn = QPushButton(gate)
            btn.clicked.connect(lambda _, g=gate: self.scene.setGateType(g))
            layout_btns.addWidget(btn)

        btn_run = QPushButton("Executar Simulação")
        btn_run.clicked.connect(self.scene.evaluate)
        layout_btns.addWidget(btn_run)

        layout_main = QVBoxLayout()
        layout_main.addLayout(layout_btns)
        layout_main.addWidget(self.view)

        container = QWidget()
        container.setLayout(layout_main)
        self.setCentralWidget(container)

        self.createMenuBar()

    def createMenuBar(self):
        menubar = QMenuBar(self)
        self.setMenuBar(menubar)

        menu_file = menubar.addMenu("Ficheiro")
        act_save = QAction("Guardar", self)
        act_load = QAction("Carregar", self)
        act_exit = QAction("Sair", self)
        act_save.triggered.connect(self.saveProject)
        act_load.triggered.connect(self.loadProject)
        act_exit.triggered.connect(self.close)
        menu_file.addActions([act_save, act_load, act_exit])

        menu_sim = menubar.addMenu("Simulação")
        act_run = QAction("Executar", self)
        act_run.triggered.connect(self.scene.evaluate)
        menu_sim.addAction(act_run)

        menu_help = menubar.addMenu("Ajuda")
        act_about = QAction("Sobre", self)
        act_about.triggered.connect(self.showAbout)
        menu_help.addAction(act_about)

    def showAbout(self):
        QMessageBox.information(self, "Sobre",
            "Simulador de Portas Lógicas\n"
            "Agora com ligações automáticas e INPUT/OUTPUT fixos\n"
            "Compatível com Windows, Ubuntu e macOS."
        )

    def saveProject(self):
        path, _ = QFileDialog.getSaveFileName(self, "Guardar Projeto", "", "JSON (*.json)")
        if not path: return
        data = []
        for item in self.scene.items():
            if isinstance(item, GateItem):
                data.append({
                    "type": "gate",
                    "gate_type": item.gate_type,
                    "x": item.pos().x(),
                    "y": item.pos().y(),
                    "value": item.value
                })
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
        QMessageBox.information(self, "Guardado", "Projeto guardado com sucesso.")

    def loadProject(self):
        path, _ = QFileDialog.getOpenFileName(self, "Carregar Projeto", "", "JSON (*.json)")
        if not path: return
        self.scene.clear()
        with open(path, "r") as f:
            data = json.load(f)
        for item in data:
            if item["type"] == "gate":
                gate = GateItem(item["gate_type"])
                gate.setPos(item["x"], item["y"])
                gate.value = item.get("value", 0)
                self.scene.addItem(gate)
        QMessageBox.information(self, "Carregado", "Projeto carregado com sucesso.")

# =============================================================
#  ENTRADA PRINCIPAL
# =============================================================

def main():
    app = QApplication(sys.argv)
    window = LogicSimulator()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
