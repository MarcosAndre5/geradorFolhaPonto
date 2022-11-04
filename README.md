# Gerador de Folha Ponto
O projeto tem como objetivo o desenvolvimento de uma ferramenta para geração de folhas de pontos de funcionarios, trabalho esse que se for feito por meio de editores de texto, mostrando-se uma tarefa muito repetitiva, tediosa e suscetível a erros.

## Pré-requisitos
* Python 3
* Pandas
    ```
    pip install pandas
    ```
## Diagrama de Casos de Uso
<img src="https://github.com/MarcosAndre5/geradorFolhaPonto/blob/main/imagens/casoDeUso_folhaPontos.jpeg" width="350">

## Imagens
### Tela Inícial
<img src="https://github.com/MarcosAndre5/geradorFolhaPonto/blob/main/imagens/interface.png" width="350">

### Exemplo
O usuário poderá realizar os seguintes passos para gerar folha de pontos:
- Informar o nome do servidor ou importar os nomes de uma base de dados pré-definida pela Secretaria Geral;
- Informar o mês da folha;
- Se o mês for fevereiro, o software abrirá a opção para informar se o ano é bissexto;
- Informar o primeiro dia do mês, se é um Sábado ou Domingo ou Segunda-Feira…;
- Informar quais são os dias feriados do mês, caso tenha.

<img src="https://github.com/MarcosAndre5/geradorFolhaPonto/blob/main/imagens/exemplo.png" width="350">

### Exemplo 2
Na geração da folha por meio da importação de nomes de um arquivo pré-definido, teremos um arquivo no formato .csv ou .txt, onde estarão todos os nomes dos funcionarios. No software existirá uma caixa onde o usuário poderá marcar, assim será consumido do arquivo e gerado uma folha de ponto para cada nome definido no arquivo de texto.

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
