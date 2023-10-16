import cv2
import face_recognition
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.graphics.texture import Texture
from kivy.clock import Clock
from datetime import datetime

class PresenceCaptureApp(App):
    def build(self):
        # Layout principal com duas colunas
        layout = BoxLayout(orientation='horizontal', spacing=10)

        # Coluna 1: Visualização da câmera e captura
        self.camera = Image()
        layout.add_widget(self.camera)

        # Coluna 2: Campos de texto e botões
        col2_layout = BoxLayout(orientation='vertical', spacing=10)

        # Labels para as opções na coluna à direita
        label_date = Label(text='Data:')
        label_text_input1 = Label(text='Curso:')
        label_text_input2 = Label(text='Disciplina:')

        # Data de Hoje dinâmicamente do sistema, pode ser alterada como texto
        data_de_hoje = datetime.now().strftime('%Y-%m-d')
        date_input = TextInput(hint_text='Data', text=data_de_hoje)

        # Campos de texto existentes
        text_input1 = TextInput(hint_text='Curso')
        text_input2 = TextInput(hint_text='Disciplina')

        # Botão Iniciar Captura de Presença
        start_button = Button(text='Iniciar Captura de Presença')
        start_button.bind(on_press=self.start_capture)

        # Botão Fechar Presença
        close_button = Button(text='Fechar Presença')
        close_button.bind(on_press=self.close_presence)

        # Adição dos widgets à coluna 2
        col2_layout.add_widget(label_date)
        col2_layout.add_widget(date_input)
        col2_layout.add_widget(label_text_input1)
        col2_layout.add_widget(text_input1)
        col2_layout.add_widget(label_text_input2)
        col2_layout.add_widget(text_input2)
        col2_layout.add_widget(start_button)
        col2_layout.add_widget(close_button)

        # Adicionar coluna 2 ao layout principal
        layout.add_widget(col2_layout)

        # Inicialize as variáveis relacionadas à detecção de rostos
        self.capture = cv2.VideoCapture(0)
        self.known_faces = []  # Lista de rostos conhecidos
        self.known_names = []  # Lista de nomes correspondentes aos rostos conhecidos
        self.detected_people = {}  # Dicionário para rastrear as pessoas detectadas

        # Inicie o temporizador para chamar a função de atualização periodicamente
        Clock.schedule_interval(self.update, 0 / 30.0)  # 30 FPS

        return layout

    def start_capture(self, instance):
        # Lógica para iniciar a captura de presença
        print("Iniciar captura clicado")

    def close_presence(self, instance):
        # Lógica para fechar a presença
        self.capture.release()
        cv2.destroyAllWindows()
        PresenceCaptureApp.stop(self)

    def update(self, dt):
        # Função de atualização chamada periodicamente para processar quadros da câmera
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

            # Atualize a textura da câmera existente
            buffer = cv2.flip(frame, 0).tobytes()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
            self.camera.texture = texture
        else:
            self.camera.source = 'Imagens/no_camera.png'

if __name__ == '__main__':
    PresenceCaptureApp().run()
