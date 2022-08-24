import telebot as tb
import sqlite3


bd = r'C:\Users\Mateu\Desktop\pastas\github\Reconhecimento-facial-pca\M-de-Mateus\Reconhecimento-facial-pca\bd\pca.db'

chave_api = '5657476175:AAFWJjKyVwWBDzeP067ocExbPf2cPnQidaI'
bot = tb.TeleBot(chave_api)


@bot.message_handler(commands=['start'])
def envia_mensagem(mensagem):
    bot.send_message(mensagem.chat.id, 'Olá, bem-vindo ao sistema Coderama! Para ativar seu cadastro digite '
                                       '/ativar '
                                       'seguido do seu CPF. Ex.: /ativar 12345678910')


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


bot.polling()
