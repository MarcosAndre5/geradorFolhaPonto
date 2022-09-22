from reportlab.lib import colors
from reportlab.lib.pagesizes import inch, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, PageBreak

import os

class PDFGen:
    elementos = []

    def criarNovoDocumento(self, linhas, mes, primeiroDiaMes, nomeFuncionario, feriados):
        if os.path.exists('PDFs') == False:
            os.mkdir('PDFs')

        self.doc = SimpleDocTemplate("PDFs/Folha_de_Pontos_" + self.nomeMes(mes + 1) + ".pdf", pagesize=A4, rightMargin=0, leftMargin=0, topMargin=0, bottomMargin=0)
        
        # Quanto no sábado, supondo (0 - segunda, 6 - domingo)
        diferencaDias = (6 - primeiroDiaMes)
        
        if(isinstance(nomeFuncionario, list)):
            for nome in nomeFuncionario:
                dadosTabela = self.montarTabela(nome, linhas, mes + 1, diferencaDias, feriados)

                t = Table(dadosTabela, 11 * [0.65 * inch], (linhas + 2) * [0.34 * inch])
                t.setStyle(TableStyle(self.obterEstiloTabela(linhas + 1, diferencaDias, feriados)))
                
                self.elementos.append(t)
                self.elementos.append(PageBreak())
        elif(isinstance(nomeFuncionario, str)):
            dadosTabela = self.montarTabela(nomeFuncionario, linhas, mes + 1, diferencaDias, feriados)

            t = Table(dadosTabela, 11 * [0.65 * inch], (linhas + 2) * [0.34 * inch])
            t.setStyle(TableStyle(self.obterEstiloTabela(linhas + 1, diferencaDias, feriados)))

            self.elementos.append(t)
            self.elementos.append(PageBreak())

    def nomeMes(self, mes):
        if mes == 1: return "Janeiro"
        elif mes == 2: return "Fevereiro"
        elif mes == 3: return "Março"
        elif mes == 4: return "Abril"
        elif mes == 5: return "Maio"
        elif mes == 6: return "Junho"
        elif mes == 7: return "Julho"
        elif mes == 8: return "Agosto"
        elif mes == 9: return "Setembro"
        elif mes == 10: return "Outubro"
        elif mes == 11: return "Novembro"
        elif mes == 12: return "Dexembro"

    def montarTabela(self, nome, linhas, mes, diferencaDias, feriados):
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
            elif str(i) in feriados:
                dadosTabela.append(["{:02d}".format(i) + '/' + "{:02d}".format(mes), '', 'FERIADO', '', '', '', '', '', '', '', ''])
            else:
                dadosTabela.append(["{:02d}".format(i) + '/' + "{:02d}".format(mes), ':', '', '', '', '', '', '', '', '', ':'])

        return dadosTabela

    def obterEstiloTabela(self, linhas, diferencaDias, feriados):
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
            elif str(i) in feriados:
                estiloTabela.append(('BACKGROUND', (0, i+1), (11, i+1), colors.gray))

        return estiloTabela

    def build(self):
        self.doc.build(self.elementos)
