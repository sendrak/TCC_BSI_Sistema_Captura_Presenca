import json
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.uix.camera import Camera


class VisualizacaoCadastro(BoxLayout):
    def __init__(self, **kwargs):
        super(VisualizacaoCadastro, self).__init__(**kwargs)
        self.caminho_pasta = None
        self.orientation = 'horizontal'
        self.imagens = []  # Lista para armazenar os caminhos das imagens
        self.imagem_atual_index = 0  # Índice da imagem atual
        self.selecionou_disciplina = False  # Flag para verificar se a disciplina foi selecionada

        # ----------- Container da Esquerda
        self.container_botoes_esquerda = BoxLayout(orientation='vertical', padding=5, spacing=5)

        # Inicializando o TextInput para a Disciplina
        self.disciplina_input = TextInput(size_hint_y=None, height='48dp', hint_text='Selecione a Disciplina')

        # Dropdown de seleção de disciplina, lista criada a partir das pastas dentro de "Alunos"
        lista_disciplinas = self.lista_de_disciplinas()
        dropdown = DropDown()

        # Criação do botão no DropDown com base na lista de disciplinas
        for disciplina in lista_disciplinas:
            btn = Button(text=disciplina, size_hint_y=None, height=44)
            btn.bind(on_release=self.selecionar_disciplina(dropdown))
            dropdown.add_widget(btn)

        # Associar o DropDown ao TextInput
        self.disciplina_input.bind(
            on_touch_down=lambda instance, touch: dropdown.open(self.disciplina_input) if instance.collide_point(
                *touch.pos) else None)

        # Adiciona o TextInput ao layout
        self.container_botoes_esquerda.add_widget(self.disciplina_input)

        # Botão de Fechar Tela
        self.fechar_button = Button(text='Fechar', size_hint_y=None, height='48dp')
        self.fechar_button.bind(on_release=self.stop_app)
        self.container_botoes_esquerda.add_widget(self.fechar_button)

        # Adicionar botões Parte Esquerda
        self.add_widget(self.container_botoes_esquerda)

        # ----------- Container da Direita
        self.container_visualizacao_direita = BoxLayout(orientation='vertical', padding=5, spacing=5)

        # Criação do Label dinâmico
        self.disciplina_label = Label(text="Nenhuma disciplina selecionada", font_size='20sp', bold=True)

        # Adiciona o evento para atualizar o label quando o texto do input mudar
        self.disciplina_input.bind(text=self.update_label)
        # Subcontainer de Opções
        self.sub_container_navegacao = BoxLayout(orientation='horizontal', padding=5, spacing=5)

        # Adiciona o Label de Disciplina
        self.container_visualizacao_direita.add_widget(self.disciplina_label)

        # ----------- Exibição da Imagem
        self.imagem_display = Image(size_hint=(1, None), height='500dp')
        self.container_visualizacao_direita.add_widget(self.imagem_display)

        # Labels dinâmicos de acordo com a imagem selecionada
        self.nome_label = Label(text="Nome: ", font_size='20sp')
        self.container_visualizacao_direita.add_widget(self.nome_label)
        self.matricula_label = Label(text="Matricula: ", font_size='20sp')
        self.container_visualizacao_direita.add_widget(self.matricula_label)

        # Botões para navegação de imagens
        self.button_anterior = Button(text="Anterior", size_hint=(1, None), height='50dp')
        self.button_anterior.bind(on_release=self.mudar_imagem_anterior)
        self.sub_container_navegacao.add_widget(self.button_anterior)

        self.button_proximo = Button(text="Próximo", size_hint=(1, None), height='50dp')
        self.button_proximo.bind(on_release=self.mudar_imagem_proxima)
        self.sub_container_navegacao.add_widget(self.button_proximo)

        # Adicionar botões Parte Direita
        self.container_visualizacao_direita.add_widget(self.sub_container_navegacao)
        self.add_widget(self.container_visualizacao_direita)

    # Atualiza o label da Disciplina
    def update_label(self, instance, value):
        self.disciplina_label.text = f"Disciplina Selecionada: {value}" if value else "Nenhuma disciplina selecionada"
        if value:
            self.selecionou_disciplina = True
            self.carregar_imagens(value)
            self.atualizar_imagem()
        else:
            self.selecionou_disciplina = False

    # Destrincha o nome do arquivo para obter o nome e matricula
    def extrair_nome_matricula(self, arquivo):
        nome_matricula = os.path.basename(arquivo).replace('.png', '')

        # Divide o nome do arquivo em três partes: disciplina, nome do aluno e matrícula pelo underline _
        partes = nome_matricula.split('_', 2)

        if len(partes) == 3:
            disciplina = partes[0]
            nome = partes[1]
            matricula = partes[2]
        else:
            # Tratativa de erro (Nunca vai acontecer caso tudo seja feito pelo software)
            disciplina = partes[0]
            nome = "N/A"
            matricula = "N/A"

        return disciplina, nome, matricula

    # Atualiza os labels de Nome e Matrícula
    def update_label_aluno(self):
        if self.imagens:
            disciplina, nome, matricula = self.extrair_nome_matricula(self.imagens[self.imagem_atual_index])
            self.nome_label.text = f"Nome: {nome}"
            self.matricula_label.text = f"Matricula: {matricula}"

    # Carrega as imagens da disciplina selecionada
    def carregar_imagens(self, disciplina):
        # Caminho para as pastas de imagens dentro da pasta de "Alunos" e para a disciplina selecionada
        self.imagens = []
        caminho_disciplina = os.path.join('Alunos', disciplina)

        if os.path.exists(caminho_disciplina):
            # Itera pelas imagens dentro da pasta da disciplina
            for item in os.listdir(caminho_disciplina):
                caminho_completo = os.path.join(caminho_disciplina, item)
                if os.path.isfile(caminho_completo) and item.lower().endswith(('.png')):
                    self.imagens.append(caminho_completo)

    # Atualiza a imagem exibida
    def atualizar_imagem(self):
        if self.imagens and 0 <= self.imagem_atual_index < len(self.imagens):  # Verificação posição no array
            self.imagem_display.source = self.imagens[self.imagem_atual_index]
            self.imagem_display.reload()  # Força o Kivy a recarregar a imagem
            self.update_label_aluno()  # Atualiza os labels de nome e matrícula ao trocar de imagem

    # Anterior
    def mudar_imagem_anterior(self, instance):
        if self.selecionou_disciplina and self.imagens:
            self.imagem_atual_index = (self.imagem_atual_index - 1) % len(self.imagens)
            self.atualizar_imagem()

    # Próximo
    def mudar_imagem_proxima(self, instance):
        if self.selecionou_disciplina and self.imagens:
            self.imagem_atual_index = (self.imagem_atual_index + 1) % len(self.imagens)
            self.atualizar_imagem()

    # Busca a Lista de Disciplinas pelas pastas criadas
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
            dropdown.dismiss()  # Fecha o dropdown

        return update_text

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
