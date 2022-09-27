# Gerador de Folha Ponto
Projeto em Python para geração de folha de pontos de funcionários.

### Pré-requisitos
* Python 3
* Pandas
    ```
    pip install pandas
    ```

### Gerando o arquivo executável
* Pyinstaller
    ```
    pip install pyinstaller
    ```
    
    ```
    pyinstaller --noconsole --name="Nome do Projeto" --icon="nome_icone.ico" --add-data="nome_icone.ico;." --onefile <nome_arquivo.py>
    ```
