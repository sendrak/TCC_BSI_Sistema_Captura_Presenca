import os


class helper_busca_disciplinas:
    def __init__(self, caminho_pasta='Alunos'):
        self.caminho_pasta = caminho_pasta

    def lista_de_disciplinas_cadastradas(self):
        lista_disciplinas = []

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

    def selecionar_disciplina(self, dropdown, text_input):
        def update_text(instance):
            text_input.text = instance.text
            dropdown.dismiss()  # Fecha o dropdown

        return update_text
