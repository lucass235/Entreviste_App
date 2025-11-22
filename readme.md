# Sistema de Ponto – PontoFácil

Aplicação desenvolvida para o trabalho final da disciplina, cujo objetivo é
controlar o ponto de funcionários de forma simples, utilizando **Python**, **Streamlit**,
**CSV** para persistência e **Programação Orientada a Objetos (POO)**.

O sistema implementa os casos de uso definidos no diagrama da equipe,
separando claramente os papéis de **Administrador** e **Funcionário**.

---

## ✨ Funcionalidades

### Perfil Administrador

- **Registrar dados do funcionário**
  - Cadastrar funcionário com: matrícula (única), nome, idade e turno
    (Matutino / Vespertino / Noturno).
- **Editar dados do funcionário**
  - Alterar nome, idade e turno de funcionários já cadastrados.
- **Consultar dados do funcionário**
  - Visualizar lista de todos os funcionários.
  - Selecionar um funcionário e visualizar seus dados cadastrais
    + histórico de ponto.
- **Consultar horários de entrada e saída**
  - Listar todos os registros de ponto, com filtros por:
    - Funcionário
    - Intervalo de datas
- **Gerar relatórios**
  - Gráfico de **barras** com funcionários ordenados por idade.
  - Gráfico de **pizza** com distribuição de funcionários por turno.
  - Os gráficos são salvos automaticamente em:
    - `graficos/idade_barras.png`
    - `graficos/turno_pizza.png`

### Perfil Funcionário

- **Registrar horário de chegada**
  - Registra um evento de entrada para a própria matrícula.
- **Registrar horário de saída**
  - Registra um evento de saída, garantindo que exista uma entrada em aberto.
- **Consultar meus dados**
  - Mostra dados cadastrais do funcionário logado e seu histórico de ponto.

### Regras de integridade

- Confirmação de matrícula antes de qualquer operação do funcionário.
- Não permite:
  - registrar ponto para matrícula inexistente;
  - duas entradas seguidas sem saída.
- Os registros são gravados em `data/attendance.csv`.
- Os funcionários são gravados em `data/employees.csv`.

---

## 📁 Estrutura de Pastas

```text
ENTREVISTE_APP/
├── app/
│   ├── config.py             # Caminhos de CSVs e gráficos
│   ├── models/               # Classes de domínio (POO)
│   │   ├── funcionario.py
│   │   ├── registro_ponto.py
│   │   ├── turno.py
│   │   └── usuario.py        # Representa Administrador ou Funcionário
│   ├── repositories/         # Acesso aos arquivos CSV
│   │   ├── employee_csv_repository.py
│   │   └── attendance_csv_repository.py
│   ├── services/
│   │   └── sistema_ponto.py  # Regras de negócio (casos de uso)
│   └── cli/
│       └── interface_terminal.py  # Modo linha de comando (opcional)
├── data/
│   ├── employees.csv         # Funcionários (criado/atualizado pelo sistema)
│   └── attendance.csv        # Registros de ponto (criado/atualizado pelo sistema)
├── graficos/
│   ├── idade_barras.png      # Gráfico gerado automaticamente
│   └── turno_pizza.png       # Gráfico gerado automaticamente
├── main.py                   # Entrada para modo linha de comando (CLI)
├── streamlit_app.py          # Aplicação web (UI com 2 atores)
├── requirements.txt          # Dependências Python
└── README.md                 # Este arquivo
```

Os arquivos `employees.csv` e `attendance.csv` **não precisam existir** antes.
O sistema cria/atualiza eles automaticamente na pasta `data/`.

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
   .venv\Scripts\activate
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

## 🧭 Uso da interface

### 1. Escolher o perfil (ator)

Na **barra lateral** do Streamlit:

- Selecione **Administrador** ou **Funcionário**.

#### Administrador

Não precisa informar matrícula. Escolha uma das opções do menu lateral:

- **Registrar dados do funcionário** – cadastro.
- **Editar dados do funcionário** – alteração.
- **Consultar dados do funcionário** – resumo + histórico.
- **Consultar horários de entrada e saída** – registros com filtros.
- **Gerar relatórios** – gráficos de idade e turno (também geram os PNGs em `graficos/`).

#### Funcionário

1. Informe sua **matrícula** na barra lateral.
2. Escolha no menu:
   - **Registrar horário de chegada**
   - **Registrar horário de saída**
   - **Consultar meus dados**

Se a matrícula não estiver cadastrada, o sistema exibe:
> *“Falha em confirmar matrícula. Verifique a matrícula informada.”*

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

## 🤝 Colaboradores

| ![Ana Cris Silva](https://avatars.githubusercontent.com/u/213529724?v=4&s=96) | ![Lucas Sgotti](https://avatars.githubusercontent.com/u/20289476?v=4&s=96) | ![Filipe Moreno](https://avatars.githubusercontent.com/u/79486720?v=4&s=96) | ![Nivson](https://avatars.githubusercontent.com/u/245549257?v=4&s=96) | ![Lucas dos Santos](https://avatars.githubusercontent.com/u/64389529?v=4&s=96) |
|---|---|---|---|---|
| [**Ana Cris Silva**](https://github.com/anacris34) | [**Lucas Sgotti**](https://github.com/lsgotti) | [**Filipe Moreno**](https://github.com/MoonHawlk) | [**Nivson**](https://github.com/nivson-cesar-school) | [**Lucas dos Santos**](https://github.com/lucass235) |
