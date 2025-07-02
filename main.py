import os
import tkinter as tk
from tkinter import filedialog
from datetime import datetime


def selecionar_arquivo():
    """
    Abre uma janela para seleção do arquivo SRT ou TXT.
    Retorna o caminho do arquivo selecionado.
    """
    root = tk.Tk()
    root.withdraw()
    caminho_arquivo = filedialog.askopenfilename(
        title="Selecione o arquivo .srt ou .txt",
        filetypes=[("Arquivos SRT ou TXT", "*.srt;*.txt"), ("Todos os Arquivos", "*.*")]
    )
    return caminho_arquivo


def ler_paragrafos_srt(caminho_arquivo):
    """
    Lê o arquivo SRT e extrai os parágrafos válidos.
    Cada parágrafo é um bloco de texto separado por quebras de linha duplas.

    :param caminho_arquivo: Caminho do arquivo SRT.
    :return: Lista de parágrafos (blocos) não vazios.
    """
    with open(caminho_arquivo, 'r', encoding='utf-8') as file:
        conteudo = file.read()

    # Normaliza as quebras de linha para o padrão \n
    conteudo = conteudo.replace('\r\n', '\n').replace('\r', '\n')

    # Divide o conteúdo em blocos usando duas quebras de linha e remove espaços em branco
    blocos = [bloco.strip() for bloco in conteudo.split('\n\n') if bloco.strip() != '']

    return blocos


def determinar_numero_partes(total_paragrafos):
    """
    Determina em quantas partes o arquivo deverá ser dividido,
    com base na quantidade total de parágrafos.

    Critério adotado:
      - Arquivos pequenos a médios: 2 partes;
      - Arquivos intermediários: 3 partes;
      - Arquivos muito grandes: 4 partes.

    :param total_paragrafos: Quantidade total de parágrafos válidos.
    :return: Número de partes (2, 3 ou 4).
    """
    if total_paragrafos < 50:
        return 2
    elif total_paragrafos < 150:
        return 3
    else:
        return 4


def dividir_lista_em_blocos(lista, n):
    """
    Divide uma lista em n blocos com tamanhos similares.

    :param lista: Lista original a ser dividida.
    :param n: Número de blocos desejados.
    :return: Lista de listas (blocos).
    """
    total = len(lista)
    blocos = []

    # Tamanho base de cada bloco e o resto que serão distribuídos (um a um) nos primeiros blocos
    tamanho_base = total // n
    resto = total % n

    inicio = 0
    for i in range(n):
        tamanho_atual = tamanho_base + (1 if i < resto else 0)
        fim = inicio + tamanho_atual
        blocos.append(lista[inicio:fim])
        inicio = fim

    return blocos


def criar_diretorio_saida(caminho_original):
    """
    Cria uma nova pasta no mesmo diretório do arquivo original, usando data e hora para o nome.
    O nome gerado não possui símbolos para garantir que seja válido.

    :param caminho_original: Caminho do arquivo SRT original.
    :return: Caminho completo para a nova pasta criada.
    """
    diretorio, _ = os.path.split(caminho_original)

    # Gera um nome com data e hora (ex: 20250205_153045)
    nome_pasta = datetime.now().strftime("%Y%m%d_%H%M%S")
    caminho_novo = os.path.join(diretorio, nome_pasta)

    # Cria a pasta, se não existir
    os.makedirs(caminho_novo, exist_ok=True)

    return caminho_novo


def salvar_blocos(blocos, caminho_original):
    """
    Salva cada bloco de parágrafos em um arquivo .txt.
    Os arquivos serão salvos em uma nova pasta criada no mesmo diretório do arquivo original.

    :param blocos: Lista de blocos (cada bloco é uma lista de parágrafos).
    :param caminho_original: Caminho do arquivo SRT original.
    """
    # Cria o diretório de saída com base na data e hora
    diretorio_saida = criar_diretorio_saida(caminho_original)

    # Extrai o nome base do arquivo original
    _, nome_arquivo = os.path.split(caminho_original)
    nome_base, _ = os.path.splitext(nome_arquivo)

    for i, bloco in enumerate(blocos, start=1):
        novo_nome = f"{nome_base}_parte{i}.txt"
        caminho_novo = os.path.join(diretorio_saida, novo_nome)

        # Junta os parágrafos com duas quebras de linha para preservar o formato de separação
        with open(caminho_novo, 'w', encoding='utf-8') as f:
            f.write("\n\n".join(bloco))

        print(f"Arquivo salvo: {caminho_novo}")


def main():
    """
    Função principal que orquestra a seleção do arquivo, leitura, divisão e gravação.
    """
    caminho_srt = selecionar_arquivo()
    if not caminho_srt:
        print("Nenhum arquivo foi selecionado.")
        return

    paragrafos = ler_paragrafos_srt(caminho_srt)
    total_paragrafos = len(paragrafos)
    print(f"Total de parágrafos válidos: {total_paragrafos}")

    num_partes = determinar_numero_partes(total_paragrafos)
    print(f"O arquivo será dividido em {num_partes} partes.")

    blocos = dividir_lista_em_blocos(paragrafos, num_partes)

    salvar_blocos(blocos, caminho_srt)


if __name__ == "__main__":
    main()
