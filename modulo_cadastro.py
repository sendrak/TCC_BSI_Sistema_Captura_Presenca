from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.camera import Camera
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.core.window import Window
import os

Builder.load_string('''
<CadastroPessoas>:
    GridLayout:
        cols: 2

        BoxLayout:
            orientation: 'vertical'
            Camera:
                id: camera
                resolution: (640, 480)
                play: True

        BoxLayout:
            orientation: 'vertical'
            size_hint_y: None
            height: '200dp'

            ToggleButton:
                text: 'Pause / Play'
                size_hint_y: None
                height: '48dp'
                on_press: camera.play = not camera.play

            TextInput:
                id: name_input
                size_hint_y: None
                height: '48dp'
                hint_text: 'Nome da pessoa'

            TextInput:
                id: matricula_input
                size_hint_y: None
                height: '48dp'
                hint_text: 'Matrícula'

            Button:
                text: 'Capturar'
                size_hint_y: None
                height: '48dp'
                on_press: root.capture()

            Button:
                text: 'Fechar'
                size_hint_y: None
                height: '48dp'
                on_release: app.stop()
''')

class CadastroPessoas(BoxLayout):
    caminho_salvar = "./Pessoas"  # Defina o caminho desejado aqui

    def capture(self):
        camera = self.ids['camera']
        name = self.ids['name_input'].text.strip().replace(" ", "_")  # Substitui espaços por _
        matricula = self.ids['matricula_input'].text.strip()
        if not name or not matricula:
            print("Por favor, preencha o nome e a matrícula da pessoa antes de capturar.")
            return

        filename = os.path.join(self.caminho_salvar, f"{name}_{matricula}.png")
        camera.export_to_png(filename)
        self.show_capture_popup(filename)

    def show_capture_popup(self, filename):
        image = Image(source=filename, size_hint=(1, None), height=300)
        popup_content = BoxLayout(orientation='vertical')
        popup_content.add_widget(image)
        popup_content.add_widget(Label(text=f'O arquivo foi salvo como:\n{filename}'))
        buttons_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='48dp')
        nova_captura_button = Button(text='Nova Captura', size_hint_x=1)
        nova_captura_button.bind(on_press=lambda instance: self.dismiss_popup())
        buttons_layout.add_widget(nova_captura_button)

        fechar_button = Button(text='Fechar', size_hint_x=1)
        fechar_button.bind(on_press=lambda instance: App.get_running_app().stop())
        buttons_layout.add_widget(fechar_button)

        popup_content.add_widget(buttons_layout)

        popup = Popup(title='Arquivo PNG Capturado', content=popup_content,
                      size_hint=(None, None), size=(400, 550))
        self._popup = popup
        popup.open()

    def dismiss_popup(self):
        self._popup.dismiss()


class CadastroDePessoasApp(App):
    def build(self):
        Window.maximize()
        self.title = 'Cadastro de Alunos'
        self.icon = 'Imagens/icone_camera.png'
        return CadastroPessoas()

if __name__ == '__main__':
    CadastroDePessoasApp().run()
