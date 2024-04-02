import os
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.properties import StringProperty

Builder.load_string('''
<VisualizadorImagens>:
    BoxLayout:
        orientation: 'vertical'

        Image:
            id: image_view
            source: root.current_image
            size_hint_y: 0.8

        Label:
            id: image_name_label
            text: root.current_filename
            size_hint_y: 0.1

        BoxLayout:
            size_hint_y: 0.1

            Button:
                text: 'Anterior'
                on_press: root.show_previous_image()

            Button:
                text: 'Próximo'
                on_press: root.show_next_image()

            Button:
                text: 'Excluir Cadastro'
                on_press: root.show_delete_confirmation_popup()

            Button:
                text: 'Fechar'
                on_press: app.stop()

<DeleteConfirmationContent>:
    orientation: 'vertical'
    Image:
        id: delete_image_view
        source: root.current_image
    Label:
        id: delete_image_name_label
        text: root.current_filename
    Button:
        text: 'Excluir Cadastro'
        id: confirm_button
    Button:
        text: 'Cancelar'
        id: cancel_button

<NoImagesContent>:
    orientation: 'vertical'
    Label:
        text: 'Não existe imagem cadastrada no Banco de Imagens'
    Button:
        text: 'Ok'
        id: ok_button
''')


class DeleteConfirmationContent(BoxLayout):
    current_image = StringProperty("")  # Adicione essa propriedade
    current_filename = StringProperty("")  # Adicione essa propriedade

    def __init__(self, **kwargs):
        super(DeleteConfirmationContent, self).__init__(**kwargs)
        self.ids.delete_image_view.source = self.current_image
        self.ids.delete_image_name_label.text = self.current_filename


class NoImagesContent(BoxLayout):
    pass

class VisualizadorImagens(BoxLayout):
    image_files = []

    def __init__(self, **kwargs):
        super(VisualizadorImagens, self).__init__(**kwargs)
        self.load_images_from_directory("./Pessoas")
        self.current_index = 0
        self.update_image()  # Exibe a primeira imagem ao iniciar o programa

    @property
    def current_image(self):
        if len(self.image_files) > 0:
            return self.image_files[self.current_index]
        else:
            return ""

    @property
    def current_filename(self):
        if len(self.image_files) > 0:
            return os.path.basename(self.current_image)
        else:
            return ""

    def load_images_from_directory(self, directory):
        for filename in os.listdir(directory):
            if filename.endswith(".png"):
                self.image_files.append(os.path.join(directory, filename))
        self.image_files = sorted(self.image_files)

    def show_previous_image(self):
        if len(self.image_files) > 0:
            if self.current_index > 0:
                self.current_index -= 1
            else:
                self.current_index = len(self.image_files) - 1
            self.update_image()

    def show_next_image(self):
        if len(self.image_files) > 0:
            if self.current_index < len(self.image_files) - 1:
                self.current_index += 1
            else:
                self.current_index = 0
            self.update_image()

    def show_delete_confirmation_popup(self):
        if len(self.image_files) > 0:
            content = DeleteConfirmationContent(current_image=self.current_image,
                                                current_filename=self.current_filename)
            popup = Popup(title='Excluir Foto', content=content, size_hint=(0.6, 0.6))
            content.ids.confirm_button.bind(on_release=lambda x: self.delete_current_image(popup))
            content.ids.cancel_button.bind(on_release=popup.dismiss)
            popup.open()
        else:
            content = NoImagesContent()
            popup = Popup(title='Aviso', content=content, size_hint=(0.6, 0.3))
            content.ids.ok_button.bind(on_release=popup.dismiss)
            popup.open()

    def delete_current_image(self, popup):
        os.remove(self.current_image)
        self.image_files.pop(self.current_index)
        if self.current_index >= len(self.image_files):
            self.current_index = max(len(self.image_files) - 1, 0)
        self.update_image()
        popup.dismiss()

    def update_image(self, *args):
        if len(self.image_files) > 0:
            self.ids['image_view'].source = self.current_image
            self.ids['image_name_label'].text = self.current_filename
        else:
            self.ids['image_view'].source = ""
            self.ids['image_name_label'].text = ""


class VisualizadorImagensApp(App):
    def build(self):
        self.title = 'Instituto Federal Fluminense - Banco de Imagens'
        self.icon = 'Imagens/icone_camera.png'
        return VisualizadorImagens()


if __name__ == '__main__':
    VisualizadorImagensApp().run()
