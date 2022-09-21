import gi

gi.require_version('Gtk', '3.0')

from pdf_gen import PDFGen
from gi.repository import Gtk
from data_model import DataModel
from data_manager import DataManager

class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Gerador de Folha de Pontos")
        self.set_icon_from_file('icone.png')

        self.set_border_width(15)
        self.set_resizable(False)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.data_model = DataModel()
        self.month = 0
        self.day1 = 0
        self.feriados = 0

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        month_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        day1_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        leapyear_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        name_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)

        obs_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        obs_button = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        feriados_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        
        vbox.pack_start(name_box, True, True, 0)
        vbox.pack_start(obs_box, True, True, 0)
        vbox.pack_start(obs_button, True, True, 0)
        vbox.pack_start(month_box, True, True, 0)
        vbox.pack_start(leapyear_box, True, True, 0)
        vbox.pack_start(day1_box, True, True, 0)
        vbox.pack_start(feriados_box, True, True, 0)
        vbox.pack_start(button_box, True, True, 0)

        label_obs = Gtk.Label()
        label_obs.set_markup(
            "<small>"+
                "Obs: Se o campo de Nome ficar em branco, a folha de pontos será\n" +
                "gerada com base no arquivo <b>nomes.csv</b>. Se o campo de Nome for\n" +
                "preenchido, será gerada uma folha de pontos com o nome inserido\n" +
                "no campo." +
            "</small>"
        )
        obs_box.pack_start(label_obs, False, False, True)
        
        label_name = Gtk.Label("Nome do servidor: ")
        name_box.pack_start(label_name, False, False, True)

        self.name_entry = Gtk.Entry()
        name_box.pack_start(self.name_entry, True, True, 0)

        label_month = Gtk.Label("Mês da folha:* ")
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

        self.label_leapyear = Gtk.Label("Ano bissexto? ")
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

        label_feriados = Gtk.Label("Feriados do mês: ")
        feriados_box.pack_start(label_feriados, False, False, True)
        
        self.feriados_entry = Gtk.Entry()
        feriados_box.pack_start(self.feriados_entry, True, True, 0)

        button = Gtk.Button.new_with_label("Gerar Folha de Pontos")
        button.connect("clicked", self.create_pdf)
        button_box.pack_start(button, True, True, 0)

        self.add(vbox)

    def on_month_combo_changed(self, combo):
        self.month = combo.get_active()

        if(self.month == 1): # habilitar e desabilitar checkbox de bissexto
            self.check_leapyear.set_sensitive(True)
            self.label_leapyear.set_sensitive(True)
        else:
            self.check_leapyear.set_sensitive(False)
            self.label_leapyear.set_sensitive(False)

    def on_day1_combo_changed(self, combo):
        self.day1 = combo.get_active()

    def create_pdf(self, button):
        self.data_model.name = self.name_entry.get_text().strip()
        self.data_model.month = self.month
        self.data_model.is_leapyear = self.check_leapyear.get_active()
        self.data_model.day1 = self.day1
        self.data_model.feriados = self.feriados_entry.get_text().replace(' ', '').split(',')
        
        if(self.validate()):
            data_manager = DataManager()

            qtdDiasMes = [
                31, 28, 31, 30, 31, 30,
                31, 31, 30, 31, 30, 31
            ]

            doc = PDFGen()
            if(self.data_model.name == ""):
                if(self.data_model.is_leapyear == False):
                    doc.criarNovoDocumento(qtdDiasMes[self.data_model.month], self.data_model.month, self.data_model.day1, data_manager.get_names(), self.data_model.feriados)
                elif(self.data_model.is_leapyear == True and self.data_model.month == 1):
                    doc.criarNovoDocumento(qtdDiasMes[self.data_model.month]+1, self.data_model.month, self.data_model.day1, data_manager.get_names(), self.data_model.feriados)
            else:
                if(self.data_model.is_leapyear == False):
                    doc.criarNovoDocumento(qtdDiasMes[self.data_model.month], self.data_model.month, self.data_model.day1, self.data_model.name, self.data_model.feriados)
                elif(self.data_model.is_leapyear == True and self.data_model.month == 1):
                    doc.criarNovoDocumento(qtdDiasMes[self.data_model.month]+1, self.data_model.month, self.data_model.day1, self.data_model.name, self.data_model.feriados)
            
            doc.build()

            win = MessageDialogWindow("Folha de Pontos Gerada!")
            win.connect("destroy", Gtk.main_quit)
            win.show_all()
            Gtk.main()
        else:
            win = MessageDialogWindow("Dados Inválidos! Tente Novamente.\n\nObservação:\n\t- Campo de Mês é obrigatório;\n\t- Campo de Dia é obrigatório")
            win.connect("destroy", Gtk.main_quit)
            win.show_all()
            Gtk.main()

    def validate(self):
        if(self.data_model.month != '' and self.data_model.day1 != ''):
            return True
        else:
            return False

class MessageDialogWindow(Gtk.Window):
    def __init__(self, text):
        Gtk.Window.__init__(self, title="Aviso")

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)

        self.add(box)
        self.set_default_size(500, 100)
        self.set_position(Gtk.WindowPosition.CENTER)

        label = Gtk.Label(text)
        label.set_hexpand(True)
        box.pack_start(label, False, False, True)
