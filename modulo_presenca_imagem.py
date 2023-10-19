import os
import datetime
import cv2
import numpy as np
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from openpyxl import Workbook
import openpyxl

class ImageChooserApp(App):
    def build(self):
        self.image = Image(source='Imagens/selecione_imagem.png')
        left_column = BoxLayout(orientation='vertical', spacing=10)
        left_column.add_widget(self.image)
        self.file_chooser = FileChooserListView(path=str(os.getcwd()))
        self.file_chooser.bind(on_submit=self.load_image)
        left_column.add_widget(self.file_chooser)

        # Adicione os novos widgets aqui
        self.label_date = Label(text='Data:')
        self.label_text_input1 = Label(text='Curso:')
        self.label_text_input2 = Label(text='Disciplina:')
        data_de_hoje = datetime.datetime.now().strftime('%Y-%m-%d')
        self.date_input = TextInput(hint_text='Data', text=data_de_hoje)
        self.text_input1 = TextInput(hint_text='Curso')
        self.text_input2 = TextInput(hint_text='Disciplina')

        generate_button = Button(text='Gerar Presença')
        close_button = Button(text='Fechar')
        generate_button.bind(on_press=self.generate_presence)
        close_button.bind(on_press=self.close_popup)

        # Adicione os novos widgets à coluna da direita
        right_column = BoxLayout(orientation='vertical', spacing=10)
        right_column.add_widget(self.label_date)
        right_column.add_widget(self.date_input)
        right_column.add_widget(self.label_text_input1)
        right_column.add_widget(self.text_input1)
        right_column.add_widget(self.label_text_input2)
        right_column.add_widget(self.text_input2)
        right_column.add_widget(generate_button)
        right_column.add_widget(close_button)

        layout = BoxLayout(spacing=10)
        layout.add_widget(left_column)
        layout.add_widget(right_column)

        return layout

    def load_image(self, instance, selection, *args):
        value = selection[0]
        if os.path.isfile(value) and value.lower().endswith(('.png', '.jpg', '.jpeg')):
            self.image.source = value
        else:
            self.show_error_popup("Selecione um arquivo de imagem válido.")

    def generate_presence(self, instance):
        data = self.date_input.text
        curso = self.text_input1.text
        disciplina = self.text_input2.text
        filename = f"{curso}_{disciplina}_{data}.xlsx"

        workbook = Workbook()
        sheet = workbook.active

        # Criação das Colunas
        sheet.cell(row=1, column=1, value="Aluno")
        sheet.cell(row=1, column=2, value="Matricula")
        sheet.cell(row=1, column=3, value="Status")

        # Diretório de imagens das pessoas registradas
        people_dir = "Pessoas"

        # Reconhecimento facial (utilize uma biblioteca de reconhecimento facial apropriada)
        recognized_people = self.recognize_people(people_dir)

        # Preencha o Excel com base no reconhecimento facial
        row_index = 2
        for person in recognized_people:
            person = person.replace(".png", "")
            nome_matricula = person.split("_")
            nome = nome_matricula[0]
            matricula = nome_matricula[1]

            sheet.cell(row=row_index, column=1, value=nome)
            sheet.cell(row=row_index, column=2, value=matricula)
            sheet.cell(row=row_index, column=3, value="PRESENTE")
            row_index += 1

        # Defina pessoas ausentes
        all_people = [os.path.splitext(filename)[0] for filename in os.listdir(people_dir)]
        missing_people = list(set(all_people) - set([person[0] for person in recognized_people]))
        for person in missing_people:
            person = person.replace(".png", "")
            nome_matricula = person.split("_")
            nome = nome_matricula[0]
            matricula = nome_matricula[1]
            sheet.cell(row=row_index, column=1, value=nome)
            sheet.cell(row=row_index, column=2, value=matricula)
            sheet.cell(row=row_index, column=3, value="AUSENTE")
            row_index += 1

        # Salvando o arquivo Excel no diretório designado
        app_root_dir = os.path.dirname(os.path.abspath(__file__))
        save_dir = os.path.join(app_root_dir, "ListaPresencas")
        os.makedirs(save_dir, exist_ok=True)  # Cria o diretório se ele não existir

        file_path = os.path.join(save_dir, filename)
        workbook.save(file_path)

        self.show_info_popup(f'Arquivo de presença "{filename}" \nfoi gerado com sucesso na Pasta.')

    def recognize_people(self, people_dir):
        # Implemente o reconhecimento facial aqui e retorne uma lista de pessoas reconhecidas
        recognized_people = []
        # Implemente o reconhecimento facial aqui e adicione as pessoas reconhecidas à lista
        return recognized_people

    def show_error_popup(self, message):
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text=message))
        close_button = Button(text='Fechar')
        content.add_widget(close_button)
        popup = Popup(title='Erro', content=content, auto_dismiss=False, size_hint=(None, None), size=(400, 300))
        close_button.bind(on_release=popup.dismiss)
        popup.open()

    def show_info_popup(self, message):
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text=message))
        close_button = Button(text='Fechar')
        content.add_widget(close_button)
        popup = Popup(title='Informação', content=content, auto_dismiss=False, size_hint=(None, None), size=(400, 300))
        close_button.bind(on_release=popup.dismiss)
        popup.open()

    def close_popup(self, instance):
        App.get_running_app().stop()

if __name__ == '__main__':
    ImageChooserApp().run()
