import datetime as dt
from time import sleep
import sqlite3

conn = sqlite3.connect(r'C:\Users\Mateu\Desktop\pastas\github\Reconhecimento-facial-pca\M-de-Mateus\Reconhecimento'
                       r'-facial-pca\bd\pca.db')
cursor = conn.cursor()

cursor.execute('''UPDATE responsavel SET idchat = {} WHERE cpfresponsavel = '{}''')
for linha in cursor.fetchall():
    print(linha)

'''agora = dt.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
hora_atual = dt.datetime.strptime(str(agora), '%d-%m-%Y %H:%M:%S')
sleep(5)
depois = dt.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
hora_mais_atual = dt.datetime.strptime(str(depois), '%d-%m-%Y %H:%M:%S')
intervalo = hora_mais_atual - hora_atual
print(hora_atual)
print(hora_mais_atual)
print(intervalo)
if dt.timedelta.total_seconds(intervalo) < 10:
    print('ok')'''
