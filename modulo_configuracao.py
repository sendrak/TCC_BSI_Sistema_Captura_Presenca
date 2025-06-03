import kivy
import json

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.image import Image

class ConfigScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(ConfigScreen, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 5
        self.spacing = 5

        image = Image(source="Imagens/logo_iff_campus_centro.png")
        self.add_widget(image)

        self.informacoes_label = Label(text="**As informações definidas aqui são pré carregadas nas telas do sistema.**", size_hint_y=None, height=30)
        self.add_widget(self.informacoes_label)

        # Label e campos de entrada para os parâmetros
        self.select_cam_label = Label(text="Selecione a Camera que será utilizada (Padrão Windows = 0 / A câmera de um notebook será sempre a 0):", size_hint_y=None, height=30)
        self.select_cam_input = TextInput(size_hint_y=None, height=30)
        self.add_widget(self.select_cam_label)
        self.add_widget(self.select_cam_input)

        # Novo Label e TextInput para a Matrícula
        self.select_matricula_label = Label(text="Informe a Matrícula de Professor:", size_hint_y=None, height=30)
        self.select_matricula_input = TextInput(size_hint_y=None, height=30)
        self.add_widget(self.select_matricula_label)
        self.add_widget(self.select_matricula_input)

        # O label Disciplina foi reativado para evitar erro no salvamento
        self.select_disciplina_label = Label(text="Informe a Disciplina:", size_hint_y=None, height=30)
        self.select_disciplina_input = TextInput(size_hint_y=None, height=30)
        self.add_widget(self.select_disciplina_label)
        self.add_widget(self.select_disciplina_input)

        self.select_curso_label = Label(text="Informe o Curso: ", size_hint_y=None, height=30)
        self.select_curso_input = TextInput(size_hint_y=None, height=30)
        self.add_widget(self.select_curso_label)
        self.add_widget(self.select_curso_input)

        # Busca o arquivo TXT e carrega os parâmetros
        try:
            with open("Configuracoes/config.txt", "r") as config_file:
                config = json.load(config_file)
                self.select_cam_input.text = config.get("select_cam", "")
                self.select_matricula_input.text = config.get("select_matricula", "")
                self.select_disciplina_input.text = config.get("select_disciplina", "") 
                self.select_curso_input.text = config.get("select_curso", "")
        except FileNotFoundError:
            pass

        # Botão de Salvar
        save_button = Button(text="Salvar Configurações", size_hint_y=None, height=40)
        save_button.bind(on_press=self.save_config)
        self.add_widget(save_button)

        # Botão de Fechar
        close_button = Button(text="Fechar", size_hint_y=None, height=40)
        close_button.bind(on_press=self.close_app)
        self.add_widget(close_button)

    def save_config(self, instance):
        # Salvanmento dos parâmetros no arquivo config.txt
        config = {
            "select_cam": self.select_cam_input.text,
            "select_matricula": self.select_matricula_input.text,
            "select_disciplina": self.select_disciplina_input.text,
            "select_curso": self.select_curso_input.text,
        }

        with open("Configuracoes/config.txt", "w") as config_file:
            json.dump(config, config_file)

        # Mensagem com novos valores
        message = f"Configurações Padrão Alteradas:\n\n" \
                  f"Index da Camera: {config['select_cam']}\n" \
                  f"Matrícula do Professor: {config['select_matricula']}\n" \
                  f"Disciplina: {config['select_disciplina']}\n" \
                  f"Curso: {config['select_curso']}"

        # Abra uma popup de confirmação com os novos valores
        popup = Popup(title="Salvamento de Configurações", size_hint=(0.7, 0.7))

        # BoxLayout para organizar os widgets dentro da popup
        popup_content = BoxLayout(orientation='vertical')

        # Label com a mensagem
        popup_content.add_widget(Label(text=message))

        # Botão "Fechar Popup" para fechar a popup
        close_popup_button = Button(text="Fechar Popup", size_hint_y=None, height=40)
        close_popup_button.bind(on_press=popup.dismiss)
        popup_content.add_widget(close_popup_button)

        # Conteúdo da popup
        popup.content = popup_content

        popup.open()

    def close_app(self, instance):
        App.get_running_app().stop()


class ConfigApp(App):
    def build(self):
        self.title = 'Instituto Federal Fluminense - Configurações do Aplicativo'
        self.icon = 'Imagens/icone_camera.png'
        return ConfigScreen()


if __name__ == '__main__':
    ConfigApp().run()
