import re
import streamlit as st
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH

def formatar_texto_abnt(texto):
    """Formata o texto inserido pelo usuário para as regras ABNT.

    Args:
        texto: O texto a ser formatado.

    Returns:
        O texto formatado de acordo com as regras ABNT.
    """
    # Remove espaços em branco desnecessários.
    texto = re.sub(r'\s+', ' ', texto).strip()

    # Converte aspas simples para aspas duplas.
    texto = texto.replace("'", '"')

    # Remove aspas desnecessárias.
    texto = re.sub(r'(" )|(" $)', '', texto)

    # Adiciona aspas duplas ao redor do título.
    if texto and texto[0].isupper():
        texto = f'"{texto}"'

    # Retorna o texto formatado.
    return texto

def exportar_para_word(texto_formatado, caminho_arquivo, espacamento_citacoes_longas):
    """Exporta o texto formatado para um arquivo Word."""
    # Cria um novo documento do Word.
    documento = Document()

    # Define margens do documento
    sections = documento.sections
    for section in sections:
        section.top_margin = Cm(3)
        section.bottom_margin = Cm(2)
        section.left_margin = Cm(3)
        section.right_margin = Cm(2)

    # Adiciona o texto formatado ao documento.
    for paragrafo in texto_formatado.split("\n"):
        p = documento.add_paragraph(paragrafo)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

        # Define a fonte, tamanho e alinhamento do parágrafo
        style = documento.styles['Normal']
        font = style.font
        font.name = 'Times New Roman'
        font.size = Pt(12)

        # Define o espaçamento do parágrafo
        if espacamento_citacoes_longas:
            p.paragraph_format.line_spacing = 1.0
        else:
            p.paragraph_format.line_spacing = 1.5

    # Salva o documento em um arquivo.
    documento.save(caminho_arquivo)

# Interface gráfica usando Streamlit
st.title("Formatador de Texto ABNT")

# Entrada de texto
texto_entrada = st.text_area("Insira o texto a ser formatado")

# Checkbox para definir o espaçamento para citações longas
espacamento_citacoes_longas = st.checkbox("Ativar espaçamento 1.0 para citações longas")

# Botão para formatar o texto
if st.button("Formatar"):
    texto_formatado = formatar_texto_abnt(texto_entrada)
    st.text_area("Texto Formatado", value=texto_formatado, height=200)

# Entrada do nome do arquivo
caminho_arquivo = st.text_input("Digite o nome do arquivo (com a extensão .docx):")

# Botão para exportar o texto para o Word
if st.button("Exportar para Word"):
    if texto_entrada:
        texto_formatado = formatar_texto_abnt(texto_entrada)
        if caminho_arquivo:
            exportar_para_word(texto_formatado, caminho_arquivo, espacamento_citacoes_longas)
            st.success("O texto formatado foi exportado com sucesso para o arquivo Word.")
        else:
            st.error("Por favor, forneça um nome de arquivo válido.")
    else:
        st.error("Por favor, insira o texto a ser formatado.")
