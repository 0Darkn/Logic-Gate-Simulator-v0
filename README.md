# 🧠 Simulador de Portas Lógicas em Python (PySide6)

Simulador gráfico de circuitos digitais compatível com:

* ✅ Windows 10
* ✅ Ubuntu Linux
* ✅ macOS

Desenvolvido com **PySide6 (Qt)**.

Autor: Ricardo (adaptado por ChatGPT-5)

---

## 📦 Requisitos

```bash
pip install PySide6
```

Recomendado: **PySide6 ≥ 6.7**

---

## 🚀 Como Executar

1. Instalar dependência:

```bash
pip install PySide6
```

2. Guardar o ficheiro como:

```bash
simulador_portas.py
```

3. Executar:

```bash
python simulador_portas.py
```

---

## 🧩 Funcionalidades

O programa cria uma janela Qt com:

* 🎛️ Painel para adicionar portas:

  * AND
  * OR
  * NOT
  * XOR
  * NAND
  * NOR
  * INPUT
  * OUTPUT

* 🖼️ Área gráfica (`QGraphicsView`)

  * Portas arrastáveis
  * Selecionáveis
  * Conectáveis por fios

* 🔗 Ligações automáticas

* 🔁 Simulação iterativa até estabilidade

* 💾 Guardar / carregar projetos em JSON

* 📋 Menu completo (Ficheiro, Simulação, Ajuda)

* 🧠 Comentários detalhados no código

---

## 🔗 Ligações Automáticas

1. Clique numa **âncora de saída** (lado direito).
2. Clique numa **âncora de entrada** (lado esquerdo).
3. O fio é criado automaticamente.

Não é necessário mudar manualmente de modo.

---

## ⚙️ INPUT e OUTPUT

### 🔘 INPUT

* Duplo clique alterna entre:

  * `0`
  * `1`
* Usado para fornecer valores ao circuito.

### 📤 OUTPUT

* Mostra o resultado final da simulação.
* Atualiza automaticamente após execução.

---

## ▶️ Interações do Simulador

* Clique num botão (ex: `AND`) → clique na cena para colocar a porta.
* Duplo clique num `INPUT` para alternar valor.
* Selecionar porta ou fio + `Delete` para apagar.
* Botão **Executar Simulação** propaga os valores.
* **Guardar / Carregar** para persistir projeto em JSON.

---

## 🧠 Lógica Interna (Para Desenvolvedores)

### 📌 Estrutura principal

* `GATE_TYPES` → definição dos tipos de portas
* `gate_and`, `gate_or`, etc. → funções lógicas
* `LogicScene` → gere:

  * modos
  * ligações
  * simulação (`evaluate()`)
* `GateItem` → cada porta gráfica
* `Anchor` → pontos de ligação
* `WireItem` → fios entre portas

---

## ➕ Como Adicionar Nova Porta

1. Criar função lógica:

```python
def gate_nova(a, b):
    return ...
```

2. Adicionar em `GATE_TYPES`.

Simples e extensível.

---

## 🖥️ Compatibilidade

✔ Windows 10
✔ Ubuntu Linux
✔ macOS
✔ Python 3.10+

---

## 🎯 Objetivo

Ferramenta educativa para:

* Aprender lógica digital
* Testar circuitos simples
* Demonstrar propagação lógica visualmente
* Servir como base para projetos maiores (robótica, FPGA, simulação digital)

---
