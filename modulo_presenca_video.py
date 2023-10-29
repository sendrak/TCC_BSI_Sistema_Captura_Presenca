import cv2
import face_recognition
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.graphics.texture import Texture
from kivy.clock import Clock
from datetime import datetime
from openpyxl import Workbook, load_workbook
import os

class CapturaPresencaVideo(App):
    def build(self):
        self.title = 'Instituto Federal Fluminense - Captura de Presença'
        self.icon = 'Imagens/icone_camera.png'

        # Layout principal com duas colunas
        layout = BoxLayout(orientation='horizontal', spacing=10)

        # Coluna 1: Visualização da câmera e captura
        col1_layout = BoxLayout(orientation='vertical', spacing=10)

        self.camera = Image()
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

        text_input1 = TextInput(hint_text='Curso')
        text_input2 = TextInput(hint_text='Disciplina')

        start_button = Button(text='Iniciar Captura de Presença')
        start_button.bind(on_press=self.inicia_presenca)

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
        self.popup_shown = False  # Atributo para rastrear se o popup foi mostrado
        self.is_capturing = False  # Atributo para controlar a captura em andamento

        Clock.schedule_interval(self.update, 0 / 30.0)  # 30 FPS

        self.date_input = date_input
        self.text_input1 = text_input1
        self.text_input2 = text_input2

        return layout

    def inicia_presenca(self, instance):
        user_time_input = int(self.timer_input.text)
        if user_time_input <= 0:
            print("O tempo deve ser um valor inteiro maior que zero")
            return

        if not self.is_capturing:
            self.is_capturing = True
            self.popup_shown = False  # Redefinir o popup mostrado

            self.remaining_time = user_time_input
            self.timer_label.text = f"Tempo restante: {user_time_input // 60:02}:{user_time_input % 60:02}"

            if self.timer is None:
                self.timer = Clock.schedule_interval(self.update_timer, 1)
            print("Captura de presença iniciada, a captura será finalizada ao fim do temporizador")

    def close_app(self, instance):
        App.get_running_app().stop()

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
                        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                    else:
                        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                exited_people = set(self.detected_people.keys()) - newly_detected_people
                for person_name in exited_people:
                    print(f"{person_name} saiu do alcance da câmera")

                self.detected_people = {person_name: (top, right, bottom, left) for (top, right, bottom, left), person_name
                                        in zip(face_locations, newly_detected_people)}

                buffer = cv2.flip(frame, 0).tobytes()
                texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
                texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
                self.camera.texture = texture
            else:
                self.camera.source = 'Imagens/no_camera.png'

    def update_timer(self, dt):
        if self.remaining_time > 0:
            self.remaining_time -= 1
            minutes = self.remaining_time // 60
            seconds = self.remaining_time % 60
            self.timer_label.text = f"Tempo restante: {minutes:02}:{seconds:02}"
        elif not self.popup_shown:
            self.timer_label.text = "Tempo esgotado, presença finalizada"
            self.popup_finaliza_tempo()

    def popup_finaliza_tempo(self):
        self.popup_shown = True  # Marcar o popup como mostrado para evitar múltiplas chamadas
        message = "Tempo esgotado, presença finalizada"

        box_popup = BoxLayout(orientation='vertical')
        box_popup.add_widget(Label(text=message))
        close_button = Button(text='Fechar')
        box_popup.add_widget(close_button)

        popup = Popup(title='Tempo de Presença Esgotado', content=box_popup, size_hint=(0.5, 0.5))

        close_button.bind(on_release=popup.dismiss)
        popup.open()

if __name__ == '__main__':
    CapturaPresencaVideo().run()
