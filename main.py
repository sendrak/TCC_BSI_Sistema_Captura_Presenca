from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
import os
import subprocess

class MainMenu(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.processes = []  # Lista para rastrear subprocessos

        button1 = Button(text="Monitoramento Multicâmeras")
        button1.bind(on_release=self.open_app1)
        self.add_widget(button1)

        button2 = Button(text="Cadastro de Alunos")
        button2.bind(on_release=self.open_app2)
        self.add_widget(button2)

        button3 = Button(text="Banco de Dados")
        button3.bind(on_release=self.open_app3)
        self.add_widget(button3)

        button4 = Button(text="Controle de Presença")
        button4.bind(on_release=self.open_app4)
        self.add_widget(button4)

        button5 = Button(text="Fechar")
        button5.bind(on_release=self.close_all_apps)
        self.add_widget(button5)

    def open_app1(self, instance):
        try:
            current_directory = os.path.dirname(os.path.abspath(__file__))
            app1_path = os.path.join(current_directory, 'modulo_monitoramento.py')
            print("Abrindo:", app1_path)
            process = subprocess.Popen(['python', app1_path])
            self.processes.append(process)  # Adicione o subprocesso à lista
        except Exception as e:
            print(f"Erro ao abrir a aplicação: {e}")

    def open_app2(self, instance):
        try:
            current_directory = os.path.dirname(os.path.abspath(__file__))
            app2_path = os.path.join(current_directory, 'modulo_cadastro.py')
            print("Abrindo:", app2_path)
            process = subprocess.Popen(['python', app2_path])
            self.processes.append(process)  # Adicione o subprocesso à lista
        except Exception as e:
            print(f"Erro ao abrir a aplicação: {e}")

    def open_app3(self, instance):
        try:
            current_directory = os.path.dirname(os.path.abspath(__file__))
            app3_path = os.path.join(current_directory, 'modulo_banco_de_dados.py')
            print("Abrindo:", app3_path)
            process = subprocess.Popen(['python', app3_path])
            self.processes.append(process)  # Adicione o subprocesso à lista
        except Exception as e:
            print(f"Erro ao abrir a aplicação: {e}")

    def open_app4(self, instance):
        try:
            current_directory = os.path.dirname(os.path.abspath(__file__))
            app4_path = os.path.join(current_directory, 'modulo_presenca.py')
            print("Abrindo:", app4_path)
            process = subprocess.Popen(['python', app4_path])
            self.processes.append(process)  # Adicione o subprocesso à lista
        except Exception as e:
            print(f"Erro ao abrir a aplicação: {e}")

    def close_all_apps(self, instance):
        for process in self.processes:
            process.terminate()  # Encerrar o processo
        App.get_running_app().stop()  # Fechar o aplicativo principal

class MainApp(App):
    def build(self):
        self.title = 'Captura de Presença'
        self.icon = 'Imagens/icone_camera.png'
        return MainMenu()

if __name__ == '__main__':
    MainApp().run()
