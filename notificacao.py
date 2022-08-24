import telebot as tb
import sqlite3


bd = r'C:\Users\Mateu\Desktop\pastas\github\Reconhecimento-facial-pca\M-de-Mateus\Reconhecimento-facial-pca\bd\pca.db'

chave_api = 'TOKEN'
bot = tb.TeleBot(chave_api)


def main():
    idchat = None
    data = None
    hora = None
    conn = sqlite3.connect(bd, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''SELECT statusAluno, cpfResponsavel, nomeAluno, matricula FROM aluno''')
    for query in cursor.fetchall():
        try:
            if query[0] == 'chegada':
                cursor.execute(f'''SELECT max(data) FROM registro WHERE matriculaAluno = "{query[3]}"''')
                for horario in cursor.fetchall():
                    date = horario[0]
                    data, hora = date.split(' ', 1)
                cursor.execute(f'''SELECT idChatResponsavel FROM responsavel WHERE cpfResponsavel = "{query[1]}"''')
                for chat in cursor.fetchall():
                    idchat = chat[0]
                bot.send_message(int(idchat), f'Seu filho {query[2]} acaba de chegar na escola! '
                                              f'Dia {data} às {hora}')
                cursor.execute(f'''UPDATE aluno SET statusAluno = "Dentro da escola" WHERE cpfResponsavel = 
                                "{query[1]}"''')
                conn.commit()
            elif query[0] == 'saida':
                cursor.execute(f'''SELECT max(data) FROM registro WHERE matriculaAluno = "{query[3]}"''')
                for horario in cursor.fetchall():
                    date = horario[0]
                    data, hora = date.split(' ', 1)
                cursor.execute(f'''SELECT idChatResponsavel FROM responsavel WHERE cpfResponsavel = "{query[1]}"''')
                for chat in cursor.fetchall():
                    idchat = chat[0]
                bot.send_message(int(idchat), f'Seu filho {query[2]} acaba de sair da escola! Dia {data} às {hora}')
                cursor.execute(
                    f'''UPDATE aluno SET statusAluno = "Fora da escola" WHERE cpfResponsavel = "{query[1]}"''')
                conn.commit()
        except ValueError:
            print('cadastro não ativado!')
    conn.close()


if __name__ == '__main__':
    main()
