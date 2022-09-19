from reportlab.lib import colors
from reportlab.lib.pagesizes import inch, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, PageBreak

class PDFGen:
    elementos = []

    def criarNovoDocumento(self, linhas, mes, primeiroDiaMes, nomeFuncionario):
        self.doc = SimpleDocTemplate("Folha_de_Pontos.pdf", pagesize=A4, rightMargin=0, leftMargin=0, topMargin=0, bottomMargin=0)
        
        # Quanto no sábado, supondo (0 - segunda, 6 - domingo)
        diferencaDias = (6 - primeiroDiaMes)
        
        if(isinstance(nomeFuncionario, list)):
            for nome in nomeFuncionario:
                dadosTabela = self.montarTabela(nome, linhas, mes + 1, diferencaDias)

                t = Table(dadosTabela, 11 * [0.65 * inch], (linhas + 2) * [0.34 * inch])
                t.setStyle(TableStyle(self.obterEstiloTabela(linhas + 1, diferencaDias)))
                
                self.elementos.append(t)
                self.elementos.append(PageBreak())
        elif(isinstance(nomeFuncionario, str)):
            dadosTabela = self.montarTabela(nomeFuncionario, linhas, mes + 1, diferencaDias)

            t = Table(dadosTabela, 11 * [0.65 * inch], (linhas + 2) * [0.34 * inch])
            t.setStyle(TableStyle(self.obterEstiloTabela(linhas + 1, diferencaDias)))

            self.elementos.append(t)
            self.elementos.append(PageBreak())

    def montarTabela(self, nome, linhas, mes, diferencaDias):
        dadosTabela = [[nome.upper()]]
        
        sabado = False
        for i in range(0, linhas + 1):
            if i == 0:
                dadosTabela.append(['DATA', 'ENTRADA', 'ASSINATURA', '', '', '', '', '', '', '', 'SAÍDA'])
            elif i % 7 == diferencaDias:
                dadosTabela.append(["{:02d}".format(i) + '/' + "{:02d}".format(mes), '', 'SÁBADO', '', '', '', '', '', '', '', ''])
                sabado = True
            elif i % 7 == diferencaDias + 1 or sabado == True:
                dadosTabela.append(["{:02d}".format(i) + '/' + "{:02d}".format(mes), '', 'DOMINGO', '', '', '', '', '', '', '', ''])
                sabado = False
            else:
                dadosTabela.append(["{:02d}".format(i) + '/' + "{:02d}".format(mes), ':', '', '', '', '', '', '', '', '', ':'])

        return dadosTabela

    def obterEstiloTabela(self, linhas, diferencaDias):
        estiloTabela = [
            ('ALIGN', (0, 0), (10, linhas), 'CENTER'),
            ('VALIGN', (0, 0), (10, linhas), 'MIDDLE'),
            ('BOX', (0, 0), (10, linhas), 0.25, colors.black),
            ('INNERGRID', (0, 0), (10, linhas), 0.25, colors.black),
            ('SPAN', (0, 0), (10, 0)),
            ('SPAN', (2, 1), (4, 1)),
            ('SPAN', (7, 1), (9, 1))
        ]

        # células grandes para nomes
        for i in range(1, linhas + 1):
            estiloTabela.append(('SPAN', (2, i), (9, i)))
            estiloTabela.append(('SPAN', (7, i), (9, i)))

        # Mudandça de cor para as linhas de sábados de domingos
        sabado = False
        for i in range(1, linhas + 1):
            if i % 7 == diferencaDias:
                estiloTabela.append(('BACKGROUND', (0, i+1), (11, i+1), colors.gray))
                sabado = True
            elif i % 7 == diferencaDias + 1 or sabado == True:
                estiloTabela.append(('BACKGROUND', (0, i+1), (11, i+1), colors.gray))
                sabado = False

        return estiloTabela

    def build(self):
        self.doc.build(self.elementos)
