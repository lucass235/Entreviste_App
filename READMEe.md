# Sistema de Ponto – Trabalho Final da Disciplina

Aplicação para controle simples de funcionários e registro de ponto,
com interface em **Streamlit**, persistência em **CSV** e organização em **POO**.

---

## ✨ Funcionalidades

- Cadastro de funcionários (matrícula, nome, idade, turno).
- Registro de **entrada** e **saída** de ponto.
- Visualização de dados em tabelas (funcionários e registros).
- Gráfico de **barras** (funcionários ordenados por idade).
- Gráfico de **pizza** (distribuição de funcionários por turno).
- Gráficos são salvos automaticamente em:
  - `graficos/idade_barras.png`
  - `graficos/turno_pizza.png`

---

## 📁 Estrutura de Pastas

```text
ENTREVISTE_APP/
├── app/
│   ├── config.py
│   ├── models/          # Classes de domínio (POO)
│   ├── repositories/    # Acesso aos arquivos CSV
│   ├── services/        # Regra de negócio (SistemaPonto)
│   └── cli/             # Interface de linha de comando (opcional)
├── data/
│   ├── employees.csv    # Funcionários (criado/atualizado pelo sistema)
│   └── attendance.csv   # Registros de ponto (criado/atualizado pelo sistema)
├── graficos/
│   ├── idade_barras.png # Gráfico gerado automaticamente
│   └── turno_pizza.png  # Gráfico gerado automaticamente
├── main.py              # Entrada para modo linha de comando (CLI)
├── streamlit_app.py     # Aplicação web (UI)
├── requirements.txt     # Dependências Python
└── readme.md
```

Os arquivos `employees.csv` e `attendance.csv` **não precisam existir** antes.
O sistema cria/atualiza eles automaticamente.

---

## ✅ Pré-requisitos

- Python **3.10+**
- `pip` instalado
- (Opcional, mas recomendado) ambiente virtual (`venv`)

---

## 🚀 Como rodar a aplicação (Streamlit – UI)

1. **Clonar ou baixar** este repositório na sua máquina.

2. (Opcional) Criar e ativar um ambiente virtual:

   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scriptsctivate
   # Linux/Mac:
   source .venv/bin/activate
   ```

3. **Instalar as dependências**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Rodar a aplicação Streamlit**:

   ```bash
   streamlit run streamlit_app.py
   ```

5. Abrir no navegador o endereço mostrado no terminal  
   (normalmente: `http://localhost:8501`).

---

## 🧭 Uso da interface (Streamlit)

Na barra lateral existem as seções:

- **Cadastrar Funcionário**  
  Preencha matrícula, nome, idade e turno e clique em **Salvar**.

- **Funcionários**  
  Lista todos os funcionários cadastrados (dados vindos de `employees.csv`).

- **Registrar Ponto**  
  Escolha o funcionário e o tipo de registro (**entrada** ou **saída**) e clique em **Registrar**.  
  Os registros são gravados em `attendance.csv`.

- **Registros**  
  Mostra a tabela completa de registros de ponto (com data/hora e tipo).

- **Gráficos**  
  Mostra:
  - Gráfico de barras (idade dos funcionários)  
  - Gráfico de pizza (distribuição por turno)  

  Sempre que essa aba é aberta, os gráficos são **recriados** e salvos em:
  - `graficos/idade_barras.png`
  - `graficos/turno_pizza.png`

Esses PNGs podem ser usados em apresentações e relatório do trabalho.

---

## 💻 Modo Linha de Comando (opcional)

Também é possível usar o sistema pelo terminal:

```bash
python main.py
```

O menu permite:

1. Cadastrar funcionário  
2. Listar funcionários  
3. Registrar entrada  
4. Registrar saída  
5. Gerar/mostrar gráfico de barras (idade)  
6. Gerar/mostrar gráfico de pizza (turno)  
7. Listar registros de ponto  

As mesmas regras de gravação em CSV e geração dos gráficos são utilizadas.

---

## 🧱 Tecnologias utilizadas

- Python
- Pandas
- Matplotlib
- Streamlit
- Programação Orientada a Objetos (POO)
