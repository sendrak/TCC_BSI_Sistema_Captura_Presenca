from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image

import os
import subprocess

class MainMenu(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.processes = []  # Lista para rastrear subprocessos, utilizado para finalizar o app no botão fechar

        # BoxLayout para conter os botões e logo
        container_central = BoxLayout(orientation='vertical', padding=5, spacing=5)

        # Adicione um widget de imagem no topo
        image = Image(source="Imagens/logo_iff_campus_centro.png")
        container_central.add_widget(image)

        # Botões com tamanho fixo
        button1 = Button(text="Monitoramento Multicâmeras", size=(200, 50))
        button1.bind(on_release=self.open_app1)
        container_central.add_widget(button1)

        button2 = Button(text="Cadastro de Alunos", size=(200, 50))
        button2.bind(on_release=self.open_app2)
        container_central.add_widget(button2)

        button3 = Button(text="Banco de Dados", size=(200, 50))
        button3.bind(on_release=self.open_app3)
        container_central.add_widget(button3)

        button4 = Button(text="Captura de Presença - Tempo Real", size=(200, 50))
        button4.bind(on_release=self.open_app4)
        container_central.add_widget(button4)

        button5 = Button(text="Captura Presença - Imagem", size=(200, 50))
        button5.bind(on_release=self.open_app5)
        container_central.add_widget(button5)

        button_close = Button(text="Fechar Aplicação", size=(200, 50))
        button_close.bind(on_release=self.close_apps)
        container_central.add_widget(button_close)

        # Adicione o BoxLayout com a imagem e os botões ao MainMenu
        self.add_widget(container_central)

    def open_app1(self, instance):
        try:
            current_directory = os.path.dirname(os.path.abspath(__file__))
            app1_path = os.path.join(current_directory, 'modulo_monitoramento.py')
            print("Abrindo:", app1_path)
            process = subprocess.Popen(['python', app1_path])
            self.processes.append(process)  # Adiciona o subprocesso à lista de apps abertos
        except Exception as e:
            print(f"Erro ao abrir a aplicação: {e}")

    def open_app2(self, instance):
        try:
            current_directory = os.path.dirname(os.path.abspath(__file__))
            app2_path = os.path.join(current_directory, 'modulo_cadastro.py')
            print("Abrindo:", app2_path)
            process = subprocess.Popen(['python', app2_path])
            self.processes.append(process)  # Adiciona o subprocesso à lista de apps abertos
        except Exception as e:
            print(f"Erro ao abrir a aplicação: {e}")

    def open_app3(self, instance):
        try:
            current_directory = os.path.dirname(os.path.abspath(__file__))
            app3_path = os.path.join(current_directory, 'modulo_banco_de_dados.py')
            print("Abrindo:", app3_path)
            process = subprocess.Popen(['python', app3_path])
            self.processes.append(process)  # Adiciona o subprocesso à lista de apps abertos
        except Exception as e:
            print(f"Erro ao abrir a aplicação: {e}")

    def open_app4(self, instance):
        try:
            current_directory = os.path.dirname(os.path.abspath(__file__))
            app4_path = os.path.join(current_directory, 'modulo_presenca.py')
            print("Abrindo:", app4_path)
            process = subprocess.Popen(['python', app4_path])
            self.processes.append(process)  # Adiciona o subprocesso à lista de apps abertos
        except Exception as e:
            print(f"Erro ao abrir a aplicação: {e}")

    def open_app5(self, instance):
        try:
            current_directory = os.path.dirname(os.path.abspath(__file__))
            app4_path = os.path.join(current_directory, 'modulo_presenca_imagem.py')
            print("Abrindo:", app4_path)
            process = subprocess.Popen(['python', app4_path])
            self.processes.append(process)  # Adiciona o subprocesso à lista de apps abertos
        except Exception as e:
            print(f"Erro ao abrir a aplicação: {e}")

    # Fecha o Menu e todas as janelas abertas através do menu
    def close_apps(self, instance):
        for process in self.processes:
            process.terminate()  # Encerra a janela aberta
        App.get_running_app().stop()  # Fecha o aplicativo principal após fechar os subprocessos.

class MainApp(App):
    def build(self):
        self.title = 'Captura de Presença'
        self.icon = 'Imagens/icone_camera.png'
        return MainMenu()

if __name__ == '__main__':
    MainApp().run()
