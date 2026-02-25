# simulador em Python (PySide6)
"""
Simulador de Portas Lógicas — compatível com Windows, Ubuntu e macOS
Autor: Ricardo (adaptado por ChatGPT-5)
Requisitos: pip install PySide6

Descrição:
Este simulador permite criar e testar circuitos digitais simples
usando portas lógicas AND, OR, NOT, XOR, NAND e NOR.
Inclui:
 - Menu (Ficheiro, Simulação, Ajuda)
 - Botões para adicionar portas
 - Área gráfica com portas e ligações
 - Simulação com valores lógicos 0/1
 - Guardar e carregar projectos em JSON
"""
* Um programa completo, num único ficheiro, que cria uma janela Qt com:

  * painel para colocar portas (AND, OR, NOT, XOR, NAND, NOR), nós INPUT e OUTPUT;
  * área de desenho (QGraphicsView) com portas arrastáveis e seleccionáveis;
  * ligações por fios (clicar na âncora de saída -> clicar na âncora de entrada);
  * duplo clique em INPUT para alternar 0/1;
  * botão para executar a simulação (propagação iterativa até estabilidade);
  * guardar / carregar projecto em JSON;
  * comentários detalhados passo-a-passo no próprio código explicando cada secção.
Como executar (rápido)

1. Instalar dependência: `pip install PySide6`
2. Guardar o ficheiro (por exemplo `simulador_portas.py`) ou usar o que criei no canvas e correr:
   `python simulador_portas.py`

Principais interacções do jogo/simulador

* Clique num botão (ex.: `AND`) e depois clique na cena para colocar a porta.
* Clique em `Ligar (modo connect)` ou clique directamente numa âncora para começar a ligar.

  * Clique na pequena bolinha de saída (lado direito) e depois na bolinha de entrada (lado esquerdo) da outra porta.
* Duplo clique num `INPUT` para alternar entre 0 e 1.
* Seleccione um fio ou uma porta e pressione `Delete` para apagar.
* `Executar simulação` faz a propagação lógica e actualiza os valores visuais.
* `Guardar...` / `Carregar...` para persistir o projecto.

Notas sobre o código (onde procurar/como estender)

* A lógica das portas está em `GATE_TYPES` e nas funções `gate_and`, `gate_or`, etc. É simples adicionar novos tipos seguindo esse padrão.
* A cena (`LogicScene`) gere os modos, o processo de ligar e a simulação (`evaluate()`).
* Cada porta é um `GateItem` com âncoras (`Anchor`) para facilitar cliques e posicionamento.
* Os fios são `WireItem` que mantêm referências às âncoras origem/destino e actualizam o traço quando as portas se movem.
 ---
 
1. 🔗 **Ligações automáticas:**

   * Clicar numa **âncora de saída** → depois numa **âncora de entrada** cria automaticamente um fio.
   * O utilizador não precisa mudar de modo manual.

2. ⚙️ **Portas fixas `INPUT` e `OUTPUT`:**

   * `INPUT` pode ser duplamente clicado para alternar entre 0 e 1.
   * `OUTPUT` mostra o resultado final após a simulação.

---

### 🧠 **O que foi adicionado**

✅ **Ligações automáticas**

* Clique numa **âncora de saída** e depois numa **âncora de entrada** → cria fio automaticamente.

✅ **INPUT fixos**

* Duplo clique num `INPUT` → alterna entre 0 e 1.
* Usa-se para fornecer valores ao circuito.

✅ **OUTPUT fixos**

* Porta `OUTPUT` mostra o resultado final calculado.

✅ **Simulação lógica completa**

* Propaga valores de `INPUT` até `OUTPUT`.

✅ **Compatível com:**

* **Windows 10**, **Ubuntu Linux**, **macOS**
* **PySide6 ≥ 6.7**
---
✅ **script completo e corrigido** — compatível com **Windows 10, Ubuntu e macOS**, usando **PySide6 (Qt)**.

Ele inclui:

* 🧩 Portas lógicas (AND, OR, NOT, XOR, NAND, NOR)
* ⚙️ Entradas e saídas fixas (INPUT/OUTPUT)
* 🔗 Ligações automáticas (clicar numa saída e depois numa entrada)
* 🖱️ Interface gráfica (arrastar, soltar, clicar)
* 🧠 Atualização automática do estado lógico
* 📋 Menu com opções básicas
* 💬 Comentários e explicações passo a passo em português europeu

---

### 🧠 Dependências:

```bash
pip install PySide6
```

---

### 💡 Como funciona

1. O menu **“Adicionar Porta”** permite criar portas AND, OR, NOT, etc.
2. As **entradas fixas (INPUT)** já estão ligadas a `True` e `False`.
3. As **saídas fixas (OUTPUT)** mostram o resultado final da lógica.
4. Para **ligar automaticamente**:

   * Clica numa **porta de saída**
   * Depois clica numa **porta de entrada**
   * O fio é desenhado automaticamente e o valor é propagado
