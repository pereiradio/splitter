# Divisor de Arquivos por Palavras

Este script em Python lê um arquivo de legendas (`.srt`) ou texto simples (`.txt`) e o divide em múltiplos arquivos de saída, equilibrando o número de palavras em cada parte.

## Funcionalidades

* **Seleção de arquivo por GUI**: abre uma janela com `tkinter` para escolher o arquivo de entrada.
* **Contagem de palavras**: calcula o total de palavras do texto.
* **Cálculo dinâmico de partes**: determina quantas partes criar com base em:

  * Tamanho-alvo de palavras por arquivo (padrão: 1000)
  * Mínimo de partes (padrão: 2)
  * Máximo de partes (padrão: 10)
* **Divisão equilibrada**: cada arquivo resultante terá aproximadamente o mesmo número de palavras.
* **Saída organizada**: salva todos os arquivos em uma pasta nomeada com timestamp (`YYYYMMDD_HHMMSS`) no mesmo diretório do arquivo original.

## Pré-requisitos

* **Python 3.7+**
* Bibliotecas da biblioteca padrão:

  * `tkinter` (para GUI)
  * `pathlib`, `datetime`, `math`

> **Observação**: `tkinter` geralmente já vem instalado com o Python, mas em algumas distribuições Linux você pode precisar instalar o pacote `python3-tk`.

## Instalação

1. Clone este repositório:

   ```bash
   git clone https://seu-repositorio.git
   cd seu-repositorio
   ```
2. (Opcional) Crie e ative um ambiente virtual:

   ```bash
   python -m venv venv
   # Linux/macOS
   source venv/bin/activate
   # Windows
   venv\Scripts\activate
   ```

## Uso

Execute o script principal:

```bash
python split_srt_por_palavras.py
```

1. Uma janela se abrirá para selecionar o arquivo `.srt` ou `.txt`.
2. O terminal exibirá o total de palavras e a lógica usada para dividir (tamanho-alvo, estimativa de partes, teto, número final).
3. Os arquivos resultantes serão salvos em `./<timestamp>/<nome_base>_parteX.txt`.

## Configuração

Caso queira alterar a forma de divisão, ajuste os valores padrões na função:

```python
def determinar_numero_partes_por_palavras(
    total_palavras: int,
    tamanho_alvo: int = 1000,  # meta de palavras por arquivo
    min_parts: int = 2,        # mínimo de arquivos
    max_parts: int = 10        # máximo de arquivos
) -> tuple[int, int, int, int]:
    ...
```

* **`tamanho_alvo`**: define quantas palavras, em média, cada parte deve conter.
* **`min_parts`**: garante pelo menos este número de arquivos.
* **`max_parts`**: impede que a divisão crie mais do que este número de arquivos.

## Estrutura de Arquivos

```bash
.
├── README.md
└── split_srt_por_palavras.py  # script principal
```

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
