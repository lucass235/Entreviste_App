# A — Ficha de Requisitos

## 1. Requisitos Funcionais (RF)

### **RF1 — Cadastrar funcionário**
- O sistema deve permitir cadastrar um funcionário com os campos: matrícula (única), nome, idade e turno (matutino / vespertino / noturno).
- Deve validar duplicidade de matrícula.

### **RF2 — Registrar ponto (entrada/saída)**
- O sistema deve permitir registrar diariamente horários de entrada e saída para cada funcionário.
- Cada registro deve conter: matrícula do funcionário, data, hora e tipo (entrada/saída).

### **RF3 — Consultar dados do funcionário**
- Permitir visualizar os dados cadastrais de um funcionário e seu histórico de ponto.

### **RF4 — Gerar relatórios**
- Gerar gráficos:  
  - **(a)** gráfico de barras com funcionários ordenados por idade;  
  - **(b)** gráfico de pizza com distribuição de funcionários por turno.  
- **Exportar dados (opcional):** salvar em arquivo CSV/Excel.

### **RF5 — Controle de integridade**
- Ao registrar ponto, confirmar que a matrícula existe.  
- Não permitir registros no futuro sem confirmação.

### **RF6 — Relatórios diários/por período**
- Permitir filtrar registros por data, funcionário e intervalo de datas.

---

## 2. Requisitos Não Funcionais (RNF)

### **RNF1 — Simplicidade de UI**
- Interface simples de entrada de dados (poderá ser CLI, Tkinter ou Web simples).

### **RNF2 — Persistência**
- Dados devem ser salvos em arquivo local CSV/Excel/SQLite.

### **RNF3 — Portabilidade**
- O código em Python deve rodar em Windows/macOS/Linux  
  *(dependências: pandas, matplotlib, openpyxl para exportar Excel).*

### **RNF4 — Desempenho**
- Suportar ao menos centenas de funcionários sem degradação perceptível.

### **RNF5 — Segurança mínima**
- Controle de acesso básico (pode ser senha em futura versão).

### **RNF6 — Legibilidade do código**
- Documentação e comentários no código.
