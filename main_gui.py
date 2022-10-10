import gi

gi.require_version('Gtk', '3.0')

from pdf_gen import PDFGen
from gi.repository import Gtk
from data_model import DataModel
from data_manager import DataManager

class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Gerador de Folha de Pontos")
        #self.set_icon_from_file('iconeGFP.png')

        self.set_border_width(15)
        self.set_resizable(False)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.data_model = DataModel()

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        
        name_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        texto_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        nomesArquivo_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        month_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        leapyear_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        day1_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        feriados_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        texto_box2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        
        vbox.pack_start(nomesArquivo_box, True, True, 0)
        vbox.pack_start(name_box, True, True, 0)
        vbox.pack_start(texto_box, True, True, 0)
        vbox.pack_start(month_box, True, True, 0)
        vbox.pack_start(leapyear_box, True, True, 0)
        vbox.pack_start(day1_box, True, True, 0)
        vbox.pack_start(feriados_box, True, True, 0)
        vbox.pack_start(texto_box2, True, True, 0)
        vbox.pack_start(button_box, True, True, 0)
        
        self.label_nomesArquico = Gtk.Label()
        self.label_nomesArquico.set_markup("Importar nomes do arquivo <b>nomes.csv</b>?")
        nomesArquivo_box.pack_start(self.label_nomesArquico, False, False, True)

        self.check_nomesAquivo = Gtk.CheckButton()
        self.check_nomesAquivo.connect("toggled", self.desabilitarCampoNome)
        nomesArquivo_box.pack_start(self.check_nomesAquivo, False, False, True)

        self.label_name = Gtk.Label("Nome do Servidor: ")
        self.label_name.set_sensitive(True)
        name_box.pack_start(self.label_name, False, False, True)

        self.name_entry = Gtk.Entry()
        self.name_entry.set_sensitive(True)
        name_box.pack_start(self.name_entry, True, True, 0)

        self.label_texto = Gtk.Label()
        self.label_texto.set_markup(
            "<small>" +
                "<i>Obs: Se o campo de <b>Nome do Servidor</b> for preenchido, será gerada\n" +
                "uma única página de folha de pontos correspondente ao nome do\n" +
                "servidor inserido no campo.</i>" +
            "</small>"
        )
        self.label_texto.set_sensitive(True)
        texto_box.pack_start(self.label_texto, False, False, True)

        label_month = Gtk.Label("Mês da Folha:* ")
        month_box.pack_start(label_month, False, False, True)

        month_combo = Gtk.ComboBoxText()
        month_combo.connect("changed", self.on_month_combo_changed)
        month_combo.set_entry_text_column(0)
        
        mesesAno = [
            "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
            "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
        ]

        for month in mesesAno:
            month_combo.append_text(str(month))

        month_box.pack_start(month_combo, False, False, True)

        self.label_leapyear = Gtk.Label("O ano é bissexto? ")
        self.label_leapyear.set_sensitive(False)
        leapyear_box.pack_start(self.label_leapyear, False, False, True)

        self.check_leapyear = Gtk.CheckButton()
        self.check_leapyear.set_sensitive(False)
        leapyear_box.pack_start(self.check_leapyear, False, False, True)

        label_day1 = Gtk.Label("O primeiro dia do mês será numa:* ")
        day1_box.pack_start(label_day1, False, False, 0)

        days = [
            "Segunda-feira", "Terça-feira", "Quarta-feira",
            "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"
        ]

        day1_combo = Gtk.ComboBoxText()
        day1_combo.connect("changed", self.on_day1_combo_changed)
        day1_combo.set_entry_text_column(0)

        for day in days:
            day1_combo.append_text(day)

        day1_box.pack_start(day1_combo, False, False, 0)

        label_feriados = Gtk.Label("Feriados do Mês: ")
        feriados_box.pack_start(label_feriados, False, False, True)
        
        self.feriados_entry = Gtk.Entry()
        feriados_box.pack_start(self.feriados_entry, True, True, 0)

        label_texto2 = Gtk.Label()
        label_texto2.set_markup(
            "<small>" +
                "<i>Obs: Informe os dias feriados separados por vírgula. <b>Ex: 5, 12, 31...</b></i>" +
            "</small>"
        )
        texto_box2.pack_start(label_texto2, False, False, True)

        button = Gtk.Button.new_with_label("Gerar Folha de Pontos")
        button.connect("clicked", self.create_pdf)
        button_box.pack_start(button, True, True, 0)

        self.add(vbox)

    def desabilitarCampoNome(self, checkbutton):
        if checkbutton.get_active():
            self.label_name.set_sensitive(False)
            self.name_entry.set_sensitive(False)
            self.label_texto.set_sensitive(False)
        else:
            self.label_name.set_sensitive(True)
            self.name_entry.set_sensitive(True)
            self.label_texto.set_sensitive(True)

    def on_month_combo_changed(self, combo):  # habilitar e desabilitar checkbox de bissexto
        self.month = combo.get_active()

        if(self.month == 1):
            self.check_leapyear.set_sensitive(True)
            self.label_leapyear.set_sensitive(True)
        else:
            self.check_leapyear.set_sensitive(False)
            self.label_leapyear.set_sensitive(False)

    def on_day1_combo_changed(self, combo):
        self.day1 = combo.get_active()

    def create_pdf(self, button):
        self.data_model.nomesArquivo = self.check_nomesAquivo.get_active()
        self.data_model.name = self.name_entry.get_text().strip()
        self.data_model.month = self.month
        self.data_model.is_leapyear = self.check_leapyear.get_active()
        self.data_model.day1 = self.day1
        self.data_model.feriados = self.feriados_entry.get_text().replace(' ', '').split(',')
        
        if(self.validate()):
            data_manager = DataManager()

            qtdDiasMes = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

            doc = PDFGen()
            
            if(self.data_model.nomesArquivo == True):
                if(self.data_model.is_leapyear == False):
                    doc.criarNovoDocumento(qtdDiasMes[self.data_model.month], self.data_model.month, self.data_model.day1, data_manager.get_names(), self.data_model.feriados)
                elif(self.data_model.is_leapyear == True and self.data_model.month == 1):
                    doc.criarNovoDocumento(qtdDiasMes[self.data_model.month]+1, self.data_model.month, self.data_model.day1, data_manager.get_names(), self.data_model.feriados)
            elif(self.data_model.nomesArquivo == False and self.data_model.name != ''):
                if(self.data_model.is_leapyear == False):
                    doc.criarNovoDocumento(qtdDiasMes[self.data_model.month], self.data_model.month, self.data_model.day1, self.data_model.name, self.data_model.feriados)
                elif(self.data_model.is_leapyear == True and self.data_model.month == 1):
                    doc.criarNovoDocumento(qtdDiasMes[self.data_model.month]+1, self.data_model.month, self.data_model.day1, self.data_model.name, self.data_model.feriados)
            
            doc.build()

            win = MessageDialogWindow(
                "\tFolha de Pontos Gerada!" +
                "\n\nO arquivo foi salvo na pasta PDFs.")
            win.connect("destroy", Gtk.main_quit)
            win.show_all()
            Gtk.main()
        else:
            win = MessageDialogWindow(
                "Dados Inválidos! Tente Novamente.\n\n" +
                "Observação:\n" +
                    "\t- Opção de Nome(s) é obrigatório;\n" +
                    "\t- Campo de Mês é obrigatório;\n" +
                    "\t- Campo de Dia é obrigatório.")
            win.connect("destroy", Gtk.main_quit)
            win.show_all()
            Gtk.main()

    def validate(self):
        if(self.data_model.month == '' or self.data_model.day1 == '' or (self.data_model.nomesArquivo == False and self.data_model.name == '')):
            return False
        else:
            return True

class MessageDialogWindow(Gtk.Window):
    def __init__(self, text):
        Gtk.Window.__init__(self, title="Aviso")

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)

        self.add(box)
        self.set_default_size(300, 125)
        self.set_position(Gtk.WindowPosition.CENTER)

        label = Gtk.Label(text)
        label.set_hexpand(True)
        box.pack_start(label, False, False, True)
