from reportlab.lib import colors
from reportlab.lib.pagesizes import inch, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, PageBreak

class PDFGen:
    elements = []

    def create_new_document(self, linhas, mes, primeiroDiaMes, nomesAquivo):
        self.doc = SimpleDocTemplate("Folha_de_Pontos.pdf", pagesize=A4, rightMargin=0, leftMargin=0, topMargin=0, bottomMargin=0)

        # Quanto no sábado, supondo (0 - segunda, 6 - domingo)
        diferencaDias = (7 - primeiroDiaMes)

        for name in nomesAquivo:
            data_table = self.make_table(name.upper(), linhas, mes, diferencaDias)

            t = Table(data_table, 11 * [0.65 * inch], (linhas + 2) * [0.34 * inch])
            t.setStyle(TableStyle(self.get_table_style(linhas + 1, diferencaDias)))
            
            self.elements.append(t)
            self.elements.append(PageBreak())

    def make_table(self, name, linhas, mes, diferencaDias):
        data_table = [[name]]

        data_table.append(['DATA', 'ENTRADA', 'ASSINATURA', '', '', '', '', '', '', '', 'SAÍDA'])
        
        for i in range(1, linhas + 1, 1):
            if (i % 7 == diferencaDias):
                data_table.append(["{:02d}".format(i) + '/' + "{:02d}".format(mes), ':', 'SÁBADO', '', '', ':', ':', '', '', '', ':'])
            elif (i % 7 == diferencaDias + 1):
                data_table.append(["{:02d}".format(i) + '/' + "{:02d}".format(mes), ':', 'DOMINGO', '', '', ':', ':', '', '', '', ':'])
            else:
                data_table.append(["{:02d}".format(i) + '/' + "{:02d}".format(mes), ':', '', '', '', ':', ':', '', '', '', ':'])

        return data_table

    def get_table_style(self, linhas, diferencaDias):
        table_style = [
            ('ALIGN', (0, 0), (10, linhas), 'CENTER'),
            ('VALIGN', (0, 0), (10, linhas), 'MIDDLE'),
            ('BOX', (0, 0), (10, linhas), 0.25, colors.black),
            ('INNERGRID', (0, 0), (10, linhas), 0.25, colors.black),
            ('SPAN', (0, 0), (10, 0)),
            ('SPAN', (2, 1), (4, 1)),
            ('SPAN', (7, 1), (9, 1))
        ]

        # células grandes para nomes
        for i in range(1, linhas + 1, 1):
            table_style.append(('SPAN', (2, i), (9, i)))
            table_style.append(('SPAN', (7, i), (9, i)))

        # Mudandça de cor para as linhas de sábados de domingos
        for i in range(1, linhas + 1, 1):
            if (i % 7 == diferencaDias + 1 or i % 7 == diferencaDias + 2):
                table_style.append(('BACKGROUND', (0, i), (11, i), colors.gray))

        return table_style

    def build(self):
        self.doc.build(self.elements)
