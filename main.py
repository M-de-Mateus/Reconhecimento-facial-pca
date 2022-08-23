import numpy as np
import face_recognition as fr
import cv2
from engine import get_rostos
import sqlite3
import datetime as dt
from tempo import intervalo_tempo
import telebot as tb

conn = sqlite3.connect(r'C:\Users\Mateu\Desktop\pastas\github\Reconhecimento-facial-pca\M-de-Mateus\Reconhecimento'
                       r'-facial-pca\bd\pca.db')
cursor = conn.cursor()
rostos_conhecidos, nomes_dos_rostos, matricula = get_rostos()

while True:
    video_capture = cv2.VideoCapture(0)
    while True:
        ret, frame = video_capture.read()

        rgb_frame = frame[:, :, ::-1]

        localizacao_dos_rostos = fr.face_locations(rgb_frame)
        rosto_desconhecidos = fr.face_encodings(rgb_frame, localizacao_dos_rostos)

        for (top, right, bottom, left), rosto_desconhecido in zip(localizacao_dos_rostos, rosto_desconhecidos):
            resultados = fr.compare_faces(rostos_conhecidos, rosto_desconhecido)

            face_distances = fr.face_distance(rostos_conhecidos, rosto_desconhecido)

            melhor_id = np.argmin(face_distances)
            if resultados[melhor_id]:
                nome = nomes_dos_rostos[melhor_id]
            else:
                nome = "Desconhecido"

            # Ao redor do rosto
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Embaixo
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_SIMPLEX

            # Texto
            cv2.putText(frame, nome, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            cv2.imshow('Webcam_facerecognition', frame)
            try:
                verificacao = resultados.index(True)
                identificador = matricula[verificacao]
                status = cursor.execute(f'''SELECT statusAluno FROM aluno WHERE matricula = "{identificador}"''')
                for status_atual in cursor.fetchall():
                    status = status_atual[0]
                wait = cursor.execute(f'''SELECT data FROM registro WHERE matriculaAluno = "{identificador}"''')
                for pausa in cursor.fetchall():
                    wait = pausa[0]
                cpf_responsavel = cursor.execute(f'''SELECT cpfResponsavel FROM aluno
                                     WHERE matricula = "{identificador}"''')
                for cpf in cursor.fetchall():
                    cpf_responsavel = cpf[0]
                nome_aluno = cursor.execute(f'''SELECT nomeAluno FROM aluno
                                                     WHERE matricula = "{identificador}"''')
                for aluno in cursor.fetchall():
                    nome_aluno = aluno[0]
                sobrenome_aluno = cursor.execute(f'''SELECT sobrenomeAluno FROM aluno
                                                                     WHERE matricula = "{identificador}"''')
                for sobrenome in cursor.fetchall():
                    sobrenome_aluno = sobrenome[0]
                if intervalo_tempo(wait) and status == 'Fora da escola':
                    cursor.execute(f'''INSERT INTO registro (matriculaAluno, cpfResponsavel, nomeAluno, sobrenomeAluno, 
                    data, direcao) VALUES ("{identificador}", "{cpf_responsavel}", "{nome_aluno}", "{sobrenome_aluno}", 
                    "{dt.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}", "Entrando")''')
                    cursor.execute(f'''UPDATE aluno SET statusAluno = 'Dentro da escola' WHERE 
                    matricula = "{identificador}"''')
                    conn.commit()
                    print('Catraca Liberada')
                elif intervalo_tempo(wait) and status == 'Dentro da escola':
                    cursor.execute(f'''INSERT INTO registro (matriculaAluno, cpfResponsavel, nomeAluno, sobrenomeAluno, 
                    data, direcao) VALUES ("{identificador}", "{cpf_responsavel}", "{nome_aluno}", "{sobrenome_aluno}", 
                    "{dt.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}", "Entrando")''')
                    cursor.execute(f'''UPDATE aluno SET statusAluno = 'Fora da escola' WHERE 
                                        matricula = "{identificador}"''')
                    conn.commit()
                    print('Catraca Liberada')
                else:
                    pass
            except ValueError:
                print('Aluno desconhecido!')

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
    break
conn.close()
