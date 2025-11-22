"""
sistema_ponto.py
Dependências: pandas, matplotlib, openpyxl (para Excel)
Instalação (pip): pip install pandas matplotlib openpyxl
"""

from datetime import datetime, date
import pandas as pd
import matplotlib.pyplot as plt
import os

# Inicializa DataFrames vazios (ou carrega se já existir arquivo)
EMPLOYEES_FILE = "employees.csv"
ATTENDANCE_FILE = "attendance.csv"

def load_or_create():
    if os.path.exists(EMPLOYEES_FILE):
        employees = pd.read_csv(EMPLOYEES_FILE, dtype={'matricula': str})
    else:
        employees = pd.DataFrame(columns=['matricula','nome','idade','turno'])
    if os.path.exists(ATTENDANCE_FILE):
        attendance = pd.read_csv(ATTENDANCE_FILE, parse_dates=['timestamp'], dtype={'matricula': str})
    else:
        attendance = pd.DataFrame(columns=['matricula','timestamp','tipo'])
    return employees, attendance

employees_df, attendance_df = load_or_create()

# --- Funções principais ---
def save_all():
    employees_df.to_csv(EMPLOYEES_FILE, index=False)
    attendance_df.to_csv(ATTENDANCE_FILE, index=False)

def add_employee(matricula: str, nome: str, idade: int, turno: str) -> bool:
    """
    Cadastra novo funcionário. Retorna True se cadastrado, False se matrícula já existe.
    """
    global employees_df
    matricula = str(matricula)
    if matricula in employees_df['matricula'].values:
        print(f"[erro] Matrícula {matricula} já existe.")
        return False
    new = {'matricula': matricula, 'nome': nome, 'idade': int(idade), 'turno': turno}
    employees_df = pd.concat([employees_df, pd.DataFrame([new])], ignore_index=True)
    save_all()
    print(f"[ok] Funcionário {nome} ({matricula}) cadastrado.")
    return True

def register_punch(matricula: str, tipo: str, ts: datetime = None) -> bool:
    """
    Registra ponto (tipo: 'entrada' ou 'saida'). Retorna True se ok.
    """
    global attendance_df
    matricula = str(matricula)
    if matricula not in employees_df['matricula'].values:
        print(f"[erro] Matrícula {matricula} não encontrada.")
        return False
    if ts is None:
        ts = datetime.now()
    record = {'matricula': matricula, 'timestamp': ts, 'tipo': tipo}
    
    attendance_df = pd.concat([attendance_df, pd.DataFrame([record])], ignore_index=True)
    # Garantir formato de timestamp
    attendance_df['timestamp'] = pd.to_datetime(attendance_df['timestamp'])
    save_all()
    print(f"[ok] {tipo} registrada para {matricula} em {ts}.")
    return True

def get_employee_records(matricula: str) -> pd.DataFrame:
    matricula = str(matricula)
    if matricula not in employees_df['matricula'].values:
        raise ValueError("Matrícula não encontrada.")
    recs = attendance_df[attendance_df['matricula'] == matricula].sort_values('timestamp')
    return recs

# --- Relatórios / Gráficos ---
def plot_age_bar(save_path: str = None):
    """
    Gera gráfico de barras de funcionários ordenados por idade.
    """
    if employees_df.empty:
        print("[aviso] Sem funcionários para plotar.")
        return
    df = employees_df.copy()
    df['idade'] = df['idade'].astype(int)
    df_sorted = df.sort_values('idade', ascending=False)  # maior primeiro (pode ajustar)
    plt.figure(figsize=(10,6))
    plt.bar(df_sorted['nome'], df_sorted['idade'])
    plt.xticks(rotation=45, ha='right')
    plt.ylabel("Idade")
    plt.title("Funcionários ordenados por idade")
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
        print(f"[ok] Gráfico salvo em {save_path}")
    else:
        plt.show()
    plt.close()

def plot_shift_pie(save_path: str = None):
    """
    Gera gráfico de pizza com porcentagem de funcionários por turno.
    """
    if employees_df.empty:
        print("[aviso] Sem funcionários para plotar.")
        return
    counts = employees_df['turno'].value_counts()
    plt.figure(figsize=(6,6))
    counts.plot.pie(autopct='%1.1f%%', startangle=90)
    plt.ylabel("")
    plt.title("Distribuição de funcionários por turno")
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
        print(f"[ok] Gráfico salvo em {save_path}")
    else:
        plt.show()
    plt.close()

def export_to_excel(path="dados_sistema_ponto.xlsx"):
    """
    Exporta employees e attendance para um arquivo Excel com duas abas.
    """
    with pd.ExcelWriter(path, engine='openpyxl') as writer:
        employees_df.to_excel(writer, sheet_name='Employees', index=False)
        attendance_df.to_excel(writer, sheet_name='Attendance', index=False)
    print(f"[ok] Exportado para {path}")

# --- Exemplo de uso (Se preferir @Lucas, pode mudar pra uma UI) ---
if __name__ == "__main__":
    # Exemplo: cadastrar alguns funcionários (somente se não existirem)
    if employees_df.empty:
        add_employee("1001", "Ana Silva", 34, "Matutino")
        add_employee("1002", "Bruno Costa", 29, "Vespertino")
        add_employee("1003", "Carla Souza", 41, "Noturno")
    # Registrar punches de exemplo
    register_punch("1001", "entrada")
    register_punch("1002", "entrada")
    register_punch("1001", "saida")
    # Gerar gráficos e exportar
    plot_age_bar("idade_barras.png")
    plot_shift_pie("turno_pizza.png")
    export_to_excel("dados_sistema_ponto.xlsx")
