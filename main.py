from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
import os
import subprocess

class MainMenu(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        button1 = Button(text="Monitoramento")
        button1.bind(on_release=self.open_app1)
        self.add_widget(button1)

        button2 = Button(text="Cadastro de Alunos")
        button2.bind(on_release=self.open_app2)
        self.add_widget(button2)

        button3 = Button(text="Banco de Dados")
        button3.bind(on_release=self.open_app3)
        self.add_widget(button3)

    def open_app1(self, instance):
        try:
            current_directory = os.path.dirname(os.path.abspath(__file__))
            app1_path = os.path.join(current_directory, 'modulo_monitoramento.py')
            # print("Abrindo:", app1_path)
            subprocess.Popen(['python', app1_path])
        except Exception as e:
            print(f"Erro ao abrir a aplicação: {e}")

    def open_app2(self, instance):
        try:
            current_directory = os.path.dirname(os.path.abspath(__file__))
            app1_path = os.path.join(current_directory, 'modulo_cadastro.py')
            # print("Abrindo:", app1_path)
            subprocess.Popen(['python', app1_path])
        except Exception as e:
            print(f"Erro ao abrir a aplicação: {e}")

    def open_app3(self, instance):
        try:
            current_directory = os.path.dirname(os.path.abspath(__file__))
            app1_path = os.path.join(current_directory, 'modulo_banco_de_dados.py')
            # print("Abrindo:", app1_path)
            subprocess.Popen(['python', app1_path])
        except Exception as e:
            print(f"Erro ao abrir a aplicação: {e}")

class MainApp(App):
    def build(self):
        self.title = 'Sistema de Monitoramento'
        self.icon = 'Imagens/icone_camera.png'
        return MainMenu()

if __name__ == '__main__':
    MainApp().run()
