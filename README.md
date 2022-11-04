# Gerador de Folha Ponto
Projeto em Python para geração de folha de pontos de funcionários.

## Pré-requisitos
* Python 3
* Pandas
    ```
    pip install pandas
    ```

## Imagens
### Tela Inícial
<img src="https://github.com/MarcosAndre5/geradorFolhaPonto/blob/main/imagens/interface.png" width="350">

### Exemplo
<img src="https://github.com/MarcosAndre5/geradorFolhaPonto/blob/main/imagens/exemplo.png" width="350">

### Exemplo 2
<img src="https://github.com/MarcosAndre5/geradorFolhaPonto/blob/main/imagens/exemplo2.png" width="350">

### Folha Gerada
<img src="https://github.com/MarcosAndre5/geradorFolhaPonto/blob/main/imagens/folhaGerada.png" width="350">

## Gerando o arquivo executável
* Pyinstaller
    ```
    pip install pyinstaller
    ```
    
    ```
    pyinstaller --noconsole --name="Nome do Projeto" --icon="nome_icone.ico" --add-data="nome_icone.ico;." --onefile <nome_arquivo.py>
    ```
