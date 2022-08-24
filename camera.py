import os
import cv2
import sqlite3
import numpy as np
import datetime as dt
import face_recognition as fr
from notificacao import main
from engine import get_rostos
from tempo import intervalo_tempo

# Cria a conexão e o cursor do banco de dados
conn = sqlite3.connect(os.path.relpath(r'bd\pca.db'))
cursor = conn.cursor()

# importa a função do arquivo engine
rostos_conhecidos, nomes_dos_rostos, matricula = get_rostos()


while True:
    # inicia a camera de video
    video_capture = cv2.VideoCapture(0)
    while True:
        # le o frame da camera
        ret, frame = video_capture.read()
        # converte as cores do frame
        rgb_frame = frame[:, :, ::-1]
        # localiza os rostos
        localizacao_dos_rostos = fr.face_locations(rgb_frame)
        # identifica rostos desconhecidos nas fotos
        rosto_desconhecidos = fr.face_encodings(rgb_frame, localizacao_dos_rostos)
        # faz a comparação dos rostos
        for (top, right, bottom, left), rosto_desconhecido in zip(localizacao_dos_rostos, rosto_desconhecidos):
            resultados = fr.compare_faces(rostos_conhecidos, rosto_desconhecido)
            # calcula a distancia das fotos na comparação
            face_distances = fr.face_distance(rostos_conhecidos, rosto_desconhecido)
            # seleciona a melhor distancia
            melhor_id = np.argmin(face_distances)
            if resultados[melhor_id]:
                # retorna o nome do aluno do qual o rosto pertence
                nome = nomes_dos_rostos[melhor_id]
            else:
                nome = "Desconhecido"

            # retangulo
            # Ao redor do rosto
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 139, 139), 2)

            # Embaixo
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 139, 139), cv2.FILLED)
            font = cv2.FONT_HERSHEY_SIMPLEX

            # Texto
            cv2.putText(frame, nome, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            # define o nome que aparece na janela da webcam
            cv2.imshow('Reconhecimento facial', frame)

            try:
                # verifica no index do rosto que pertence ao aluno na lista de rostos
                verificacao = resultados.index(True)
                # retorna a matricula do aluno identificado
                identificador = matricula[verificacao]
                # seleciona o status do aluno
                status = cursor.execute(f'''SELECT statusAluno FROM aluno WHERE matricula = "{identificador}"''')
                for status_atual in cursor.fetchall():
                    status = status_atual[0]
                # seleciona a data do registro mais recente do aluno
                wait = cursor.execute(f'''SELECT max(data) FROM registro WHERE matriculaAluno = "{identificador}"''')
                for pausa in cursor.fetchall():
                    wait = pausa[0]
                # seleciona o cpf do responsavel do aluno
                cpf_responsavel = cursor.execute(f'''SELECT cpfResponsavel FROM aluno
                                     WHERE matricula = "{identificador}"''')
                for cpf in cursor.fetchall():
                    cpf_responsavel = cpf[0]
                # seleciona o nome do aluno
                nome_aluno = cursor.execute(f'''SELECT nomeAluno FROM aluno
                                                     WHERE matricula = "{identificador}"''')
                for aluno in cursor.fetchall():
                    nome_aluno = aluno[0]
                # seleciona o sobrenome do aluno
                sobrenome_aluno = cursor.execute(f'''SELECT sobrenomeAluno FROM aluno
                                                                     WHERE matricula = "{identificador}"''')
                for sobrenome in cursor.fetchall():
                    sobrenome_aluno = sobrenome[0]
                # verifica se o ultimo registro do aluno foi a menos de 10 segundos atrás, para evitar registro
                # duplicado
                # verifica o status do aluno
                if intervalo_tempo(wait) and status == 'Fora da escola':
                    # insere os dados de chegada do aluno a escola
                    cursor.execute(f'''INSERT INTO registro (matriculaAluno, cpfResponsavel, nomeAluno, sobrenomeAluno, 
                    data, direcao) VALUES ("{identificador}", "{cpf_responsavel}", "{nome_aluno}", "{sobrenome_aluno}", 
                    "{dt.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}", "Entrando")''')
                    # muda o status do aluno para de 'Fora da escola' para 'chegada'
                    cursor.execute(f'''UPDATE aluno SET statusAluno = 'chegada' WHERE 
                    matricula = "{identificador}"''')
                    # envia as alterações para o banco de dados
                    conn.commit()
                    # libera a catrata
                    print('Catraca Liberada')
                    # verifica se o ultimo registro do aluno foi a menos de 10 segundos atrás, para evitar registro
                    # duplicado
                    # verifica o status do aluno
                elif intervalo_tempo(wait) and status == 'Dentro da escola':
                    # insere os dados de saida do aluno da escola
                    cursor.execute(f'''INSERT INTO registro (matriculaAluno, cpfResponsavel, nomeAluno, sobrenomeAluno, 
                    data, direcao) VALUES ("{identificador}", "{cpf_responsavel}", "{nome_aluno}", "{sobrenome_aluno}", 
                    "{dt.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}", "Saindo")''')
                    # troca o status do aluno de 'Dentro da escola' para 'saida'
                    cursor.execute(f'''UPDATE aluno SET statusAluno = 'saida' WHERE 
                                        matricula = "{identificador}"''')
                    # envia as alterações para o banco de dados
                    conn.commit()
                    # libera a catrata
                    print('Catraca Liberada')
                # caso o ultimo registro do aluno tenha sido a menos de 10 segundos, o código não faz nada
                else:
                    pass
            except ValueError:
                # caso o rosto identificado não esteja na lista de alunos
                print('Aluno desconhecido!')
        # executa a função de notificação que envia as mensagens para os pais
        main()
        # Ao apertar a leta 'q' do teclado, fecha a janela e quebra o lopping
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # libera a camera de video e quebra o lopping
    video_capture.release()
    cv2.destroyAllWindows()
    break
# fecha a conexão com o banco de dados
conn.close()
