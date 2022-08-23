import face_recognition as fr
import warnings
import sqlite3

warnings.simplefilter(action='ignore', category=FutureWarning)
conn = sqlite3.connect(r'C:\Users\Mateu\Desktop\pastas\github\Reconhecimento-facial-pca\M-de-Mateus\Reconhecimento'
                       r'-facial-pca\bd\pca.db')
cursor = conn.cursor()


def reconhece_face(url_foto):
    foto = fr.load_image_file(url_foto)
    rostos = fr.face_encodings(foto)
    if len(rostos) > 0:
        return True, rostos

    return False, []


def get_rostos():
    rostos_conhecidos = []
    nomes_dos_rostos = []
    matricula = []

    cursor.execute('''SELECT pathimagem FROM aluno''')
    for i, rosto in enumerate(cursor.fetchall()):
        if rosto not in rostos_conhecidos:
            face = reconhece_face(rosto[0])
            rostos_conhecidos.append(face[1][0])
            cursor.execute(f'''SELECT nomeAluno FROM aluno WHERE pathimagem = "{rosto[0]}"''')
            for c, nome in enumerate(cursor.fetchall()):
                nomes_dos_rostos.append(nome[c])
            cursor.execute(f'''SELECT matricula FROM aluno WHERE pathimagem = "{rosto[0]}"''')
            for m, matricula_aluno in enumerate(cursor.fetchall()):
                matricula.append(matricula_aluno[m])
    return rostos_conhecidos, nomes_dos_rostos, matricula
