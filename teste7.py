import streamlit as st
import pandas as pd
import plotly.graph_objs as go

def abrir_planilha_e_exibir():
    # Abrir uma janela de seleção de arquivo na barra lateral
    caminho_arquivo = st.sidebar.file_uploader("Selecione uma planilha", type=["xlsx", "csv"])

    # Verificar se um arquivo foi selecionado
    if caminho_arquivo is not None:
        try:
            # Ler a planilha usando pandas
            global dados
            dados = pd.read_excel(caminho_arquivo) if caminho_arquivo.name.endswith('xlsx') else pd.read_csv(
                caminho_arquivo)

            # Aplicar filtros
            dados_filtrados = aplicar_filtro(dados)
            # Exibir a planilha principal filtrada
            st.write("## Planilha Principal")
            st.write(dados_filtrados)

            # Adicionar combobox para seleção da coluna
            coluna = st.sidebar.selectbox("Selecione uma coluna", options=dados_filtrados.columns)

            # Se a coluna foi selecionada
            if coluna:
                # Gerar resultado dos métodos estatísticos
                resultado_estatistico = aplicar_metodo_estatistico(coluna, dados_filtrados)

                # Exibir resultado dos métodos estatísticos
                st.write(f"### Resultado dos Métodos Estatísticos para a Coluna '{coluna}'")
                st.write(resultado_estatistico)

        except Exception as e:
            st.error(f"Ocorreu um erro ao abrir a planilha: {e}")

def aplicar_filtro(dados):
    # Adicionar filtros às colunas
    filtro_colunas = {}
    for col in dados.columns:
        filtro_colunas[col] = st.sidebar.multiselect(f"Filtrar por {col}", options=dados[col].unique())

    # Aplicar filtros
    dados_filtrados = dados.copy()
    for col, filtro in filtro_colunas.items():
        if filtro:
            dados_filtrados = dados_filtrados[dados_filtrados[col].isin(filtro)]

    return dados_filtrados


def aplicar_metodo_estatistico(coluna, dados_filtrados):
    # Adicionar combobox para seleção do método estatístico
    metodo_estatistico = st.sidebar.selectbox("Selecione um método estatístico",
                                      ["Média", "Mediana", "Desvio Padrão", "Contagem", "Value Counts", "Describe",
                                       "GroupBy - Soma", "GroupBy - Média"])

    # Se o método estatístico escolhido for GroupBy
    if metodo_estatistico.startswith("GroupBy"):
        # Aplicar GroupBy
        resultado_groupby = aplicar_groupby(metodo_estatistico.split(" - ")[-1].lower(), coluna, dados_filtrados)
        # Se houver resultado do GroupBy
        if resultado_groupby is not None:
            # Exibir resultado em formato de tabela
            st.write(f"### Resultado do GroupBy - {metodo_estatistico.split(' - ')[-1]}")
            st.write(resultado_groupby)
            # Oferecer seleção dos eixos para gráfico
            st.write("### Configurações do Gráfico")
            coluna_x = st.selectbox("Selecione a coluna para o eixo X", options=resultado_groupby.columns)
            coluna_y = st.selectbox("Selecione a coluna para o eixo Y", options=resultado_groupby.columns)
            modo_exibicao = st.selectbox("Selecione o modo de exibição do gráfico", ["BAR", "LINE", "SCATTER"])
            # Exibir o gráfico
            exibir_grafico(resultado_groupby, coluna_x, coluna_y, modo_exibicao)
    else:
        # Aplicar o método estatístico individual na planilha filtrada
        return aplicar_metodo_estatistico_individual(coluna, metodo_estatistico, dados_filtrados)


def aplicar_metodo_estatistico_individual(coluna, metodo, dados_filtrados):
    if metodo == "Média":
        return dados_filtrados[coluna].mean()
    elif metodo == "Mediana":
        return dados_filtrados[coluna].median()
    elif metodo == "Desvio Padrão":
        return dados_filtrados[coluna].std()
    elif metodo == "Contagem":
        return dados_filtrados[coluna].count()
    elif metodo == "Value Counts":
        return dados_filtrados[coluna].value_counts()
    elif metodo == "Describe":
        return dados_filtrados[coluna].describe()


def aplicar_groupby(metodo, coluna, dados_filtrados):
    if coluna:
        try:
            # Filtrar apenas colunas numéricas
            colunas_numericas = dados_filtrados.select_dtypes(include=['float64', 'int64']).columns
            # Aplicar o GroupBy
            resultado = dados_filtrados.groupby(coluna)[colunas_numericas].agg('sum' if metodo == 'soma' else 'mean')
            return resultado.reset_index()
        except Exception as e:
            st.error(f"Ocorreu um erro ao aplicar o GroupBy: {e}")
            return None
    else:
        st.info("Por favor, selecione uma coluna para aplicar o GroupBy.")
        return None


def exibir_grafico(dados, coluna_x, coluna_y, modo_exibicao):
    if dados is not None:
        if modo_exibicao == "BAR":
            fig = go.Figure(go.Bar(x=dados[coluna_x], y=dados[coluna_y]))
        elif modo_exibicao == "LINE":
            fig = go.Figure(go.Line(x=dados[coluna_x], y=dados[coluna_y]))
        elif modo_exibicao == "SCATTER":
            fig = go.Figure(go.Scatter(x=dados[coluna_x], y=dados[coluna_y]))

        fig.update_layout(title=f"Gráfico - {coluna_y} por {coluna_x}", xaxis_title=coluna_x, yaxis_title=coluna_y)
        st.plotly_chart(fig)


# Interface gráfica usando Streamlit
st.title("Analisador Estatístico de Planilhas")

# Botão para abrir uma planilha e exibir
abrir_planilha_e_exibir()
