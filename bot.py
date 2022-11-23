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


# Ativa uma função quando o bot recebe o comando /start
# A função envia instruções para o usuário
@bot.message_handler(commands=['start'])
def envia_mensagem(mensagem):
    bot.send_message(mensagem.chat.id, 'Olá, bem-vindo ao sistema Coderama! Para ativar seu cadastro digite '
                                       '/ativar '
                                       'seguido do seu CPF. Ex.: /ativar 12345678910')


# Ativa uma função quando o bot recebe o comando /ativar
# A função registra o id do chat do telegram do usuário e com isso ele recebe notificações
@bot.message_handler(commands=['ativar'])
def ativa_cadastro(mensagem):
    conn = sqlite3.connect(bd, check_same_thread=False)
    cursor = conn.cursor()
    try:
        msg = mensagem.text
        cmd, cpf = msg.split(" ", 1)
        if len(cpf) != 11:
            bot.send_message(mensagem.chat.id, 'Não consegui encontrar o seu CPF, verifique se o digitou corretamente!')
        else:
            cursor.execute(f'''SELECT cpfResponsavel FROM responsavel WHERE cpfResponsavel = "{cpf}"''')
            for linha in cursor.fetchall():
                if cpf not in str(linha[0]):
                    bot.send_message(mensagem.chat.id,
                                     'Não consegui encontrar o seu CPF, entre em contato com a escola e '
                                     'verifique seu cadastro!')
                    conn.close()
                else:
                    cursor.execute(
                        f'''UPDATE responsavel SET idChatResponsavel = "{mensagem.chat.id}" WHERE 
                        cpfResponsavel = "{cpf}"''')
                    conn.commit()
                    bot.send_message(mensagem.chat.id, 'Cadastro ativado com sucesso, agora você receberá notificações '
                                                       'quando seu filho entrar ou sair da escola!')
                    bot.send_message(mensagem.chat.id, 'Para mais comandos digite /comandos')
                    conn.close()
    except ValueError:
        bot.send_message(mensagem.chat.id, 'Digite o CPF após o comando! (Ex.: /ativar 11122233345)')


# Ativa uma função quando o bot recebe o comando /desativar
# A função troca o id do chat do usuário pelo valor 0, com isso o usuário não recebe mais notificações
@bot.message_handler(commands=['desativar'])
def desativa_cadastro(mensagem):
    conn = sqlite3.connect(bd, check_same_thread=False)
    cursor = conn.cursor()
    try:
        msg = mensagem.text
        cmd, cpf = msg.split(" ", 1)
        if len(cpf) != 11:
            bot.send_message(mensagem.chat.id, 'Não consegui encontrar o seu CPF, verifique se o digitou corretamente!')
        else:
            cursor.execute(f'''SELECT cpfResponsavel FROM responsavel WHERE cpfResponsavel = "{cpf}"''')
            for linha in cursor.fetchall():
                if cpf not in str(linha[0]):
                    bot.send_message(mensagem.chat.id,
                                     'Não consegui encontrar o seu CPF, entre em contato com a escola e '
                                     'verifique seu cadastro!')
                    conn.close()
                else:
                    cursor.execute(
                        f'''UPDATE responsavel SET idChatResponsavel = "{0}" WHERE 
                        cpfResponsavel = "{cpf}"''')
                    conn.commit()
                    bot.send_message(mensagem.chat.id, 'Cadastro desativado com sucesso, agora você não receberá '
                                                       'notificações '
                                                       'quando seu filho entrar ou sair da escola!')
                    bot.send_message(mensagem.chat.id, 'Para mais comandos digite /comandos')
                    conn.close()
    except ValueError:
        bot.send_message(mensagem.chat.id, 'Digite o CPF após o comando! (Ex.: /desativar 11122233345)')


bot.polling()
