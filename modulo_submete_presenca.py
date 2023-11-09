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
        right_column = BoxLayout(orientation='vertical', spacing=10)

        # Botão Submeter
        submit_button = Button(text="Submeter")
        right_column.add_widget(submit_button)

        # Botão Sair
        exit_button = Button(text="Sair")
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

if __name__ == '__main__':
    SubmetePresenca().run()
