import json
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

import face_recognition

class CapturaPresencaImagem(App):
    def build(self):
        self.title = 'Instituto Federal Fluminense - Gerar Presença por Imagem'
        self.icon = 'Imagens/icone_camera.png'
        self.image = Image(source='Imagens/selecione_imagem.png')

        try:
            with open("Configuracoes/config.txt", "r") as config_file:
                config = json.load(config_file)
                # select_cam = config.get("select_cam", "")
                select_matricula = config.get("select_matricula", "")
                select_disciplina = config.get("select_disciplina", "")
                select_curso = config.get("select_curso", "")
        except FileNotFoundError:
            pass

        left_column = BoxLayout(orientation='vertical', spacing=10)
        left_column.add_widget(self.image)
        self.file_chooser = FileChooserListView(path=str("ImagensParaPresenca")) # Pasta que vai abrir como default
        self.file_chooser.bind(on_submit=self.load_image)
        left_column.add_widget(self.file_chooser)

        # Adicione os novos widgets aqui
        self.label_date = Label(text='Data:')
        self.label_text_input1 = Label(text='Curso:')
        self.label_text_input2 = Label(text='Disciplina:')
        data_de_hoje = datetime.datetime.now().strftime('%Y-%m-%d')
        self.date_input = TextInput(hint_text='Data', text=data_de_hoje)
        self.text_input1 = TextInput(hint_text='Curso', text=select_curso)
        self.text_input2 = TextInput(hint_text='Disciplina', text=select_disciplina)

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

        # Carregar imagens das pessoas registradas
        known_faces, known_names = self.load_known_faces(people_dir)

        # Define todas as pessoas como "AUSENTE" inicialmente para preenchimento
        all_people = [os.path.splitext(filename)[0] for filename in os.listdir(people_dir)]
        row_index = 2

        # Faces reconhecidas na imagem selecionada
        recognized_people = self.get_pessoas_presentes(self.image.source, known_faces, known_names)

        for person in all_people:
            person = person.replace(".png", "")
            nome_matricula = person.split("_")
            nome = nome_matricula[0]
            matricula = nome_matricula[1]

            # Verificar se a pessoa está presente e definir o valor correspondente
            if person in recognized_people:
                status = "PRESENTE"
            else:
                status = "AUSENTE"

            sheet.cell(row=row_index, column=1, value=nome)
            sheet.cell(row=row_index, column=2, value=matricula)
            sheet.cell(row=row_index, column=3, value=status)
            row_index += 1

        # Salvando o arquivo Excel no diretório designado
        app_root_dir = os.path.dirname(os.path.abspath(__file__))
        save_dir = os.path.join(app_root_dir, "PresencasCapturadas")
        os.makedirs(save_dir, exist_ok=True)  # Crie o diretório se ele não existir

        file_path = os.path.join(save_dir, filename)
        workbook.save(file_path)

        self.show_info_popup(f'Arquivo de presença "{filename}" \nfoi gerado com sucesso na Pasta.')

    def load_known_faces(self, people_dir):
        known_faces = []
        known_names = []

        for person_filename in os.listdir(people_dir):
            person_path = os.path.join(people_dir, person_filename)
            if person_filename.endswith(('.png', '.jpg', '.jpeg')):
                image = face_recognition.load_image_file(person_path)
                encoding = face_recognition.face_encodings(image)[0]  # Assumindo um único rosto na imagem
                known_faces.append(encoding)
                known_names.append(os.path.splitext(person_filename)[0])

        return known_faces, known_names

    def get_pessoas_presentes(self, image_path, known_faces, known_names):
        # Carregue a imagem selecionada
        image = face_recognition.load_image_file(image_path)

        # Encontre rostos na imagem
        face_locations = face_recognition.face_locations(image)
        face_encodings = face_recognition.face_encodings(image, face_locations)

        recognized_people = []

        for face_encoding in face_encodings:
            # Compare a face com as imagens das pessoas registradas
            matches = face_recognition.compare_faces(known_faces, face_encoding)
            if any(matches):
                face_index = matches.index(True)
                person_name = known_names[face_index]
                recognized_people.append(person_name)

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
        popup = Popup(title='Informação', content=content, auto_dismiss=False, size_hint=(None, None), size=(600, 300))
        close_button.bind(on_release=popup.dismiss)
        popup.open()

    def close_popup(self, instance):
        App.get_running_app().stop()


if __name__ == '__main__':
    CapturaPresencaImagem().run()
