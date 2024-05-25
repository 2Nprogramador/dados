import tkinter as tk
from tkinter import messagebox, filedialog
import re
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

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

def copiar_texto_formatado():
    """Formata o texto e exibe em uma messagebox."""
    texto_formatado = formatar_texto_abnt(texto_entrada.get("1.0", "end-1c"))
    messagebox.showinfo("Texto Formatado", texto_formatado)

def exportar_para_word():
    """Exporta o texto formatado para um arquivo Word."""
    texto_formatado = formatar_texto_abnt(texto_entrada.get("1.0", "end-1c"))

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

        if len(paragrafo) > 40:  # Exemplo de citação longa
            p.paragraph_format.line_spacing = 1.0
        else:
            p.paragraph_format.line_spacing = 1.5

    # Salva o documento em um arquivo.
    caminho_arquivo = filedialog.asksaveasfilename(defaultextension=".docx", filetypes=[("Arquivos do Word", "*.docx")])
    if caminho_arquivo:
        documento.save(caminho_arquivo)
        # Exibe uma mensagem de sucesso.
        messagebox.showinfo("Arquivo exportado", "O texto formatado foi exportado com sucesso para o arquivo Word.")

# Cria a janela principal.
root = tk.Tk()
root.title("Formatador de Texto ABNT")

# Cria o widget de entrada de texto.
texto_entrada = tk.Text(root)
texto_entrada.pack()

# Cria o botão para formatar o texto.
botao_formatar = tk.Button(root, text="Formatar", command=copiar_texto_formatado)
botao_formatar.pack()

# Cria o botão para exportar o texto para o Word.
botao_exportar = tk.Button(root, text="Exportar para Word", command=exportar_para_word)
botao_exportar.pack()

# Executa o loop principal da janela.
root.mainloop()
