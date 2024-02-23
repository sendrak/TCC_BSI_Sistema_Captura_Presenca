import json

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.uix.camera import Camera
import os
from datetime import datetime


class ConteudoCadastroPessoas(BoxLayout):
    def __init__(self, **kwargs):
        super(ConteudoCadastroPessoas, self).__init__(**kwargs)

        try:
            with open("Configuracoes/config.txt", "r") as config_file:
                config = json.load(config_file)
                # select_cam = config.get("select_cam", "")
                select_matricula = config.get("select_matricula", "")
                select_disciplina = config.get("select_disciplina", "")
                select_curso = config.get("select_curso", "")
        except FileNotFoundError:
            pass

        self.orientation = 'horizontal'

        # Adicione a câmera à coluna da esquerda
        self.container_esquerda = BoxLayout(orientation='vertical', padding=5, spacing=5)
        self.camera = Camera(resolution=(640, 480), play=True)
        self.container_esquerda.add_widget(self.camera)
        self.add_widget(self.container_esquerda)

        self.container_direita = BoxLayout(orientation='vertical', padding=5, spacing=5)

        self.toggle_button = ToggleButton(text='Pause / Play', size_hint_y=None, height='48dp')
        self.toggle_button.bind(on_press=self.alternar_camera)
        self.container_direita.add_widget(self.toggle_button)

        self.curso_input = TextInput(size_hint_y=None, height='48dp', hint_text='Curso', text=select_curso)
        self.container_direita.add_widget(self.curso_input)

        self.disciplina_input = TextInput(size_hint_y=None, height='48dp', hint_text='Curso', text=select_disciplina)
        self.container_direita.add_widget(self.disciplina_input)

        # Pega a data de hoje
        data_atual = datetime.now().strftime('%Y-%m-%d')
        self.data_input = TextInput(size_hint_y=None, height='48dp', hint_text='Data', text=data_atual)
        self.container_direita.add_widget(self.data_input)

        self.capturar_button = Button(text='Capturar', size_hint_y=None, height='48dp')
        self.capturar_button.bind(on_press=self.capture)
        self.container_direita.add_widget(self.capturar_button)

        self.fechar_button = Button(text='Fechar', size_hint_y=None, height='48dp')
        self.fechar_button.bind(on_release=self.stop_app)
        self.container_direita.add_widget(self.fechar_button)

        self.add_widget(self.container_direita)

        self.caminho_salvar = "./ImagensParaPresenca"  # Local de salvamento das imagens

    def alternar_camera(self, instance):
        self.camera.play = not self.camera.play

    def capture(self, instance):
        curso = self.curso_input.text.strip()
        disciplina = self.disciplina_input.text.strip()
        data = self.data_input.text.strip()
        if not curso or not data:
            print("Por favor, preencha o nome e a matrícula da pessoa antes de capturar.")
            return

        filename = os.path.join(self.caminho_salvar, f"{curso}_{disciplina}_{data}.png")
        self.camera.export_to_png(filename)  # Alterado para usar a câmera do self
        self.show_capture_popup(filename)

    def show_capture_popup(self, filename):
        image = Image(source=filename, size_hint=(1, None), height=300)
        popup_content = BoxLayout(orientation='vertical')
        popup_content.add_widget(image)
        popup_content.add_widget(Label(text=f'O arquivo foi salvo como:\n{filename}'))
        buttons_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='48dp')
        nova_captura_button = Button(text='Nova Captura', size_hint_x=1)
        nova_captura_button.bind(on_press=self.dismiss_popup)
        buttons_layout.add_widget(nova_captura_button)

        button_fechar = Button(text='Fechar', size_hint_x=1)
        button_fechar.bind(on_press=self.stop_app)
        buttons_layout.add_widget(button_fechar)

        popup_content.add_widget(buttons_layout)

        popup = Popup(title='Arquivo PNG Capturado', content=popup_content,
                      size_hint=(None, None), size=(400, 550))
        self._popup = popup
        popup.open()

    def dismiss_popup(self, instance):
        self._popup.dismiss()

    def stop_app(self, instance):
        App.get_running_app().stop()


class CadastroDePessoasApp(App):
    def build(self):
        Window.maximize()
        self.title = 'Captura de Imagem da Turma'
        self.icon = 'Imagens/icone_camera.png'

        return ConteudoCadastroPessoas()



if __name__ == '__main__':
    CadastroDePessoasApp().run()
