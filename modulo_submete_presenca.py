import json
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
import pandas as pd

class SubmetePresenca(App):
    def build(self):
        self.title = 'Instituto Federal Fluminense - Submeter Presença para Acadêmico'
        self.icon = 'Imagens/icone_camera.png'

        try:
            with open("Configuracoes/config.txt", "r") as config_file:
                config = json.load(config_file)
                # select_cam = config.get("select_cam", "")
                select_matricula = config.get("select_matricula", "")
                select_disciplina = config.get("select_disciplina", "")
                select_curso = config.get("select_curso", "")
        except FileNotFoundError:
            pass

        # Layout principal dividido em duas colunas horizontais
        layout = BoxLayout(orientation='horizontal', spacing=10)

        # Coluna da esquerda
        left_column = BoxLayout(orientation='vertical', spacing=10)

        # Visualizador de conteúdo de arquivo Excel
        self.excel_viewer = TextInput(multiline=True, readonly=True)
        left_column.add_widget(self.excel_viewer)

        # FileChooser para selecionar o arquivo Excel
        file_chooser = FileChooserListView(path=str("PresencasCapturadas"))
        file_chooser.bind(on_submit=self.load_excel_content)
        left_column.add_widget(file_chooser)

        # Adiciona a coluna da esquerda ao layout principal
        layout.add_widget(left_column)

        # Coluna da direita
        right_column = BoxLayout(orientation='vertical', spacing=5, padding=5)

        # Adiciona Labels e TextInputs
        label_matricula = Label(text="Matrícula Acadêmico:")
        input_matricula = TextInput(text=select_matricula, password=False, multiline=False)
        label_senha = Label(text="Senha:")
        input_senha = TextInput(password=True, multiline=False)
        label_curso = Label(text="Curso:")
        input_curso = TextInput(text=select_curso, password=False, multiline=False)
        label_disciplina = Label(text="Disciplina:")
        input_disciplina = TextInput(text=select_disciplina, password=False, multiline=False)

        right_column.add_widget(label_matricula)
        right_column.add_widget(input_matricula)
        right_column.add_widget(label_senha)
        right_column.add_widget(input_senha)
        right_column.add_widget(label_curso)
        right_column.add_widget(input_curso)
        right_column.add_widget(label_disciplina)
        right_column.add_widget(input_disciplina)

        # Botão Submeter
        submit_button = Button(text="Submeter")
        submit_button.bind(on_press=self.submeter_academico)
        right_column.add_widget(submit_button)

        # Botão Sair
        exit_button = Button(text="Sair")
        exit_button.bind(on_press=self.close_app)
        right_column.add_widget(exit_button)

        # Adiciona a coluna da direita ao layout principal
        layout.add_widget(right_column)

        return layout

    def load_excel_content(self, chooser, selected, touch):
        # Carrega o conteúdo do arquivo Excel selecionado no visualizador
        if selected:
            try:
                # Utiliza o pandas para ler o arquivo Excel
                df = pd.read_excel(selected[0])

                # Converte o DataFrame para uma string formatada
                content = df.to_string(index=False)

                # Atualiza o visualizador com o conteúdo formatado
                self.excel_viewer.text = content
            except Exception as e:
                # Se houver um erro ao ler o arquivo Excel, exibe uma mensagem no visualizador
                self.excel_viewer.text = f"Erro ao ler o arquivo Excel: {str(e)}"

    def close_app(self, instance):
        print("Clicou Fechar App")
        App.get_running_app().stop()

    def submeter_academico(self, instance):
        print("Chamou submeter presença para acadêmico")

if __name__ == '__main__':
    SubmetePresenca().run()
