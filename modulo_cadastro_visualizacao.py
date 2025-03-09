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

class VisualizacaoCadastro(BoxLayout):
    def __init__(self, **kwargs):
        super(VisualizacaoCadastro, self).__init__(**kwargs)
        self.orientation = 'horizontal'

        # Container da esquerda
        self.container_esquerda = BoxLayout(orientation='vertical', padding=5, spacing=5)

        # Subcontainer de Opções
        self.sub_container_esquerda = BoxLayout(orientation='horizontal', padding=5, spacing=5)

        # Botão Anterior

        # Botão Próximo

        # Exibição da Imagem do Aluno

        # Labels de Identificação

        # Adicionar botóes Parte Esquerda
        self.add_widget(self.container_esquerda)

        # ----------- Container da Direita
        self.container_direita = BoxLayout(orientation='vertical', padding=5, spacing=5)

        # Dropdown selecao de disciplina
        # self.disciplina_input = TextInput(size_hint_y=None, height='48dp', hint_text='Disciplina', text=select_disciplina)
        # self.container_direita.add_widget(self.disciplina_input)

        # Campo de Nome
        # self.name_input = TextInput(size_hint_y=None, height='48dp', hint_text='Nome da pessoa')
        # self.container_direita.add_widget(self.name_input)

        # self.matricula_input = TextInput(size_hint_y=None, height='48dp', hint_text='Matrícula')
        # self.container_direita.add_widget(self.matricula_input)

        # Atualizar Cadastro

        # Fechar Tela
        self.fechar_button = Button(text='Fechar', size_hint_y=None, height='48dp')
        self.fechar_button.bind(on_release=self.stop_app)
        self.container_direita.add_widget(self.fechar_button)

        # Adicionar botóes Parte Direita
        self.add_widget(self.container_direita)

    def capture(self, instance):
        name = self.name_input.text.strip()
        matricula = self.matricula_input.text.strip()
        disciplina = self.disciplina_input.text.strip()
        if not name or not matricula or not disciplina:
            print("Por favor, preencha o nome disciplina e matrícula da pessoa antes de capturar.")
            return

        if not os.path.exists(self.caminho_salvar):
            os.makedirs(self.caminho_salvar)
            filename = os.path.join(self.caminho_salvar, f"{disciplina}_{name}_{matricula}.png")
        else:
            filename = os.path.join(self.caminho_salvar, f"{disciplina}_{name}_{matricula}.png")


        self.camera.export_to_png(filename)  # Alterado para usar a câmera do self
        self.show_capture_popup(filename)



    def stop_app(self, instance):
        App.get_running_app().stop()

class VisualizacaoCadastroApp(App):
    def build(self):
        Window.maximize()
        self.title = 'Instituto Federal Fluminense - Cadastro de Alunos'
        self.icon = 'Imagens/icone_camera.png'
        return VisualizacaoCadastro()


if __name__ == '__main__':
    VisualizacaoCadastroApp().run()
