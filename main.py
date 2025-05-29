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

        # Logotipo do IFF no topo
        image = Image(source="Imagens/logo_iff_campus_centro.png")
        container_central.add_widget(image)

        # Botões de monitoramento (Trabalho Futuro)
        button_monitoramento = Button(text="Monitoramento Multicâmeras(Trabalho Futuro)", size=(200, 50))
        button_monitoramento.bind(on_release=self.open_monitoramento)

        button_submete_presenca = Button(text="Submeter Presença para IFF Acadêmico(Trabalho Futuro)")
        button_submete_presenca.bind(on_release=self.open_submete_presenca)

        # Botão duplo em linha - trabalho futuro
        container_trabalho_futuro = BoxLayout(orientation='horizontal', spacing=5)
        container_trabalho_futuro.add_widget(button_monitoramento)
        container_trabalho_futuro.add_widget(button_submete_presenca)
        container_central.add_widget(container_trabalho_futuro)

        button_cadastro_alunos = Button(text="Cadastro de Alunos", size=(200, 50))
        button_cadastro_alunos.bind(on_release=self.open_cadastro)
        container_central.add_widget(button_cadastro_alunos)

        button_banco_de_dados = Button(text="Banco de Dados - Alunos Cadastrados", size=(200, 50))
        button_banco_de_dados.bind(on_release=self.open_database)
        container_central.add_widget(button_banco_de_dados)

        button_captura_video = Button(text="Gerar de Presença Por Vídeo em Tempo Real", size=(200, 50))
        button_captura_video.bind(on_release=self.open_captura_video)
        container_central.add_widget(button_captura_video)

        # Botão duplo em linha
        container_presenca_imagem = BoxLayout(orientation='horizontal', spacing=5)
        button_captura_imagem_turma = Button(text="Captura de Foto para Presença da Turma", size=(200, 50))
        button_captura_imagem_turma.bind(on_release=self.open_captura_imagem_turma)
        container_presenca_imagem.add_widget(button_captura_imagem_turma)

        button_captura_imagem = Button(text="Gerar Presença por Imagem da Turma", size=(200, 50))
        button_captura_imagem.bind(on_release=self.open_captura_imagem)
        container_presenca_imagem.add_widget(button_captura_imagem)

        container_central.add_widget(container_presenca_imagem)

        # Botão duplo em linha
        container_config_fechar = BoxLayout(orientation='horizontal', spacing=5)
        button_config = Button(text="Configurações", size=(200, 50))
        button_config.bind(on_release=self.open_config)
        container_config_fechar.add_widget(button_config)

        button_close = Button(text="Fechar Aplicação", size=(200, 50))
        button_close.bind(on_release=self.close_apps)
        container_config_fechar.add_widget(button_close)

        container_central.add_widget(container_config_fechar)

        # BoxLayout com a imagem e os botões ao MainMenu
        self.add_widget(container_central)

    def open_monitoramento(self, instance):
        try:
            current_directory = os.path.dirname(os.path.abspath(__file__))
            app_path = os.path.join(current_directory, 'modulo_multicameras.py')
            print("Abrindo:", app_path)
            process = subprocess.Popen(['python', app_path])
            self.processes.append(process)  # Adiciona o subprocesso à lista de apps abertos
        except Exception as e:
            print(f"Erro ao abrir a aplicação: {e}")

    def open_cadastro(self, instance):
        try:
            current_directory = os.path.dirname(os.path.abspath(__file__))
            app_path = os.path.join(current_directory, 'modulo_cadastro.py')
            print("Abrindo:", app_path)
            process = subprocess.Popen(['python', app_path])
            self.processes.append(process)  # Adiciona o subprocesso à lista de apps abertos
        except Exception as e:
            print(f"Erro ao abrir a aplicação: {e}")

    def open_database(self, instance):
        try:
            current_directory = os.path.dirname(os.path.abspath(__file__))
            app_path = os.path.join(current_directory, 'modulo_cadastro_visualizacao.py')
            print("Abrindo:", app_path)
            process = subprocess.Popen(['python', app_path])
            self.processes.append(process)  # Adiciona o subprocesso à lista de apps abertos
        except Exception as e:
            print(f"Erro ao abrir a aplicação: {e}")

    def open_submete_presenca(self, instance):
        try:
            current_directory = os.path.dirname(os.path.abspath(__file__))
            app_path = os.path.join(current_directory, 'modulo_submete_presenca.py')
            print("Abrindo:", app_path)
            process = subprocess.Popen(['python', app_path])
            self.processes.append(process)  # Adiciona o subprocesso à lista de apps abertos
        except Exception as e:
            print(f"Erro ao abrir a aplicação: {e}")

    def open_captura_video(self, instance):
        try:
            current_directory = os.path.dirname(os.path.abspath(__file__))
            app_path = os.path.join(current_directory, 'modulo_presenca_video.py')
            print("Abrindo:", app_path)
            process = subprocess.Popen(['python', app_path])
            self.processes.append(process)  # Adiciona o subprocesso à lista de apps abertos
        except Exception as e:
            print(f"Erro ao abrir a aplicação: {e}")

    def open_captura_imagem_turma(self, instance):
        try:
            current_directory = os.path.dirname(os.path.abspath(__file__))
            app_path = os.path.join(current_directory, 'modulo_captura_turma.py')
            print("Abrindo:", app_path)
            process = subprocess.Popen(['python', app_path])
            self.processes.append(process)  # Adiciona o subprocesso à lista de apps abertos
        except Exception as e:
            print(f"Erro ao abrir a aplicação: {e}")

    def open_captura_imagem(self, instance):
        try:
            current_directory = os.path.dirname(os.path.abspath(__file__))
            app_path = os.path.join(current_directory, 'modulo_presenca_imagem.py')
            print("Abrindo:", app_path)
            process = subprocess.Popen(['python', app_path])
            self.processes.append(process)  # Adiciona o subprocesso à lista de apps abertos
        except Exception as e:
            print(f"Erro ao abrir a aplicação: {e}")

    def open_config(self, instance):
        try:
            current_directory = os.path.dirname(os.path.abspath(__file__))
            app_path = os.path.join(current_directory, 'modulo_configuracao.py')
            print("Abrindo:", app_path)
            process = subprocess.Popen(['python', app_path])
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
        self.title = 'Instituto Federal Fluminense - Captura de Presença'
        self.icon = 'Imagens/icone_camera.png'
        return MainMenu()


if __name__ == '__main__':
    MainApp().run()
