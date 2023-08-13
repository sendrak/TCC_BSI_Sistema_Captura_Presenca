from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.clock import Clock
import cv2
from kivy.graphics.texture import Texture
import face_recognition
import os

# Widget personalizado para exibir a imagem da câmera
class CameraLabel(BoxLayout):
    def __init__(self, camera_index, known_faces, known_names, log_label, **kwargs):
        super().__init__(**kwargs)
        self.camera_index = camera_index
        self.known_faces = known_faces  # Lista de faces conhecidas
        self.known_names = known_names  # Lista de nomes correspondentes
        self.log_label = log_label

        self.capture = cv2.VideoCapture(camera_index)
        self.image = Image(source='Imagens/no_camera.png')
        self.add_widget(self.image)

        Clock.schedule_interval(self.update, 0/30.0)  # Atualiza os frames em 1/30 segundos mais próximo de zero maior desempenho

    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            buffer = cv2.flip(frame, 0).tobytes()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')

            # Realize o reconhecimento facial no frame capturado
            face_locations = face_recognition.face_locations(frame)
            face_encodings = face_recognition.face_encodings(frame, face_locations)

            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                matches = face_recognition.compare_faces(self.known_faces, face_encoding)
                if any(matches):
                    face_index = matches.index(True)
                    person_name = self.known_names[face_index]
                    self.log_label.text = f"Face reconhecida: {person_name}"
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                else:
                    self.log_label.text = "Não existe face reconhecida"
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            self.image.texture = texture
        else:
            self.image.source = 'Imagens/no_camera.png'

    def on_stop(self):
        self.capture.release()


class CamerasApp(App):
    def build(self):
        # Configurações da Janela
        self.title = 'Monitoramento Multicamera'
        self.icon = 'Imagens/icone_camera.png'
        Window.maximize()

        # Lista de faces conhecidas
        known_faces = []
        known_names = []

        # Caminho para o Banco de Faces
        known_faces_folder = "Pessoas"

        # Percorra a pasta e calcule as representações faciais para cada imagem
        for filename in os.listdir(known_faces_folder):
            if filename.endswith(".jpg") or filename.endswith(".png"):
                image_path = os.path.join(known_faces_folder, filename)
                face_image = face_recognition.load_image_file(image_path)
                face_encoding = face_recognition.face_encodings(face_image)[0]
                known_faces.append(face_encoding)
                person_name = os.path.splitext(filename)[0]
                known_names.append(person_name)

        # Layout principal com três colunas
        main_layout = BoxLayout(orientation='horizontal', spacing=10)

        # Layout secundário para a coluna de câmeras à esquerda
        cameras_layout = BoxLayout(orientation='vertical', spacing=10)

        # Layout secundário para a primeira linha de câmeras
        first_column_layout = BoxLayout(orientation='horizontal', spacing=10)

        # Label de logs
        self.log_label = Label(text='', size_hint_y=None, height=30)
        first_column_layout.add_widget(self.log_label)

        # Adicionar as labels das câmeras para a primeira linha
        for camera_index in range(2):
            first_column_layout.add_widget(CameraLabel(camera_index, known_faces, known_names, self.log_label))

        cameras_layout.add_widget(first_column_layout)

        # Layout secundário para a segunda linha de câmeras
        second_column_layout = BoxLayout(orientation='horizontal', spacing=10)

        # Adicionar as labels das câmeras para a segunda linha
        for camera_index in range(2, 4):  # Altere para o número correto de câmeras na segunda linha
            second_column_layout.add_widget(CameraLabel(camera_index, known_faces, known_names, self.log_label))

        cameras_layout.add_widget(second_column_layout)

        main_layout.add_widget(cameras_layout)

        # Layout secundário para a coluna de botões à direita
        right_layout = BoxLayout(orientation='vertical', spacing=10)

        # Label de logs
        self.log_label = Label(text='', size_hint_y=None, height=30)
        right_layout.add_widget(self.log_label)

        # Botão para atualizar as câmeras
        refresh_button = Button(text='Refresh das Câmeras')
        refresh_button.bind(on_press=self.refresh_cameras)
        right_layout.add_widget(refresh_button)

        # Adicionar os demais botões ao layout à direita
        for i in range(4):
            button = Button(text=f'Botão {i+2}')
            right_layout.add_widget(button)

        main_layout.add_widget(right_layout)

        return main_layout

    def refresh_cameras(self, instance):
        # Limpar as câmeras existentes
        cameras_layout = self.root.children[0]
        for column_layout in cameras_layout.children:
            for camera_widget in column_layout.children:
                if isinstance(camera_widget, CameraLabel):
                    camera_widget.on_stop()
                    column_layout.remove_widget(camera_widget)

        # Recriar os widgets de câmeras e adicioná-los novamente
        for camera_index in range(4):
            if camera_index < 2:
                column_layout = cameras_layout.children[0]
            else:
                column_layout = cameras_layout.children[1]
            column_layout.add_widget(CameraLabel(camera_index, known_faces, known_names, self.log_label))

if __name__ == '__main__':
    CamerasApp().run()
