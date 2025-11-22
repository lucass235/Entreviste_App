# Ficha de Requisitos (Grupo 3)

## 1. Requisitos Funcionais (RF)

### **RF1 - Cadastrar funcionário**

- O sistema deve permitir cadastrar um funcionário com os campos: matrícula (única), nome, idade e turno (matutino / vespertino / noturno).
- Deve validar duplicidade de matrícula.

### **RF2 - Registrar ponto (entrada/saída)**

- O sistema deve permitir registrar diariamente horários de entrada e saída para cada funcionário.
- Cada registro deve conter: matrícula do funcionário, data, hora e tipo (entrada/saída).

### **RF3 - Consultar dados do funcionário**

- Permitir visualizar os dados cadastrais de um funcionário e seu histórico de ponto.

### **RF4 - Gerar relatórios**

- Gerar gráficos:  
  - **(a)** gráfico de barras com funcionários ordenados por idade;  
  - **(b)** gráfico de pizza com distribuição de funcionários por turno.  
- **Exportar dados (opcional):** salvar em arquivo CSV/Excel.

### **RF5 - Controle de integridade**

- Ao registrar ponto, confirmar que a matrícula existe.  
- Não permitir registros no futuro sem confirmação.

### **RF6 - Relatórios diários/por período**

- Permitir filtrar registros por data, funcionário e intervalo de datas.

---

## 2. Requisitos Não Funcionais (RNF)

### **RNF1 - Simplicidade de UI**

- Interface simples de entrada de dados (poderá ser CLI, Tkinter ou Web simples).

### **RNF2 - Persistência**

- Dados devem ser salvos em arquivo local CSV/Excel/SQLite.

### **RNF3 - Portabilidade**

- O código em Python deve rodar em Windows/macOS/Linux  
  *(dependências: pandas, matplotlib, openpyxl para exportar Excel).*

### **RNF4 - Desempenho**

- Suportar ao menos centenas de funcionários sem degradação perceptível.

### **RNF5 - Segurança mínima**

- Controle de acesso básico (pode ser senha em futura versão).

### **RNF6 - Legibilidade do código**

- Documentação e comentários no código.

---

## 3. Metodologia de Extração de Requisitos

A extração dos requisitos do sistema foi realizada com base no texto da entrevista forncecida, que apresenta a necessidade de desenvolvimento de um sistema simples para cadastro de funcionários e controle de ponto.

O procedimento adotado segue práticas reconhecidas da Engenharia de Software para elicitação e análise de requisitos, conforme descrito a seguir.

### 1. Identificação de Elementos Relevantes no Texto

Inicialmente, foi realizada uma leitura detalhada do texto-base, buscando identificar palavras-chave, ações e entidades mencionadas pelo usuário entrevistado. Verbos como "cadastrar", "registrar", "consultar" e "gerar relatórios" foram classificados como indicadores diretos de funcionalidades essenciais.

Da mesma forma, substantivos e informações estruturadas como "funcionário", "matrícula", "idade", "turno" e "horários de entrada e saída" foram reconhecidos como elementos que compõem as estruturas de dados que o sistema deve manipular.

### 2. Derivação dos Requisitos Funcionais

A partir das ações explicitamente descritas no texto, foram extraídos os requisitos funcionais do sistema.

Cada ação mencionada pelo entrevistado foi convertida em uma funcionalidade concreta, como cadastrar funcionários, registrar horário de entrada e saída, consultar dados registrados e gerar relatórios.

Esses requisitos representam diretamente as responsabilidades fundamentais que o sistema deve atender.

### 3. Identificação das Entidades e Atributos

Com base nos elementos informacionais mencionados, foram definidas as entidades principais necessárias ao modelo de dados.

Assim, a entidade Funcionário foi delimitada com os atributos matrícula, nome, idade e turno. Da mesma forma, a necessidade de registrar atividades diárias levou à definição da entidade Registro de Ponto, contendo matrícula do funcionário, data, hora e tipo de registro (entrada/saída). Essas informações estruturam o modelo lógico do sistema.

### 4. Definição dos Atores

A análise do texto permitiu identificar os dois atores que interagem com o sistema.

1. O Funcionário aparece como responsável por registrar sua entrada e saída.
2. Administrador — implícito no contexto da entrevista — é responsável por cadastrar funcionários e gerar relatórios.

### 5. Construção dos Casos de Uso

Com os atores e requisitos definidos, os casos de uso foram elaborados seguindo a relação entre necessidades descritas e operações esperadas do sistema.

Os principais casos de uso identificados foram: Cadastrar Funcionário, Registrar Ponto e Consultar Dados/Gerar Relatórios. Cada caso resume a interação entre ator e sistema conforme indicado na entrevista.

### 6. Extração dos Requisitos Não Funcionais

Embora o texto-base não descrevesse explicitamente requisitos não funcionais, estes foram inferidos considerando o contexto e o objetivo do sistema.

Termos como "sistema simples" e a exigência de manipulação de dados levaram à dedução de requisitos como facilidade de uso, persistência dos dados, portabilidade e desempenho adequado para consultas e relatórios. Esses requisitos complementam o escopo, assegurando que o sistema atenda expectativas de qualidade e usabilidade.

### 7. Integração das Informações ao Modelo Final

A partir das informações coletadas e analisadas, foi possível estruturar os diagramas de casos de uso e classes, além de realizar o desenvolvimento das funcionalidades em Python utilizando a biblioteca pandas.

Todo o conjunto de requisitos funcionais e não funcionais emergiu diretamente do texto da entrevista ou de interpretações fundamentadas sobre o ambiente de uso e as necessidades implícitas.
