import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseForbidden, JsonResponse
from django.db.models import Q
from .models import Dashboard, PermissaoDashboard
from django.conf import settings
import google.generativeai as genai

def logout_view(request):
    logout(request)
    return redirect('/')

def login_view(request):
    if request.method == "POST":
        username_from_form = request.POST.get('username')
        password_from_form = request.POST.get('password')
        
        user = authenticate(request, username=username_from_form, password=password_from_form)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html')
            
    return render(request, 'login.html')

def home_view(request):
    return render(request, 'home.html')

def dashboards_view(request):
    query = request.GET.get('q', '')
    dashboards_list = Dashboard.objects.filter(
        permissaodashboard__usuario=request.user, 
        permissaodashboard__pode_visualizar=True
    ).distinct()

    if query:
        dashboards_list = dashboards_list.filter(
            Q(nome__icontains=query) | Q(descricao__icontains=query)
        )

    context = {
        'dashboards': dashboards_list,
        'query': query,
    }
    return render(request, 'dashboards.html', context)

@login_required
def view_dashboard(request, dashboard_id):
    dashboard = get_object_or_404(Dashboard, id=dashboard_id)
    
    has_permission = PermissaoDashboard.objects.filter(
        usuario=request.user, 
        dashboard=dashboard,
        pode_visualizar=True
    ).exists()

    if not has_permission and not request.user.is_superuser:
        return HttpResponseForbidden("Você não tem permissão para ver este dashboard.")
        
    context = {
        'dashboard': dashboard
    }
    return render(request, 'view_dashboard.html', context)

def ask_ai_view(request):
    if request.method == 'POST':
        api_key = getattr(settings, 'GEMINI_API_KEY', None)
        if not api_key or api_key == 'COLOQUE_SUA_CHAVE_API_AQUI':
            return JsonResponse({'response': 'ERRO: A chave da API do Gemini não foi configurada no settings.py.'})

        try:
            # 1. Get user's message
            data = json.loads(request.body)
            message = data.get('message')
            if not message:
                return JsonResponse({'error': 'Nenhuma mensagem recebida.'}, status=400)

            # 2. Get user's accessible dashboards
            dashboards = Dashboard.objects.filter(
                permissaodashboard__usuario=request.user,
                permissaodashboard__pode_visualizar=True
            ).distinct()

            dashboard_list_str = "\n".join([f"- Nome: {d.nome}, Descrição: {d.descricao}, URL: /dashboards/{d.id}/" for d in dashboards])

            # 3. Create the system prompt
            system_prompt = f'''Você é um assistente prestativo em um portal de BI.
            Aqui está uma lista de dashboards disponíveis para o usuário:
            {dashboard_list_str}

            Se o usuário pedir para ver um dashboard ou fizer uma pergunta que pode ser respondida navegando para um, sua resposta DEVE ser apenas um objeto JSON no seguinte formato:
            {{"action": "navigate", "url": "URL_DO_DASHBOARD"}}

            Se a pergunta do usuário for geral e não puder ser respondida com um dashboard, responda normalmente como um assistente prestativo.
            '''

            # 4. Call the AI
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(
                model_name='gemini-2.5-flash',
                system_instruction=system_prompt
            )
            response = model.generate_content(message)

            # 5. Check if the response is a navigation command
            try:
                # Attempt to parse the response as JSON
                potential_json = json.loads(response.text)
                if isinstance(potential_json, dict) and potential_json.get('action') == 'navigate':
                    # It's a navigation command, forward it to the frontend
                    return JsonResponse(potential_json)
            except json.JSONDecodeError:
                # It's not JSON, so it's a regular text response
                pass

            # 6. Return regular text response
            return JsonResponse({'response': response.text})

        except Exception as e:
            return JsonResponse({'error': f'Ocorreu um erro no servidor: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Apenas requisições POST são permitidas.'}, status=405)

@staff_member_required
def grant_bulk_permissions_view(request):
    User = get_user_model()
    if request.method == 'POST':
        user_id = request.POST.get('user')
        dashboard_ids = request.POST.getlist('dashboards')

        if user_id and dashboard_ids:
            user = User.objects.get(id=user_id)
            for dash_id in dashboard_ids:
                dashboard = Dashboard.objects.get(id=dash_id)
                PermissaoDashboard.objects.update_or_create(
                    usuario=user,
                    dashboard=dashboard,
                    defaults={'pode_visualizar': True}
                )
            return redirect('admin:index')

    users = User.objects.all()
    dashboards = Dashboard.objects.all().order_by('nome')
    context = {
        'users': users,
        'dashboards': dashboards,
        'title': 'Conceder Permissões em Massa'
    }
    return render(request, 'admin/grant_bulk_permissions.html', context)
