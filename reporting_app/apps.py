from django.apps import AppConfig


class ReportingAppConfig(AppConfig):
    name = 'reporting_app'

    def ready(self):
        from reporting_app import updater
        updater.start()