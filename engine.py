import os
import sqlite3
import warnings
import face_recognition as fr

warnings.simplefilter(action='ignore', category=FutureWarning)


# codifica as fotos e localiza os rostos
def reconhece_face(url_foto):
    foto = fr.load_image_file(url_foto)
    rostos = fr.face_encodings(foto)
    if len(rostos) > 0:
        return True, rostos

    return False, []


# seleciona os rotos nas fotos do bd e armazena em uma lista de rostos conhecidos
# junto com o nome e a matricula do aluno
def get_rostos():
    rostos_conhecidos = []
    nomes_dos_rostos = []
    matricula = []

    # cria conexão com o banco de dados (bd)
    conn = sqlite3.connect(os.path.relpath(r'bd\pca.db'))
    # cria o cursor que executara as consultas ao bd
    cursor = conn.cursor()

    # seleciona a imagem de todos os alunos
    cursor.execute('''SELECT pathimagem FROM aluno''')
    for i, rosto in enumerate(cursor.fetchall()):
        # identifica os rostos nas fotos e os adiciona em uma lista
        if rosto not in rostos_conhecidos:
            face = reconhece_face(rosto[0])
            rostos_conhecidos.append(face[1][0])
            # seleciona o nome do aluno e o adiciona em uma lista
            cursor.execute(f'''SELECT nomeAluno FROM aluno WHERE pathimagem = "{rosto[0]}"''')
            for c, nome in enumerate(cursor.fetchall()):
                nomes_dos_rostos.append(nome[c])
            # seleciona a matricula do aluno e adiciona em uma lista
            cursor.execute(f'''SELECT matricula FROM aluno WHERE pathimagem = "{rosto[0]}"''')
            for m, matricula_aluno in enumerate(cursor.fetchall()):
                matricula.append(matricula_aluno[m])
    # fecha a conexão com o banco de dados
    conn.close()
    return rostos_conhecidos, nomes_dos_rostos, matricula
