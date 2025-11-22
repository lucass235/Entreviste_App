import streamlit as st
import pandas as pd

from app.services.sistema_ponto import SistemaPonto
from app.models.turno import Turno


def main():
    st.set_page_config(page_title="Sistema de Ponto", layout="wide")
    st.title("Sistema de Ponto - Empresa X")

    sistema = SistemaPonto()

    menu = st.sidebar.radio(
        "Navegação",
        ["Cadastrar Funcionário", "Funcionários", "Registrar Ponto", "Registros", "Gráficos"],
    )

    # ---------- CADASTRO DE FUNCIONÁRIO ----------
    if menu == "Cadastrar Funcionário":
        st.subheader("Cadastro de Funcionários")

        with st.form("form_cadastro_funcionario"):
            matricula = st.text_input("Matrícula")
            nome = st.text_input("Nome")
            idade = st.number_input("Idade", min_value=16, max_value=100, step=1)
            turno_label = st.selectbox(
                "Turno",
                [t.value for t in Turno],
            )
            submit = st.form_submit_button("Salvar")

            if submit:
                if not matricula or not nome:
                    st.error("Preencha matrícula e nome.")
                else:
                    try:
                        # converte do value ("Matutino") para o name do Enum ("MATUTINO")
                        turno_name = [t.name for t in Turno if t.value == turno_label][0]
                        sistema.cadastrar_funcionario(
                            matricula=str(matricula),
                            nome=nome,
                            idade=int(idade),
                            turno=turno_name,
                        )
                        st.success("Funcionário cadastrado com sucesso!")
                    except Exception as e:
                        st.error(str(e))

    # ---------- LISTA DE FUNCIONÁRIOS ----------
    elif menu == "Funcionários":
        st.subheader("Lista de Funcionários")
        df = sistema.dataframe_funcionarios()
        if df.empty:
            st.info("Nenhum funcionário cadastrado.")
        else:
            st.dataframe(df)

    # ---------- REGISTRAR PONTO ----------
    elif menu == "Registrar Ponto":
        st.subheader("Registrar Entrada/Saída")
        df = sistema.dataframe_funcionarios()
        if df.empty:
            st.info("Cadastre um funcionário antes de registrar o ponto.")
        else:
            opcoes = {
                f"{row['matricula']} - {row['nome']}": str(row["matricula"])
                for _, row in df.iterrows()
            }
            chave = st.selectbox("Funcionário", list(opcoes.keys()))
            matricula_escolhida = opcoes[chave]

            tipo = st.radio("Tipo de registro", ["entrada", "saida"], horizontal=True)

            if st.button("Registrar"):
                try:
                    if tipo == "entrada":
                        sistema.registrar_entrada(matricula_escolhida)
                    else:
                        sistema.registrar_saida(matricula_escolhida)
                    st.success(f"Registro de {tipo} salvo com sucesso!")
                except Exception as e:
                    st.error(str(e))

    # ---------- REGISTROS DE PONTO ----------
    elif menu == "Registros":
        st.subheader("Registros de Ponto")
        df = sistema.dataframe_registros()
        if df.empty:
            st.info("Nenhum registro encontrado.")
        else:
            df["timestamp"] = pd.to_datetime(df["timestamp"])
            st.dataframe(df.sort_values("timestamp", ascending=False))

    # ---------- GRÁFICOS ----------
    elif menu == "Gráficos":
        st.subheader("Gráficos")
        df_func = sistema.dataframe_funcionarios()
        if df_func.empty:
            st.info("Cadastre funcionários para visualizar gráficos.")
        else:
            col1, col2 = st.columns(2)

            # Barras - idade (usa serviço, salva PNG e mostra no Streamlit)
            with col1:
                st.markdown("**Funcionários ordenados por idade**")
                fig_idade = sistema.grafico_barras_por_idade(show=False)
                if fig_idade is None:
                    st.info("Sem dados para o gráfico.")
                else:
                    st.pyplot(fig_idade)

            # Pizza - turno (usa serviço, salva PNG e mostra no Streamlit)
            with col2:
                st.markdown("**Funcionários por turno**")
                fig_turno = sistema.grafico_pizza_por_turno(show=False)
                if fig_turno is None:
                    st.info("Sem dados para o gráfico.")
                else:
                    st.pyplot(fig_turno)


if __name__ == "__main__":
    main()
