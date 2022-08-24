import datetime as dt


def intervalo_tempo(hora_atual, pausa=10):
    try:
        # converte a hora para um formato que me permite fazer expressões matematicas
        hora_atual = dt.datetime.strptime(str(hora_atual), '%d-%m-%Y %H:%M:%S')
        # retorna a hora atual em que a função foi executada
        depois = dt.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        # converte a hora para um formato que me permite fazer expressões matematicas
        hora_mais_atual = dt.datetime.strptime(str(depois), '%d-%m-%Y %H:%M:%S')
        # calcula a diferença de tempo entre uma hora e outra
        intervalo = hora_mais_atual - hora_atual
        # faz a comparação de quantos segundos possui essa diferença
        if dt.timedelta.total_seconds(intervalo) < pausa:
            # pausa padrão 10s, mas pode ser alterada pelo usuario
            # retorna falso se o intervalo for menor que a pausa definida
            return False
        # retorna True caso o intervalo de tempo seja maior que a pausa definida
        return True
    # retorna ValueError se o aluno ainda não tiver nenhum registro no banco
    except ValueError:
        # retorna True para permitir a criação do primeiro registro
        return True
