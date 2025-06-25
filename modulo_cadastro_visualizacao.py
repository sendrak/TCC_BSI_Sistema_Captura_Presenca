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
from kivy.uix.popup import Popup
from kivy.uix.anchorlayout import AnchorLayout
from helper_funcoes_reutilizadas import helper_busca_disciplinas


class VisualizacaoCadastro(BoxLayout):
    def __init__(self, **kwargs):
        super(VisualizacaoCadastro, self).__init__(**kwargs)
        self.caminho_pasta = None
        self.orientation = 'horizontal'
        self.imagens = []
        self.imagem_atual_index = 0
        self.selecionou_disciplina = False

        self.container_botoes_esquerda = BoxLayout(orientation='vertical', padding=5, spacing=5)

        self.disciplina_input = TextInput(size_hint_y=None, height='48dp', hint_text='Selecione a Disciplina', readonly=True)

        helper = helper_busca_disciplinas()
        lista_disciplinas = helper.lista_de_disciplinas_cadastradas()
        dropdown = DropDown()

        for disciplina in lista_disciplinas:
            btn = Button(text=disciplina, size_hint_y=None, height=44)
            btn.bind(on_release=self.selecionar_disciplina(dropdown, self.disciplina_input))
            dropdown.add_widget(btn)

        self.disciplina_input.bind(
            on_touch_down=lambda instance, touch: dropdown.open(self.disciplina_input) if instance.collide_point(*touch.pos) else None)

        self.container_botoes_esquerda.add_widget(self.disciplina_input)

        self.fechar_button = Button(text='Fechar', size_hint_y=None, height='48dp')
        self.fechar_button.bind(on_release=self.stop_app)
        self.container_botoes_esquerda.add_widget(self.fechar_button)

        self.add_widget(self.container_botoes_esquerda)

        self.container_visualizacao_direita = BoxLayout(orientation='vertical', padding=5, spacing=5)

        self.disciplina_label = Label(text="Nenhuma disciplina selecionada", font_size='20sp', bold=True)

        self.disciplina_input.bind(text=self.update_label)

        self.sub_container_navegacao = BoxLayout(orientation='horizontal', padding=5, spacing=5)

        self.container_visualizacao_direita.add_widget(self.disciplina_label)

        self.imagem_display = Image(size_hint=(1, None), height='500dp')
        self.container_visualizacao_direita.add_widget(self.imagem_display)

        self.nome_label = Label(text="Nome: ", font_size='20sp')
        self.container_visualizacao_direita.add_widget(self.nome_label)
        self.matricula_label = Label(text="Matricula: ", font_size='20sp')
        self.container_visualizacao_direita.add_widget(self.matricula_label)

        # Botão de Excluir Cadastro
        self.button_excluir = Button(text="Excluir Cadastro", size_hint=(1, None), height='50dp')
        self.button_excluir.bind(on_release=self.confirmar_exclusao)
        self.sub_container_navegacao.add_widget(self.button_excluir)

        self.button_anterior = Button(text="Anterior", size_hint=(1, None), height='50dp')
        self.button_anterior.bind(on_release=self.mudar_imagem_anterior)
        self.sub_container_navegacao.add_widget(self.button_anterior)

        self.button_proximo = Button(text="Próximo", size_hint=(1, None), height='50dp')
        self.button_proximo.bind(on_release=self.mudar_imagem_proxima)
        self.sub_container_navegacao.add_widget(self.button_proximo)

        self.container_visualizacao_direita.add_widget(self.sub_container_navegacao)
        self.add_widget(self.container_visualizacao_direita)

    def update_label(self, instance, value):
        self.disciplina_label.text = f"Disciplina Selecionada: {value}" if value else "Nenhuma disciplina selecionada"
        if value:
            self.selecionou_disciplina = True
            self.carregar_imagens(value)
            self.atualizar_imagem()
        else:
            self.selecionou_disciplina = False

    def extrair_nome_matricula(self, arquivo):
        nome_matricula = os.path.basename(arquivo).replace('.png', '')
        partes = nome_matricula.split('_', 2)

        if len(partes) == 3:
            disciplina = partes[0]
            nome = partes[1]
            matricula = partes[2]
        else:
            disciplina = partes[0]
            nome = "N/A"
            matricula = "N/A"

        return disciplina, nome, matricula

    def update_label_aluno(self):
        if self.imagens:
            disciplina, nome, matricula = self.extrair_nome_matricula(self.imagens[self.imagem_atual_index])
            self.nome_label.text = f"Nome: {nome}"
            self.matricula_label.text = f"Matricula: {matricula}"

    def carregar_imagens(self, disciplina):
        self.imagens = []
        caminho_disciplina = os.path.join('Alunos', disciplina)

        if os.path.exists(caminho_disciplina):
            for item in os.listdir(caminho_disciplina):
                caminho_completo = os.path.join(caminho_disciplina, item)
                if os.path.isfile(caminho_completo) and item.lower().endswith(('.png')):
                    self.imagens.append(caminho_completo)

        if not self.imagens:
            self.imagem_display.source = ''
            self.nome_label.text = "Nome: N/A"
            self.matricula_label.text = "Matricula: N/A"
        else:
            self.imagem_atual_index = 0
            self.atualizar_imagem()

    def atualizar_imagem(self):
        if self.imagens and 0 <= self.imagem_atual_index < len(self.imagens):
            self.imagem_display.source = self.imagens[self.imagem_atual_index]
            self.imagem_display.reload()
            self.update_label_aluno()
        else:
            self.imagem_display.source = ''
            self.nome_label.text = "Nome: N/A"
            self.matricula_label.text = "Matricula: N/A"

    def mudar_imagem_anterior(self, instance):
        if self.selecionou_disciplina and self.imagens:
            if len(self.imagens) > 1:
                self.imagem_atual_index = (self.imagem_atual_index - 1) % len(self.imagens)
            self.atualizar_imagem()

    def mudar_imagem_proxima(self, instance):
        if self.selecionou_disciplina and self.imagens:
            if len(self.imagens) > 1:
                self.imagem_atual_index = (self.imagem_atual_index + 1) % len(self.imagens)
            self.atualizar_imagem()

    def selecionar_disciplina(self, dropdown, input_disciplina):
        def update_text(instance):
            input_disciplina.text = instance.text
            dropdown.dismiss()
        return update_text

    def stop_app(self, instance):
        App.get_running_app().stop()

    def confirmar_exclusao(self, instance):
        if not self.imagens:
            return

        imagem_path = self.imagens[self.imagem_atual_index]

        box = BoxLayout(orientation='vertical', spacing=10, padding=10)
        img = Image(source=imagem_path, size_hint=(1, 0.7))
        path_label = Label(text=f"Diretório: {imagem_path}", size_hint=(1, 0.1))
        botoes = BoxLayout(size_hint=(1, 0.2), spacing=10)

        btn_cancelar = Button(text='Cancelar')
        btn_excluir = Button(text='Excluir')

        botoes.add_widget(btn_cancelar)
        botoes.add_widget(btn_excluir)

        box.add_widget(img)
        box.add_widget(path_label)
        box.add_widget(botoes)

        popup = Popup(title="Confirmar Exclusão", content=box, size_hint=(0.9, 0.9))

        btn_cancelar.bind(on_release=popup.dismiss)

        def excluir_e_atualizar(inst):
            popup.dismiss()
            try:
                os.remove(imagem_path)
            except Exception as e:
                print(f"Erro ao excluir a imagem: {e}")
                return
            self.carregar_imagens(self.disciplina_input.text)
            self.atualizar_imagem()

        btn_excluir.bind(on_release=excluir_e_atualizar)

        popup.open()


class VisualizacaoCadastroApp(App):
    def build(self):
        Window.maximize()
        self.title = 'Instituto Federal Fluminense - Cadastro de Alunos'
        self.icon = 'Imagens/icone_camera.png'
        return VisualizacaoCadastro()


if __name__ == '__main__':
    VisualizacaoCadastroApp().run()
