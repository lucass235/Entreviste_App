import streamlit as st
import pandas as pd

from app.services.sistema_ponto import SistemaPonto
from app.models.turno import Turno
from app.models.usuario import Usuario, PapelUsuario


def pagina_admin(sistema: SistemaPonto, menu: str) -> None:
    # ---------- ADMIN: REGISTRAR DADOS DO FUNCIONÁRIO ----------
    if menu == "Registrar dados do funcionário":
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

    # ---------- ADMIN: EDITAR DADOS DO FUNCIONÁRIO ----------
    elif menu == "Editar dados do funcionário":
        st.subheader("Editar dados do funcionário")
        df = sistema.dataframe_funcionarios()
        if df.empty:
            st.info("Nenhum funcionário cadastrado.")
        else:
            opcoes = {
                f"{row['matricula']} - {row['nome']}": row
                for _, row in df.iterrows()
            }
            chave = st.selectbox("Funcionário", list(opcoes.keys()))
            row = opcoes[chave]

            with st.form("form_editar_funcionario"):
                novo_nome = st.text_input("Nome", value=row["nome"])
                nova_idade = st.number_input(
                    "Idade", min_value=16, max_value=100, step=1, value=int(row["idade"])
                )
                turno_atual = row["turno"]
                turno_label = st.selectbox(
                    "Turno",
                    [t.value for t in Turno],
                    index=[t.value for t in Turno].index(turno_atual),
                )
                submit = st.form_submit_button("Salvar alterações")

                if submit:
                    try:
                        turno_name = [t.name for t in Turno if t.value == turno_label][0]
                        sistema.editar_funcionario(
                            matricula=str(row["matricula"]),
                            nome=novo_nome,
                            idade=int(nova_idade),
                            turno=turno_name,
                        )
                        st.success("Dados do funcionário atualizados com sucesso!")
                    except Exception as e:
                        st.error(str(e))

    # ---------- ADMIN: CONSULTAR DADOS DO FUNCIONÁRIO ----------
    elif menu == "Consultar dados do funcionário":
        st.subheader("Consulta de dados do funcionário")
        df_func = sistema.dataframe_funcionarios()
        df_reg = sistema.dataframe_registros()

        if df_func.empty:
            st.info("Nenhum funcionário cadastrado.")
        else:
            st.markdown("### Lista de funcionários")
            st.dataframe(df_func)

            if not df_reg.empty:
                st.markdown("### Detalhes de um funcionário")
                opcoes = {
                    f"{row['matricula']} - {row['nome']}": str(row["matricula"])
                    for _, row in df_func.iterrows()
                }
                chave = st.selectbox("Selecione o funcionário", list(opcoes.keys()))
                matricula_sel = opcoes[chave]

                dados = df_func[df_func["matricula"] == matricula_sel]
                historico = (
                    df_reg[df_reg["matricula"] == matricula_sel]
                    .sort_values("timestamp")
                )

                st.markdown("#### Dados cadastrais")
                st.dataframe(dados)

                st.markdown("#### Histórico de ponto")
                st.dataframe(historico)
            else:
                st.info("Ainda não há registros de ponto.")

    # ---------- ADMIN: CONSULTAR HORÁRIOS DE ENTRADA E SAÍDA ----------
    elif menu == "Consultar horários de entrada e saída":
        st.subheader("Registros de Ponto")
        df = sistema.dataframe_registros()
        if df.empty:
            st.info("Nenhum registro encontrado.")
        else:
            df["timestamp"] = pd.to_datetime(df["timestamp"])

            st.markdown("### Filtros")

            funcionarios = sorted(df["matricula"].unique())
            matricula_filtro = st.selectbox(
                "Filtrar por funcionário (opcional)",
                ["Todos"] + funcionarios,
            )

            data_min = df["timestamp"].dt.date.min()
            data_max = df["timestamp"].dt.date.max()
            data_inicio, data_fim = st.date_input(
                "Intervalo de datas",
                (data_min, data_max),
            )

            filtrado = df.copy()
            if matricula_filtro != "Todos":
                filtrado = filtrado[filtrado["matricula"] == matricula_filtro]

            filtrado = filtrado[
                (filtrado["timestamp"].dt.date >= data_inicio)
                & (filtrado["timestamp"].dt.date <= data_fim)
            ].sort_values("timestamp", ascending=False)

            st.markdown("### Registros filtrados")
            st.dataframe(filtrado)

    # ---------- ADMIN: GERAR RELATÓRIOS ----------
    elif menu == "Gerar relatórios":
        st.subheader("Relatórios gráficos")
        df_func = sistema.dataframe_funcionarios()
        if df_func.empty:
            st.info("Cadastre funcionários para visualizar gráficos.")
        else:
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**Funcionários ordenados por idade**")
                fig_idade = sistema.grafico_barras_por_idade(show=False)
                if fig_idade is None:
                    st.info("Sem dados para o gráfico.")
                else:
                    st.pyplot(fig_idade)

            with col2:
                st.markdown("**Funcionários por turno**")
                fig_turno = sistema.grafico_pizza_por_turno(show=False)
                if fig_turno is None:
                    st.info("Sem dados para o gráfico.")
                else:
                    st.pyplot(fig_turno)


