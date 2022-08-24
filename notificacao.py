import os
import sqlite3
import telebot as tb

# le o token usado para o bot em um arquivo separado no meu computador
with open(os.path.relpath(r'C:\Users\Mateu\Desktop\token.txt'), 'r', encoding='utf-8') as token:
    chave = token.read()
chave_api = chave
bot = tb.TeleBot(chave_api)

# armazena o caminho do banco de dados
bd = os.path.relpath(r'bd\pca.db')


# Quando executada, consulta todos os status dos alunos
# Caso o status seja igual a 'chegada', envia a mensagem de chegada para os pais
# Caso o status seja igual a 'saida', envia a mensagem de saida para os pais
def main():
    # definindo variaveis locais de apoio
    idchat = None
    data = None
    hora = None
    # cria conexão com o banco de dados (bd)
    conn = sqlite3.connect(bd, check_same_thread=False)
    # cria o cursor que executara as consultas ao bd
    cursor = conn.cursor()
    # consulta os status no bd
    cursor.execute('''SELECT statusAluno, cpfResponsavel, nomeAluno, matricula FROM aluno''')
    # percorre o objeto retornado pela consulta
    for query in cursor.fetchall():
        # tenta executar o primeiro bloco
        try:
            # condição 1 == 'chegada'
            # status do aluno está como 'chegada'
            # query[0] == statusAluno
            if query[0] == 'chegada':
                # seleciona a data do ultimo status do aluno no bd
                cursor.execute(f'''SELECT max(data) FROM registro WHERE matriculaAluno = "{query[3]}"''')
                for horario in cursor.fetchall():
                    # armazena a data na variavel
                    date = horario[0]
                    # separa a data e a hora
                    data, hora = date.split(' ', 1)
                # seleciona o id do chat do telegram do pai do aluno
                cursor.execute(f'''SELECT idChatResponsavel FROM responsavel WHERE cpfResponsavel = "{query[1]}"''')
                for chat in cursor.fetchall():
                    idchat = chat[0]
                # envia a mensagem para o pai do aluno
                bot.send_message(int(idchat), f'Seu filho {query[2]} acaba de chegar na escola! '
                                              f'Dia {data} às {hora}')
                # muda o status do aluno para 'Dentro da escola'
                cursor.execute(f'''UPDATE aluno SET statusAluno = "Dentro da escola" WHERE cpfResponsavel = 
                                "{query[1]}"''')
                conn.commit()
            # condição 1 == 'saida'
            # status do aluno está como 'saida'
            # repete o mesmo processo descrito acima, porém envia uma mensagem notificando a saida do aluno da escola
            # ao final, muda o status do aluno para 'Fora da escola'
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
        # ValueError será retornado quando não houver id do chat do pai do aluno ou quando ele for 0
        # O que ocorre quando o cadastro não é ativado
        except ValueError:
            print('cadastro não ativado!')
    # fecha a conexão com o banco de dados
    conn.close()


if __name__ == '__main__':
    main()
