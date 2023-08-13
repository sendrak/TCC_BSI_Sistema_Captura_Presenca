from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.clock import Clock
import cv2
from kivy.graphics.texture import Texture

# Widget personalizado para exibir a imagem da câmera
class CameraLabel(BoxLayout):
    def __init__(self, camera_index, **kwargs):
        super().__init__(**kwargs)
        self.camera_index = camera_index
        self.capture = cv2.VideoCapture(camera_index)
        self.image = Image(source='Imagens/no_camera.png')  # Imagem caso não tenha camera disponível
        self.add_widget(self.image)

        # Schedule the update function for each instance of CameraLabel
        Clock.schedule_interval(self.update, 0 / 30.0)  # Atualiza a cada 1/30 segundos

    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            buffer = cv2.flip(frame, 0).tobytes()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
            self.image.texture = texture
        else:
            self.image.source = 'Imagens/no_camera.png'  # Define a imagem de "sem câmera" caso haja um problema de conexão

    def on_stop(self):
        self.capture.release()


class CamerasApp(App):
    def build(self):
        # Configurações da Janela
        self.title = 'Monitoramento Multicamera'
        self.icon = 'Imagens/icone_camera.png'
        Window.maximize()

        # Layout principal com três colunas
        main_layout = BoxLayout(orientation='horizontal', spacing=10)

        # Layout secundário para a coluna de câmeras à esquerda
        cameras_layout = BoxLayout(orientation='vertical', spacing=10)

        # Layout secundário para a primeira linha de câmeras
        first_column_layout = BoxLayout(orientation='horizontal', spacing=10)

        # Adicionar as labels das câmeras para a primeira linha
        for camera_index in range(2):  # Altere para o número correto de câmeras na primeira linha
            first_column_layout.add_widget(CameraLabel(camera_index))

        cameras_layout.add_widget(first_column_layout)

        # Layout secundário para a segunda linha de câmeras
        second_column_layout = BoxLayout(orientation='horizontal', spacing=10)

        # Adicionar as labels das câmeras para a segunda linha
        for camera_index in range(2, 4):  # Altere para o número correto de câmeras na segunda linha
            second_column_layout.add_widget(CameraLabel(camera_index))

        cameras_layout.add_widget(second_column_layout)

        main_layout.add_widget(cameras_layout)

        # Layout secundário para a coluna de botões à direita
        right_layout = BoxLayout(orientation='vertical', spacing=10)

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
            column_layout.add_widget(CameraLabel(camera_index))

if __name__ == '__main__':
    CamerasApp().run()