def pagina_funcionario(sistema: SistemaPonto, usuario: Usuario, menu: str) -> None:
    if not usuario.matricula:
        st.warning("Informe sua matrícula na barra lateral para usar as funções.")
        return

    matricula = usuario.matricula

    # Caso de uso: Confirmar matrícula / Falha em confirmar matrícula
    if not sistema.confirmar_matricula(matricula):
        st.error("Falha em confirmar matrícula. Verifique a matrícula informada.")
        return

    # ---------- FUNCIONÁRIO: REGISTRAR CHEGADA ----------
    if menu == "Registrar horário de chegada":
        st.subheader("Registrar horário de chegada")
        if st.button("Registrar chegada agora"):
            try:
                sistema.registrar_entrada(matricula)
                st.success("Horário de chegada registrado com sucesso!")
            except Exception as e:
                st.error(str(e))

    # ---------- FUNCIONÁRIO: REGISTRAR SAÍDA ----------
    elif menu == "Registrar horário de saída":
        st.subheader("Registrar horário de saída")
        if st.button("Registrar saída agora"):
            try:
                sistema.registrar_saida(matricula)
                st.success("Horário de saída registrado com sucesso!")
            except Exception as e:
                st.error(str(e))

    # ---------- FUNCIONÁRIO: CONSULTAR MEUS DADOS ----------
    elif menu == "Consultar meus dados":
        st.subheader("Meus dados e histórico de ponto")

        df_func = sistema.dataframe_funcionarios()
        df_reg = sistema.dataframe_registros()

        dados = df_func[df_func["matricula"] == matricula]
        if dados.empty:
            st.error("Funcionário não encontrado. Verifique a matrícula.")
            return

        st.markdown("### Dados cadastrais")
        st.dataframe(dados)

        historico = df_reg[df_reg["matricula"] == matricula].copy()
        if historico.empty:
            st.info("Ainda não há registros de ponto para esta matrícula.")
        else:
            historico = historico.sort_values("timestamp")
            st.markdown("### Histórico de ponto")
            st.dataframe(historico)


def main():
    st.set_page_config(page_title="Sistema de Ponto", layout="wide")
    st.title("Sistema de Ponto - Empresa PontoFácil")

    sistema = SistemaPonto()

    st.sidebar.title("Acesso ao sistema")
    tipo_usuario_label = st.sidebar.radio(
        "Perfil",
        [p.value for p in PapelUsuario],
    )

    if tipo_usuario_label == PapelUsuario.ADMINISTRADOR.value:
        usuario = Usuario(papel=PapelUsuario.ADMINISTRADOR)
        menu = st.sidebar.radio(
            "Navegação (Administrador)",
            [
                "Registrar dados do funcionário",
                "Editar dados do funcionário",
                "Consultar dados do funcionário",
                "Consultar horários de entrada e saída",
                "Gerar relatórios",
            ],
        )
        pagina_admin(sistema, menu)
    else:
        matricula_login = st.sidebar.text_input("Matrícula do funcionário")
        usuario = Usuario(papel=PapelUsuario.FUNCIONARIO, matricula=matricula_login or None)
        menu = st.sidebar.radio(
            "Navegação (Funcionário)",
            [
                "Registrar horário de chegada",
                "Registrar horário de saída",
                "Consultar meus dados",
            ],
        )
        pagina_funcionario(sistema, usuario, menu)


if __name__ == "__main__":
    main()
