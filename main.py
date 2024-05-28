import streamlit as st
from docx import Document
from docx.shared import Pt, Inches, Cm
from io import BytesIO
from docx.enum.text import WD_ALIGN_PARAGRAPH

def aplicar_formatacao(texto, alinhamento, espacamento, fonte):
    # Define o alinhamento do texto
    if alinhamento == "Justificado":
        alinhamento = WD_ALIGN_PARAGRAPH.JUSTIFY
    elif alinhamento == "À Esquerda":
        alinhamento = WD_ALIGN_PARAGRAPH.LEFT

    # Define o espaçamento de texto
    if espacamento == "1,0":
        line_spacing = Pt(12)
    else:
        line_spacing = Pt(18)

    # Cria um documento DOCX
    doc = Document()

    # Define as margens do documento
    sections = doc.sections
    for section in sections:
        section.top_margin = Cm(3)
        section.bottom_margin = Cm(2)
        section.left_margin = Cm(3)
        section.right_margin = Cm(2)

    p = doc.add_paragraph(texto)

    # Aplica a formatação ao parágrafo
    p.alignment = alinhamento
    p.paragraph_format.line_spacing = line_spacing
    run = p.runs[0]
    run.font.name = fonte
    run.font.size = Pt(12)  # Tamanho da fonte em pontos

    # Salva o documento em um buffer
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer



def main():
    st.title("Formatador de Texto ABNT")

    # Entrada de texto
    texto = st.text_area("Insira seu texto aqui:")

    # Opções para alinhamento, espaçamento de texto e fonte
    alinhamento = st.selectbox("Alinhamento:", ["Justificado", "À Esquerda"])
    espacamento = st.selectbox("Espaçamento de texto:", ["1,0", "1,5"])
    fonte = st.selectbox("Fonte:", ["Arial", "Times New Roman"])

    # Botão para aplicar formatação
    if st.button("Aplicar Formatação"):
        # Aplica a formatação e obtém o documento DOCX
        documento_buffer = aplicar_formatacao(texto, alinhamento, espacamento, fonte)

        # Mostra uma mensagem de sucesso
        st.success("Formatação aplicada com sucesso!")

        # Botão para baixar o documento DOCX
        st.download_button(
            label="Baixar DOCX",
            data=documento_buffer,
            file_name="texto_formatado.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )


if __name__ == "__main__":
    main()
