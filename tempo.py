import datetime as dt


def intervalo_tempo(hora_atual):
    try:
        hora_atual = dt.datetime.strptime(str(hora_atual), '%d-%m-%Y %H:%M:%S')
        depois = dt.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        hora_mais_atual = dt.datetime.strptime(str(depois), '%d-%m-%Y %H:%M:%S')
        intervalo = hora_mais_atual - hora_atual
        if dt.timedelta.total_seconds(intervalo) < 10:
            return False
        return True
    except ValueError:
        return True


print(intervalo_tempo(''))
