import streamlit as st
from io import BytesIO


def gerar_rtf(texto, espacamento, fonte):
    # Define a fonte com base na escolha do usuário
    if fonte == "Arial":
        font_rtf = r"{\fonttbl{\f0 Arial;}}"
    else:
        font_rtf = r"{\fonttbl{\f0 Times New Roman;}}"

    # Cabeçalho do arquivo RTF com margens ABNT e fonte selecionada
    rtf_header = (
        r"{\rtf1\ansi\deff0"
        f"{font_rtf}"
        r"{\colortbl ;\red0\green0\blue0;}"
        r"\margl1701\margr1134\margt1701\margb1134"  # Margens: esquerda e superior 3cm, direita e inferior 2cm
        r"\f0\fs24"  # Fonte selecionada, tamanho 12 (24 half-points)
    )

    # Configura o espaçamento de linha
    if espacamento == "1,0":
        line_spacing = r"\sl240\slmult1"
    else:
        line_spacing = r"\sl360\slmult1"

    # Configura a indentação do parágrafo
    paragraph_indent = r"\fi720"  # 1,25 cm

    # Justificação do parágrafo
    paragraph_justification = r"\qj"  # Justificado

    # Formata o texto
    paragraphs = texto.split('\n')
    formatted_text = ''
    for para in paragraphs:
        formatted_text += f"{paragraph_indent}{paragraph_justification} {para}\\par "

    # Combina todas as partes do RTF
    rtf_content = (
        f"{rtf_header}"
        f"{line_spacing}"
        f"{formatted_text}"
        r"}"
    )

    # Salva o RTF em um buffer
    buffer = BytesIO()
    buffer.write(rtf_content.encode('utf-8'))
    buffer.seek(0)
    return buffer


def main():
    st.title("Formatador de Texto ABNT")

    # Entrada de texto
    st.sidebar.header("Parâmetros de Formatação")
    texto = st.text_area("Insira seu texto aqui:")

    # Opções para espaçamento de texto
    espacamento = st.sidebar.selectbox("Espaçamento de texto:", ["1,0", "1,5"])

    # Opções para seleção de fonte
    fonte = st.sidebar.selectbox("Fonte:", ["Arial", "Times New Roman"])

    # Botão para aplicar formatação
    if st.button("Aplicar Formatação"):
        if texto.strip():
            # Aplica a formatação e obtém o documento RTF
            documento_buffer = gerar_rtf(texto, espacamento, fonte)

            # Mostra uma mensagem de sucesso
            st.success("Formatação aplicada com sucesso!")

            # Botão para baixar o documento RTF
            st.download_button(
                label="Baixar RTF",
                data=documento_buffer,
                file_name="texto_formatado.rtf",
                mime="application/rtf"
            )
        else:
            st.error("Por favor, insira algum texto para formatar.")


if __name__ == "__main__":
    main()
