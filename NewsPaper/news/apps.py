from django.apps import AppConfig


class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'

    def ready(self):
        # файлы models.py, urls.py автоматически цепляются к проекту самим django. Чтобы подцепить (выполнить) другие файлы, нужно прописать их здесь
        import news.signals
