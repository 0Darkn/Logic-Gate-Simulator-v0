# 🧠 Logic Gates Simulator in Python (PySide6)

Graphical digital circuit simulator compatible with:

* ✅ Windows 10
* ✅ Ubuntu Linux
* ✅ macOS

Developed using **PySide6 (Qt)**.

Author: Ricardo (adapted by ChatGPT-5)

---

## 📦 Requirements

```bash
pip install PySide6
```

Recommended: **PySide6 ≥ 6.7**

---

## 🚀 How to Run

1. Install dependency:

```bash
pip install PySide6
```

2. Save the file as:

```bash
simulador_portas.py
```

3. Run:

```bash
python simulador_portas.py
```

---

## 🧩 Features

The program creates a Qt window with:

* 🎛️ Panel to add logic gates:

  * AND
  * OR
  * NOT
  * XOR
  * NAND
  * NOR
  * INPUT
  * OUTPUT

* 🖼️ Graphics area (`QGraphicsView`)

  * Draggable gates
  * Selectable items
  * Wire connections

* 🔗 Automatic wiring

* 🔁 Iterative simulation until stable state

* 💾 Save / load projects in JSON

* 📋 Complete menu (File, Simulation, Help)

* 🧠 Detailed step-by-step comments in the code

---

## 🔗 Automatic Connections

1. Click on an **output anchor** (right side).
2. Click on an **input anchor** (left side).
3. A wire is automatically created.

No manual mode switching is required.

---

## ⚙️ INPUT and OUTPUT

### 🔘 INPUT

* Double-click to toggle between:

  * `0`
  * `1`
* Used to provide circuit values.

### 📤 OUTPUT

* Displays the final simulation result.
* Automatically updates after execution.

---

## ▶️ Simulator Interactions

* Click a button (e.g., `AND`) → then click on the scene to place the gate.
* Double-click an `INPUT` to toggle its value.
* Select a gate or wire + press `Delete` to remove.
* Click **Run Simulation** to propagate logic values.
* **Save / Load** to persist the project as JSON.

---

## 🧠 Internal Logic (For Developers)

### 📌 Main Structure

* `GATE_TYPES` → gate type definitions
* `gate_and`, `gate_or`, etc. → logic functions
* `LogicScene` → manages:

  * modes
  * connections
  * simulation (`evaluate()`)
* `GateItem` → each graphical gate
* `Anchor` → connection points
* `WireItem` → wires between gates

---

## ➕ How to Add a New Gate

1. Create the logic function:

```python
def gate_new(a, b):
    return ...
```

2. Add it to `GATE_TYPES`.

Simple and extensible.

---

## 🖥️ Compatibility

✔ Windows 10
✔ Ubuntu Linux
✔ macOS
✔ Python 3.10+

---

## 🎯 Purpose

Educational tool for:

* Learning digital logic
* Testing simple circuits
* Demonstrating visual logic propagation
* Serving as a base for larger projects (robotics, FPGA, digital simulation)

---
