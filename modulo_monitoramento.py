from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.clock import Clock
import cv2
from kivy.graphics.texture import Texture
import face_recognition
import os

class CameraLabel(BoxLayout):
    def __init__(self, camera_index, known_faces, known_names, **kwargs):
        super().__init__(**kwargs)
        self.camera_index = camera_index
        self.known_faces = known_faces
        self.known_names = known_names
        self.detected_people = {}  # Dictionary to track detected people

        self.capture = cv2.VideoCapture(camera_index)
        self.image = Image(source='Imagens/no_camera.png')
        self.add_widget(self.image)

        Clock.schedule_interval(self.update, 0 / 30.0)

    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            buffer = cv2.flip(frame, 0).tobytes()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')

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
                        print(f"Face reconhecida na câmera {self.camera_index + 1}: {person_name}")
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                else:
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            exited_people = set(self.detected_people.keys()) - newly_detected_people
            for person_name in exited_people:
                print(f"{person_name} saiu do alcance da câmera {self.camera_index + 1}")

            self.detected_people = {person_name: (top, right, bottom, left) for (top, right, bottom, left), person_name in zip(face_locations, newly_detected_people)}

            self.image.texture = texture
        else:
            self.image.source = 'Imagens/no_camera.png'

    def on_stop(self):
        self.capture.release()

class CamerasApp(App):
    def build(self):
        self.title = 'Monitoramento Multicamera'
        self.icon = 'Imagens/icone_camera.png'
        Window.maximize()

        known_faces = []
        known_names = []

        known_faces_folder = "Pessoas"

        for filename in os.listdir(known_faces_folder):
            if filename.endswith(".jpg") or filename.endswith(".png"):
                image_path = os.path.join(known_faces_folder, filename)
                face_image = face_recognition.load_image_file(image_path)
                face_encoding = face_recognition.face_encodings(face_image)[0]
                known_faces.append(face_encoding)
                person_name = os.path.splitext(filename)[0]
                known_names.append(person_name)

        main_layout = BoxLayout(orientation='horizontal', spacing=10)

        cameras_layout = BoxLayout(orientation='vertical', spacing=10)

        first_row_layout = BoxLayout(orientation='horizontal', spacing=10)
        second_row_layout = BoxLayout(orientation='horizontal', spacing=10)

        for camera_index in range(2):
            camera_widget = CameraLabel(camera_index, known_faces, known_names)
            first_row_layout.add_widget(camera_widget)

        for camera_index in range(2, 4):
            camera_widget = CameraLabel(camera_index, known_faces, known_names)
            second_row_layout.add_widget(camera_widget)

        cameras_layout.add_widget(first_row_layout)
        cameras_layout.add_widget(second_row_layout)

        main_layout.add_widget(cameras_layout)

        right_layout = BoxLayout(orientation='vertical', spacing=10)

        refresh_button = Button(text='Refresh das Câmeras')
        refresh_button.bind(on_press=self.refresh_cameras)
        right_layout.add_widget(refresh_button)

        for i in range(4):
            button = Button(text=f'Botão {i+2}')
            right_layout.add_widget(button)

        main_layout.add_widget(right_layout)

        return main_layout

    def refresh_cameras(self, instance):
        cameras_layout = self.root.children[0]
        for row_layout in cameras_layout.children:
            for camera_widget in row_layout.children:
                if isinstance(camera_widget, CameraLabel):
                    camera_widget.on_stop()
                    row_layout.remove_widget(camera_widget)
                    camera_widget = CameraLabel(camera_widget.camera_index, known_faces, known_names)
                    row_layout.add_widget(camera_widget)

if __name__ == '__main__':
    CamerasApp().run()
