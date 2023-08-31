from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    # Create your models here.
    # O "CharField" vai ser um texto e passar a qauntidade máxima de caracteres
    title = models.CharField(max_length=100)
    # O 'blank=True' quer dizer q apessoa pode deixar em branco
    # O "TextField" é a msm coisa do CharField, mas é usado para receber textos maiores
    describe = models.TextField(blank=True)
    # O "DateTimeField" vai ser para deixar registado quando a pessoa criou
    # O null vai armazenar os valores vazios no banco de dados
    created = models.DateTimeField(null=True)
    datecompleted = models.DateTimeField(null=True)
    # No "important" se algo for importante vai ser True, caso contrário vai ser False
    important = models.BooleanField(default=False)
    # No user, basicamente, se um usuário for deletado, todas as suas tarefas serão remmovidas
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title + ' - by: ' + self.user.username
