from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        from . import apscheduler_jobs
        apscheduler_jobs.start()
        import core.signals  # 👈 ensures signal is connected






        