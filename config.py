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

        # Crie rótulos e caixas de entrada para os parâmetros
        self.select_cam_label = Label(text="Selecione a Camera (Padrão Windows = 0):", size_hint_y=None, height=30)
        self.select_cam_input = TextInput(size_hint_y=None, height=30)
        self.add_widget(self.select_cam_label)
        self.add_widget(self.select_cam_input)

        self.select_disciplina_label = Label(text="Informe a Disciplina Padrão:", size_hint_y=None, height=30)
        self.select_disciplina_input = TextInput(size_hint_y=None, height=30)
        self.add_widget(self.select_disciplina_label)
        self.add_widget(self.select_disciplina_input)

        self.select_curso_label = Label(text="Informe o Curso Padrão:", size_hint_y=None, height=30)
        self.select_curso_input = TextInput(size_hint_y=None, height=30)
        self.add_widget(self.select_curso_label)
        self.add_widget(self.select_curso_input)

        # Carregue os parâmetros do arquivo config.txt, se existir
        try:
            with open("Configuracoes/config.txt", "r") as config_file:
                config = json.load(config_file)
                self.select_cam_input.text = config.get("select_cam", "")
                self.select_disciplina_input.text = config.get("select_disciplina", "")
                self.select_curso_input.text = config.get("select_curso", "")
        except FileNotFoundError:
            pass

        # Crie um botão para salvar as configurações
        save_button = Button(text="Salvar Configurações", size_hint_y=None, height=40)
        save_button.bind(on_press=self.save_config)
        self.add_widget(save_button)

        # Crie um botão para fechar a tela
        close_button = Button(text="Fechar", size_hint_y=None, height=40)
        close_button.bind(on_press=self.close_app)
        self.add_widget(close_button)

    def save_config(self, instance):
        # Salve os parâmetros no arquivo config.txt
        config = {
            "select_cam": self.select_cam_input.text,
            "select_disciplina": self.select_disciplina_input.text,
            "select_curso": self.select_curso_input.text,
        }

        with open("Configuracoes/config.txt", "w") as config_file:
            json.dump(config, config_file)

        # Crie uma mensagem com os novos valores
        message = f"Configurações Padrão Alteradas:\n\n" \
                  f"Selecione a Camera: {config['select_cam']}\n" \
                  f"Informe a Disciplina Padrão: {config['select_disciplina']}\n" \
                  f"Informe o Curso Padrão: {config['select_curso']}"

        # Abra uma popup de confirmação com os novos valores
        popup = Popup(title="Configurações Alteradas",
                      content=Label(text=message),
                      size_hint=(0.5, 0.5))

        # Adicione um botão "Fechar Popup" para fechar a popup
        close_popup_button = Button(text="Fechar Popup")
        close_popup_button.bind(on_press=popup.dismiss)
        popup.content.add_widget(close_popup_button)

        popup.open()

    def close_app(self, instance):
        App.get_running_app().stop()


class ConfigApp(App):
    def build(self):
        self.title = 'Configurações do Aplicativo'
        self.icon = 'Imagens/icone_camera.png'
        return ConfigScreen()


if __name__ == '__main__':
    ConfigApp().run()
