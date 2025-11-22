from app.services.sistema_ponto import SistemaPonto


def menu() -> None:
    sistema = SistemaPonto()

    while True:
        print("\n=== Sistema de Ponto ===")
        print("1 - Cadastrar funcionário")
        print("2 - Listar funcionários")
        print("3 - Registrar entrada")
        print("4 - Registrar saída")
        print("5 - Mostrar gráfico de barras (idade)")
        print("6 - Mostrar gráfico de pizza (turno)")
        print("7 - Listar registros de ponto")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ").strip()

        try:
            if opcao == "1":
                matricula = input("Matrícula: ").strip()
                nome = input("Nome: ").strip()
                idade = int(input("Idade: ").strip())
                turno = input("Turno (MATUTINO/VESPERTINO/NOTURNO): ").strip()
                sistema.cadastrar_funcionario(matricula, nome, idade, turno)
                print("Funcionário cadastrado com sucesso.")

            elif opcao == "2":
                df = sistema.dataframe_funcionarios()
                if df.empty:
                    print("Nenhum funcionário cadastrado.")
                else:
                    print(df)

            elif opcao == "3":
                matricula = input("Matrícula: ").strip()
                sistema.registrar_entrada(matricula)
                print("Entrada registrada com sucesso.")

            elif opcao == "4":
                matricula = input("Matrícula: ").strip()
                sistema.registrar_saida(matricula)
                print("Saída registrada com sucesso.")

            elif opcao == "5":
                sistema.grafico_barras_por_idade()

            elif opcao == "6":
                sistema.grafico_pizza_por_turno()

            elif opcao == "7":
                df = sistema.dataframe_registros()
                if df.empty:
                    print("Nenhum registro de ponto.")
                else:
                    print(df)

            elif opcao == "0":
                print("Saindo...")
                break

            else:
                print("Opção inválida.")

        except Exception as e:
            print(f"Erro: {e}")
