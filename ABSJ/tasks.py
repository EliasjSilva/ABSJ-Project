# from celery import shared_task
# from datetime import datetime
# from . import models as m

# @shared_task
# def atualizar_quantidade_dias():
#     data_atual = timezone.now()

#     contribuidores = m.Contribuidor.objects.all()

#     for contribuidor in contribuidores:
#         contribuidor.quantidade_dias = (data_atual.date() - contribuidor.tempo).days
#         contribuidor.save()
