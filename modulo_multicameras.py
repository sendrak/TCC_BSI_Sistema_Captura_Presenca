# modulo_multicameras.py

import cv2
import threading
from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics.texture import Texture
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock

# Variável que marca quantas câmera serão instanciadas em tela
CAMERA_COUNT = 2

class CameraWidget(BoxLayout):
    def __init__(self, cam_index, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.cam_index = cam_index
        self.capture = None
        self.image = Image()
        self.label = Label(text=f'Câmera {cam_index + 1}', size_hint_y=0.1)
        self.add_widget(self.label)
        self.add_widget(self.image)
        self.start_camera()

    def start_camera(self):
        if self.capture:
            self.capture.release()

        self.capture = cv2.VideoCapture(self.cam_index)
        if not self.capture.isOpened():
            self.capture = None
            # Imagem generica caso a câmera não funcione
            self.image.source = 'Imagens/no_camera.png'
        else:
            Clock.schedule_interval(self.update, 1.0 / 30)

    def update(self, dt):
        if not self.capture:
            return
        ret, frame = self.capture.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.rotate(frame, cv2.ROTATE_180)  # <- Corrigindo orientação
            buffer = frame.tobytes()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
            texture.blit_buffer(buffer, colorfmt='rgb', bufferfmt='ubyte')
            self.image.texture = texture
        else:
            # Imagem para exibição no caso da câmera não ser encontrada
            self.image.source = 'Imagens/no_camera.png'
            pass

    def stop_camera(self):
        if self.capture:
            self.capture.release()
            self.capture = None


class monitoramentoMulticameraApp(App):
    def build(self):
        self.icon = 'Imagens/icone_camera.png'
        self.title = 'Monitoramento Multicameras (Trabalho Futuro)'
        self.cameras = []

        main_layout = BoxLayout(orientation='vertical')
        grid = GridLayout(cols=2, size_hint_y=0.9)

        for i in range(CAMERA_COUNT):
            cam_widget = CameraWidget(i)
            self.cameras.append(cam_widget)
            grid.add_widget(cam_widget)

        refresh_button = Button(text='Refresh Câmeras', size_hint_y=0.1)
        refresh_button.bind(on_press=self.refresh_cameras)
        exit_button = Button(text='Fechar', size_hint_y=0.1)
        exit_button.bind(on_press=self.close_app)

        main_layout.add_widget(grid)
        main_layout.add_widget(refresh_button)
        main_layout.add_widget(exit_button)
        return main_layout

    def refresh_cameras(self, instance):
        for cam in self.cameras:
            cam.stop_camera()
            cam.start_camera()

    def on_stop(self):
        for cam in self.cameras:
            cam.stop_camera()

    def close_app(self):
        App.get_running_app().stop()

if __name__ == '__main__':
    monitoramentoMulticameraApp().run()
