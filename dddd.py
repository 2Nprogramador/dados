import streamlit as st
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from io import BytesIO

def formatar_docx(file, espacamento, fonte):
    # Carrega o documento
    doc = Document(file)

    # Define as margens (em polegadas)
    sections = doc.sections
    for section in sections:
        section.left_margin = Pt(3 * 28.35)  # 3 cm em pontos
        section.right_margin = Pt(2 * 28.35)  # 2 cm em pontos
        section.top_margin = Pt(3 * 28.35)  # 3 cm em pontos
        section.bottom_margin = Pt(2 * 28.35)  # 2 cm em pontos

    # Define a fonte e o espaçamento para cada parágrafo
    for para in doc.paragraphs:
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY  # Texto justificado
        for run in para.runs:
            run.font.name = fonte
            run._element.rPr.rFonts.set(qn('w:eastAsia'), fonte)  # Define a fonte para caracteres asiáticos também
            run.font.size = Pt(12)  # Tamanho da fonte

        # Define o espaçamento entre linhas
        if espacamento == "1,0":
            para.paragraph_format.line_spacing = Pt(12)  # Espaçamento de 1,0 linha
        else:
            para.paragraph_format.line_spacing = Pt(18)  # Espaçamento de 1,5 linha

    # Salva o documento em um buffer
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)

    return buffer

def main():
    st.title("Formatador de Documento ABNT")

    st.sidebar.header("Parâmetros de Formatação")
    uploaded_file = st.file_uploader("Escolha um arquivo DOCX", type="docx")

    espacamento = st.sidebar.selectbox("Espaçamento de texto:", ["1,0", "1,5"])
    fonte = st.sidebar.selectbox("Fonte:", ["Arial", "Times New Roman"])

    if uploaded_file is not None:
        if st.button("Aplicar Formatação"):
            documento_buffer = formatar_docx(uploaded_file, espacamento, fonte)
            st.success("Formatação aplicada com sucesso!")

            st.download_button(
                label="Baixar Documento Formatado",
                data=documento_buffer,
                file_name="documento_formatado.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

if __name__ == "__main__":
    main()
