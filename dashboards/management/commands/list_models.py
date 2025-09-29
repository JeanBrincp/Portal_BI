from django.core.management.base import BaseCommand
from django.conf import settings
import google.generativeai as genai

class Command(BaseCommand):
    help = 'Lists the available Gemini models for the configured API key.'

    def handle(self, *args, **options):
        api_key = getattr(settings, 'GEMINI_API_KEY', None)
        if not api_key or api_key == 'COLOQUE_SUA_CHAVE_API_AQUI':
            self.stdout.write(self.style.ERROR('ERROR: Gemini API key is not configured in settings.py.'))
            return

        try:
            genai.configure(api_key=api_key)
            self.stdout.write("Modelos disponíveis que suportam 'generateContent':")
            found_model = False
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    self.stdout.write(f'- {m.name}')
                    found_model = True
            if not found_model:
                self.stdout.write(self.style.WARNING('Nenhum modelo encontrado.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ocorreu um erro: {e}'))
