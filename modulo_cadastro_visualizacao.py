import json
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.uix.camera import Camera

class VisualizacaoCadastro(BoxLayout):
    def __init__(self, **kwargs):
        super(VisualizacaoCadastro, self).__init__(**kwargs)
        self.orientation = 'horizontal'

        # ----------- Container da esquerda
        self.container_esquerda = BoxLayout(orientation='vertical', padding=5, spacing=5)

        # Subcontainer de Opções
        self.sub_container_esquerda = BoxLayout(orientation='horizontal', padding=5, spacing=5)

        # Botão Anterior
        button_anterior = Button(text="Anterior", size=(5, 5))
        self.sub_container_esquerda.add_widget(button_anterior)

        # Botão Próximo
        button_proximo = Button(text="Próximo", size=(5, 5))
        self.sub_container_esquerda.add_widget(button_proximo)

        # Adicionar botões Parte Esquerda
        self.container_esquerda.add_widget(self.sub_container_esquerda)
        self.add_widget(self.container_esquerda)

        # ----------- Container da Direita
        self.container_direita = BoxLayout(orientation='vertical', padding=5, spacing=5)

        # Inicializando o TextInput para a Disciplina
        self.disciplina_input = TextInput(size_hint_y=None, height='48dp', hint_text='Selecione a Disciplina')

        # Dropdown de seleção de disciplina, lista criada a partir das pastas dentro de "Alunos"
        lista_disciplinas = self.lista_de_disciplinas()
        dropdown = DropDown()

        # Criação dos botões no DropDown com base na lista de disciplinas
        for disciplina in lista_disciplinas:
            btn = Button(text=disciplina, size_hint_y=None, height=44)
            btn.bind(on_release=self.selecionar_disciplina(dropdown))  # Ao selecionar uma disciplina, fecha o dropdown
            dropdown.add_widget(btn)

        # Associar o DropDown ao TextInput
        self.disciplina_input.bind(on_touch_down=lambda instance, touch: dropdown.open(self.disciplina_input) if instance.collide_point(*touch.pos) else None)

        # Adiciona o TextInput ao layout
        self.container_direita.add_widget(self.disciplina_input)

        # Botão de Fechar Tela
        self.fechar_button = Button(text='Fechar', size_hint_y=None, height='48dp')
        self.fechar_button.bind(on_release=self.stop_app)
        self.container_direita.add_widget(self.fechar_button)

        # Adicionar botões Parte Direita
        self.add_widget(self.container_direita)

    # Busca a Lista de Disciplinas pelas pastas existentes
    def lista_de_disciplinas(self):
        lista_disciplinas = []
        self.caminho_pasta = 'Alunos'

        # Verifica se o caminho da pasta existe
        if os.path.exists(self.caminho_pasta):
            # Itera pelas subpastas do diretório
            for item in os.listdir(self.caminho_pasta):
                caminho_completo = os.path.join(self.caminho_pasta, item)

                # Verifica se o item é uma pasta
                if os.path.isdir(caminho_completo):
                    lista_disciplinas.append(item)
        else:
            print(f"A pasta {self.caminho_pasta} não existe.")

        return lista_disciplinas

    def selecionar_disciplina(self, dropdown):
        def update_text(instance):
            self.disciplina_input.text = instance.text
            dropdown.dismiss()  # Fecha o dropdown após seleção

        return update_text

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
