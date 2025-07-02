import math
from pathlib import Path
import tkinter as tk
from tkinter import filedialog
from datetime import datetime

def selecionar_arquivo() -> Path | None:
    """
    Abre uma janela para seleção do arquivo SRT ou TXT.
    Retorna um objeto Path para o arquivo selecionado, ou None se nenhum for escolhido.
    """
    root = tk.Tk()
    root.withdraw()
    caminho = filedialog.askopenfilename(
        title="Selecione o arquivo .srt ou .txt",
        filetypes=[("Arquivos SRT ou TXT", "*.srt;*.txt"), ("Todos os Arquivos", "*.*")]
    )
    root.destroy()
    if not caminho:
        return None
    return Path(caminho)


def ler_conteudo(caminho_arquivo: Path) -> str:
    """
    Lê todo o conteúdo do arquivo como string e normaliza quebras de linha.
    """
    with caminho_arquivo.open('r', encoding='utf-8') as f:
        conteudo = f.read()
    return conteudo.replace('\r\n', '\n').replace('\r', '\n')


def contar_total_palavras(conteudo: str) -> int:
    """
    Conta o número total de palavras no texto, separadas por whitespace.
    """
    return len(conteudo.split())


def determinar_numero_partes_por_palavras(
    total_palavras: int,
    tamanho_alvo: int = 2500, # Tamanho alvo de palavras por parte
    min_parts: int = 2, # Número mínimo de partes
    max_parts: int = 10 # Número máximo de partes
) -> tuple[int, int, int, int]:
    """
    Calcula quantas partes criar com base no total de palavras:
      - partes_estimadas = ceil(total_palavras / tamanho_alvo)
      - n_partes = clamp(partes_estimadas, min_parts, max_parts)
    Retorna (n_partes, partes_estimadas, max_parts, tamanho_alvo).
    """
    partes_estimadas = math.ceil(total_palavras / tamanho_alvo)
    n_partes = max(min_parts, min(partes_estimadas, max_parts))
    return n_partes, partes_estimadas, max_parts, tamanho_alvo


def dividir_por_palavras(
    conteudo: str,
    n_partes: int
) -> list[str]:
    """
    Divide o texto em n_partes, aproximando-se de igual número de palavras em cada.
    """
    palavras = conteudo.split()
    total = len(palavras)
    tamanho_base = total // n_partes
    resto = total % n_partes

    blocos: list[str] = []
    inicio = 0
    for i in range(n_partes):
        tamanho = tamanho_base + (1 if i < resto else 0)
        bloco_palavras = palavras[inicio:inicio + tamanho]
        blocos.append(' '.join(bloco_palavras))
        inicio += tamanho
    return blocos


def criar_diretorio_saida(caminho_original: Path) -> Path:
    """
    Cria uma nova pasta no mesmo diretório do arquivo original, com nome baseado em timestamp.
    """
    diretorio = caminho_original.parent
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pasta_saida = diretorio / timestamp
    pasta_saida.mkdir(exist_ok=True)
    return pasta_saida


def salvar_blocos(
    blocos: list[str],
    caminho_original: Path
) -> None:
    """
    Salva cada bloco de texto em um arquivo .txt na pasta de saída.
    Nomes: <nome_base>_parte<i>.txt
    """
    diretorio_saida = criar_diretorio_saida(caminho_original)
    nome_base = caminho_original.stem

    for i, texto in enumerate(blocos, start=1):
        novo_nome = f"{nome_base}_parte{i}.txt"
        caminho_novo = diretorio_saida / novo_nome
        with caminho_novo.open('w', encoding='utf-8') as f:
            f.write(texto)
        print(f"Arquivo salvo: {caminho_novo}")


def main() -> None:
    caminho = selecionar_arquivo()
    if caminho is None:
        print("Nenhum arquivo foi selecionado.")
        return

    try:
        conteudo = ler_conteudo(caminho)
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
        return

    total_palavras = contar_total_palavras(conteudo)
    print(f"Total de palavras: {total_palavras}")

    n_partes, estimadas, max_parts, alvo = determinar_numero_partes_por_palavras(total_palavras)
    print(
        f"Tamanho alvo por parte: {alvo}\n"
        f"Partes estimadas (ceil): {estimadas}\n"
        f"Teto máximo de partes: {max_parts}\n"
        f"Serão criadas {n_partes} partes."
    )

    blocos = dividir_por_palavras(conteudo, n_partes)

    try:
        salvar_blocos(blocos, caminho)
    except Exception as e:
        print(f"Erro ao salvar os arquivos: {e}")

if __name__ == "__main__":
    main()
