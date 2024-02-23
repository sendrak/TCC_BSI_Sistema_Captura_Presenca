import json

import cv2
import face_recognition
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from datetime import datetime
from openpyxl import Workbook
import os

from openpyxl.reader.excel import load_workbook


class CapturaPresencaVideo(App):
    def build(self):
        self.title = 'Instituto Federal Fluminense - Captura de Presença'
        self.icon = 'Imagens/icone_camera.png'

        try:
            with open("Configuracoes/config.txt", "r") as config_file:
                config = json.load(config_file)
                # select_cam = config.get("select_cam", "")
                select_matricula = config.get("select_matricula", "")
                select_disciplina = config.get("select_disciplina", "")
                select_curso = config.get("select_curso", "")
        except FileNotFoundError:
            pass

        # Layout principal com duas colunas
        layout = BoxLayout(orientation='horizontal', spacing=10)

        # Coluna 1: Visualização da câmera e captura
        col1_layout = BoxLayout(orientation='vertical', spacing=10)

        # Adicionando 'no_camera' como imagem padrão
        self.camera = Image(source='Imagens/no_camera.png', allow_stretch=True)
        col1_layout.add_widget(self.camera)

        # Temporizador
        self.timer_label = Label(text="Tempo restante: 10:00")
        col1_layout.add_widget(self.timer_label)

        layout.add_widget(col1_layout)

        # Coluna 2: Campos de texto e botões
        col2_layout = BoxLayout(orientation='vertical', spacing=10)

        label_date = Label(text='Data:')
        label_text_input1 = Label(text='Curso:')
        label_text_input2 = Label(text='Disciplina:')

        data_de_hoje = datetime.now().strftime('%Y-%m-%d')
        date_input = TextInput(hint_text='Data', text=data_de_hoje)

        text_input1 = TextInput(hint_text='Curso', text=select_curso)
        text_input2 = TextInput(hint_text='Disciplina', text=select_disciplina)

        start_button = Button(text='Iniciar Captura de Presença')
        start_button.bind(on_press=self.inicia_processo_presenca)

        close_button = Button(text='Fechar')
        close_button.bind(on_press=self.close_app)

        col2_layout.add_widget(label_date)
        col2_layout.add_widget(date_input)
        col2_layout.add_widget(label_text_input1)
        col2_layout.add_widget(text_input1)
        col2_layout.add_widget(label_text_input2)
        col2_layout.add_widget(text_input2)

        # Campo para definir o tempo do temporizador
        self.timer_input = TextInput(hint_text='Tempo (segundos)', input_filter='int')
        self.timer_input.text = '600'  # Valor padrão: 10 minutos em segundos
        label_timer_input = Label(text='Defina o tempo de captura em segundos:')
        col2_layout.add_widget(label_timer_input)
        col2_layout.add_widget(self.timer_input)

        col2_layout.add_widget(start_button)
        col2_layout.add_widget(close_button)

        layout.add_widget(col2_layout)

        self.capture = cv2.VideoCapture(0)
        self.known_faces = []
        self.known_names = []
        self.detected_people = {}
        self.timer = None
        self.remaining_time = 600  # 10 minutos em segundos
        self.mostrar_popup = True  # Atributo para rastrear se o popup foi mostrado
        self.is_capturing = False  # Atributo para controlar a captura em andamento

        Clock.schedule_interval(self.update, 0 / 30.0)  # Mais próximo de zero aumenta a taxa de atualização

        self.date_input = date_input
        self.text_input1 = text_input1
        self.text_input2 = text_input2

        return layout

    def inicia_processo_presenca(self, instance):
        self.lista_presenca = []
        user_time_input = int(self.timer_input.text)
        if user_time_input <= 0:
            print("O tempo deve ser um valor inteiro maior que zero")
            return

        # Verificar se a câmera foi aberta com sucesso
        if not self.capture.isOpened():
            print("Erro ao abrir a câmera.")
            return

        if not self.is_capturing:
            self.is_capturing = True
            self.mostrar_popup = True  # Redefinir o popup mostrado

            self.remaining_time = user_time_input
            self.timer_label.text = f"Tempo restante: {user_time_input // 60:02}:{user_time_input % 60:02}"

            if self.timer is None:
                self.timer = Clock.schedule_interval(self.update_timer, 1)

            # Verifica se o arquivo Excel já existe
            data = self.date_input.text
            curso = self.text_input1.text
            disciplina = self.text_input2.text
            filename = f"{curso}_{disciplina}_{data}.xlsx"
            file_path = os.path.join("PresencasCapturadas", filename)

            if not os.path.exists(file_path):
                # Se o arquivo não existe, cria e preenche
                self.cria_excel(None)
            else:
                # Se o arquivo existe, apenas inicia a captura
                print("Captura de presença iniciada, a captura será finalizada ao fim do temporizador")

    def stop_capturing(self):
        self.is_capturing = False
        self.capture.release()
        # Exibe a imagem 'no_camera' ao finalizar a captura
        self.camera.source = 'Imagens/no_camera.png'

    def update(self, dt):
        if self.is_capturing:
            ret, frame = self.capture.read()
            if ret:
                face_locations = face_recognition.face_locations(frame)
                face_encodings = face_recognition.face_encodings(frame, face_locations)
                newly_detected_people = set()

                for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                    matches = face_recognition.compare_faces(self.known_faces, face_encoding)
                    if any(matches):
                        face_index = matches.index(True)
                        person_name = self.known_names[face_index]
                        newly_detected_people.add(person_name)
                        if person_name not in self.detected_people:
                            print(f"Face reconhecida na câmera: {person_name}")
                            self.montagem_presenca(person_name)
                        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                    else:
                        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                exited_people = set(self.detected_people.keys()) - newly_detected_people
                for person_name in exited_people:
                    print(f"{person_name} saiu do alcance da câmera")

                self.detected_people = {person_name: (top, right, bottom, left) for
                                        (top, right, bottom, left), person_name
                                        in zip(face_locations, newly_detected_people)}

                buffer = cv2.flip(frame, 0).tobytes()
                texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
                texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
                self.camera.texture = texture
            else:
                self.camera.source = 'Imagens/no_camera.png'

    def montagem_presenca(self, nome_matricula):
        nome, _ = nome_matricula.split("_", 1)
        if nome not in self.lista_presenca:
            self.lista_presenca.append(nome_matricula)
            print(f"{nome_matricula} adicionado na lista de presença")
        else:
            print(f"{nome_matricula} já está na lista de presença")

    def update_timer(self, dt):
        if self.remaining_time > 0:
            self.remaining_time -= 1
            minutes = self.remaining_time // 60
            seconds = self.remaining_time % 60
            self.timer_label.text = f"Tempo restante: {minutes:02}:{seconds:02}"
        elif self.mostrar_popup is True:
            self.timer_label.text = "Tempo esgotado, presença finalizada"
            self.popup_finaliza_tempo()
            self.stop_capturing()  # Pare a captura quando o tempo se esgotar

            # Adicione a chamada para a função de atualização do Excel aqui
            self.atualiza_excel()

    def popup_finaliza_tempo(self):
        self.mostrar_popup = False  # Marcar o popup como mostrado para evitar múltiplas chamadas
        message = "Tempo esgotado, presença finalizada"

        box_popup = BoxLayout(orientation='vertical')
        box_popup.add_widget(Label(text=message))
        close_button = Button(text='Fechar')
        box_popup.add_widget(close_button)

        popup = Popup(title='Tempo de Presença Esgotado', content=box_popup, size_hint=(0.5, 0.5))

        close_button.bind(on_release=popup.dismiss)
        popup.open()

    def atualiza_excel(self):
        print("Função de atualização do Excel chamada")

        # Diretório do arquivo Excel
        data = self.date_input.text
        curso = self.text_input1.text
        disciplina = self.text_input2.text
        filename = f"{curso}_{disciplina}_{data}.xlsx"
        file_path = os.path.join("PresencasCapturadas", filename)

        # Carrega o arquivo Excel existente
        workbook = load_workbook(file_path)
        sheet = workbook.active

        # Preenche 'PRESENTE' para as pessoas encontradas durante a captura
        for nome in self.lista_presenca:
            if nome in self.known_names:
                row_index = self.known_names.index(nome) + 2
                sheet.cell(row=row_index, column=3, value="PRESENTE")

        # Salva as alterações no arquivo Excel
        workbook.save(file_path)

    def cria_excel(self, instance):
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
        self.known_faces, self.known_names = self.load_known_faces(people_dir)

        # Define todas as pessoas como "AUSENTE" inicialmente para preenchimento
        all_people = [os.path.splitext(filename)[0] for filename in os.listdir(people_dir)]
        row_index = 2

        for person in all_people:
            person = person.replace(".png", "")
            nome_matricula = person.split("_")
            nome = nome_matricula[0]
            matricula = nome_matricula[1]
            status = "AUSENTE"  # Definindo todas as pessoas

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

    def load_known_faces(self, people_dir):
        known_faces = []
        known_names = []

        for filename in os.listdir(people_dir):
            if filename.endswith(".png"):
                path = os.path.join(people_dir, filename)
                image = face_recognition.load_image_file(path)
                encoding = face_recognition.face_encodings(image)[0]
                known_faces.append(encoding)
                known_names.append(os.path.splitext(filename)[0])

        return known_faces, known_names

    def close_app(self, instance):
        print("Clicou Fechar App")
        App.get_running_app().stop()


if __name__ == '__main__':
    CapturaPresencaVideo().run()
