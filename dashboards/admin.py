from django.contrib import admin
from .models import Dashboard, PermissaoDashboard

@admin.register(Dashboard)
class DashboardAdmin(admin.ModelAdmin):
    list_display = ('nome', 'criado_em')
    search_fields = ('nome',)

@admin.register(PermissaoDashboard)
class PermissaoDashboardAdmin(admin.ModelAdmin):
    list_display = ('dashboard', 'usuario', 'pode_visualizar', 'pode_editar')
    search_fields = ('dashboard__nome', 'usuario__username')
    list_filter = ('pode_visualizar', 'pode_editar')
    autocomplete_fields = ('dashboard', 'usuario') # Melhora a usabilidade para muitos usuários/dashboards
