from django.db import models
from django.conf import settings

class Dashboard(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    url = models.CharField(max_length=200)
    thumbnail = models.ImageField(upload_to='dashboard_thumbnails/', blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome

class PermissaoDashboard(models.Model):
    dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pode_visualizar = models.BooleanField(default=False)
    pode_editar = models.BooleanField(default=False)

    class Meta:
        unique_together = ('dashboard', 'usuario')

    def __str__(self):
        return f"{self.usuario.username} - {self.dashboard.nome}"