import gi

gi.require_version('Gtk', '3.0')

from pdf_gen import PDFGen
from gi.repository import Gtk
from data_model import DataModel
from data_manager import DataManager

class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Gerador de Folha de Pontos")

        self.set_border_width(15)
        self.set_resizable(False)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.data_model = DataModel()
        self.month = 0
        self.day1 = 0

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        month_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        day1_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        leapyear_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        name_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)

        vbox.pack_start(name_box, True, True, 0)
        vbox.pack_start(month_box, True, True, 0)
        vbox.pack_start(leapyear_box, True, True, 0)
        vbox.pack_start(day1_box, True, True, 0)
        vbox.pack_start(button_box, True, True, 0)

        label_name = Gtk.Label("Nome do servidor: ")
        name_box.pack_start(label_name, False, False, True)

        self.name_entry = Gtk.Entry()
        self.name_entry.set_text("Insira um nome...")
        name_box.pack_start(self.name_entry, True, True, 0)

        label_month = Gtk.Label("Mês da folha: ")
        month_box.pack_start(label_month, False, False, True)

        month_combo = Gtk.ComboBoxText()
        month_combo.connect("changed", self.on_month_combo_changed)
        month_combo.set_entry_text_column(0)
        
        mesesAno = ["", "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]

        for month in range(1, 14, 1):
            month_combo.append_text(str(mesesAno[month-1]))

        month_box.pack_start(month_combo, False, False, True)

        self.label_leapyear = Gtk.Label("Ano bissexto? ")
        self.label_leapyear.set_sensitive(False)
        leapyear_box.pack_start(self.label_leapyear, False, False, True)

        self.check_leapyear = Gtk.CheckButton()
        self.check_leapyear.set_sensitive(False)
        leapyear_box.pack_start(self.check_leapyear, False, False, True)

        label_day1 = Gtk.Label("O primeiro dia do mês será numa: ")
        day1_box.pack_start(label_day1, False, False, 0)

        days = ["", "Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"]
        day1_combo = Gtk.ComboBoxText()
        day1_combo.connect("changed", self.on_day1_combo_changed)
        day1_combo.set_entry_text_column(0)
        
        for day in days:
            day1_combo.append_text(day)

        day1_box.pack_start(day1_combo, False, False, 0)

        button = Gtk.Button.new_with_label("Gerar Folha de Pontos")
        button.connect("clicked", self.create_pdf)
        button_box.pack_start(button, True, True, 0)

        self.add(vbox)

    def on_month_combo_changed(self, combo):
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
        self.data_model.name = self.name_entry.get_text().strip()
        self.data_model.month = self.month
        self.data_model.is_leapyear = self.check_leapyear.get_active()
        self.data_model.day1 = self.day1

        if(self.validate()):
            data_manager = DataManager()

            doc = PDFGen()
            doc.create_new_document(31, 6, 2, data_manager.get_names())
            doc.build()

            win = MessageDialogWindow("Folha de Pontos Gerada!")
            win.connect("destroy", Gtk.main_quit)
            win.show_all()
            Gtk.main()
        else:
            win = MessageDialogWindow("Dados Inválidos! Tente Novamente.")
            win.connect("destroy", Gtk.main_quit)
            win.show_all()
            Gtk.main()

    def validate(self):
        if (self.data_model.name and self.data_model.month and self.data_model.day1):
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
