from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# CSVs
DATA_DIR = BASE_DIR / "data"
EMPLOYEES_CSV = DATA_DIR / "employees.csv"
ATTENDANCE_CSV = DATA_DIR / "attendance.csv"

# Gráficos
GRAFICOS_DIR = BASE_DIR / "graficos"
GRAFICO_IDADE = GRAFICOS_DIR / "idade_barras.png"
GRAFICO_TURNO = GRAFICOS_DIR / "turno_pizza.png"
