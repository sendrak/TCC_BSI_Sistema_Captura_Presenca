import face_recognition
import cv2
from kivy.graphics.texture import Texture

class ControleReconhecimento:
    def __init__(self, camera_instance):
        self.capture = cv2.VideoCapture(0)  # Seu código de inicialização da câmera aqui
        self.known_faces = []  # Sua lista de rostos conhecidos aqui
        self.known_names = []  # Sua lista de nomes conhecidos aqui
        self.detected_people = {}  # Dicionário de pessoas detectadas
        self.camera = camera_instance  # A instância da câmera é passada como argumento

    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            face_locations = face_recognition.face_locations(frame)
            face_encodings = face_recognition.face_encodings(frame, face_locations)

            newly_detected_people = set()

            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                matches = face_recognition.compare_faces(self.known_faces, face_encoding)
                if any(matches):
                    face_index = matches.index(True)
                    person_name = self.known_names[face_index]
                    newly_detected_people.add(person_name)
                    if person_name not in self.detected_people:
                        print(f"Face reconhecida na câmera: {person_name}")
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                else:
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            exited_people = set(self.detected_people.keys()) - newly_detected_people
            for person_name in exited_people:
                print(f"{person_name} saiu do alcance da câmera")

            self.detected_people = {person_name: (top, right, bottom, left) for (top, right, bottom, left), person_name in zip(face_locations, newly_detected_people)}

            buffer = cv2.flip(frame, 0).tobytes()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
            self.camera.texture = texture
        else:
            self.camera.source = 'Imagens/no_camera.png'

