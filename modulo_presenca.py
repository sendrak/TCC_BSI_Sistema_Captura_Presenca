from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.camera import Camera
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

class PresenceCaptureApp(App):
    def build(self):
        # Layout principal com duas colunas
        layout = BoxLayout(orientation='horizontal', spacing=10)

        # Coluna 1: Visualização da câmera
        camera = Camera(index=0, play=True)
        layout.add_widget(camera)

        # Coluna 2: Campos de texto e botões
        col2_layout = BoxLayout(orientation='vertical', spacing=10)

        # Campos de texto
        text_input1 = TextInput(hint_text='Curso')
        text_input2 = TextInput(hint_text='Disciplina')

        # Botão Iniciar Captura de Presença
        start_button = Button(text='Iniciar Captura de Presença')
        start_button.bind(on_press=self.start_capture)

        # Botão Fechar Presença
        close_button = Button(text='Fechar Presença')
        close_button.bind(on_press=self.close_presence)

        # Adicionar widgets à coluna 2
        col2_layout.add_widget(text_input1)
        col2_layout.add_widget(text_input2)
        col2_layout.add_widget(start_button)
        col2_layout.add_widget(close_button)

        # Adicionar coluna 2 ao layout principal
        layout.add_widget(col2_layout)

        return layout

    def start_capture(self, instance):
        # Lógica para iniciar a captura de presença
        # Aqui você pode implementar a lógica de captura de presença
        pass

    def close_presence(self, instance):
        # Lógica para fechar a presença
        # Aqui você pode implementar a lógica para encerrar a captura de presença
        pass

if __name__ == '__main__':
    PresenceCaptureApp().run()
