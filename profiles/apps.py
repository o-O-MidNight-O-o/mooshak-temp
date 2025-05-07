from django.apps import AppConfig

class ProfilesConfig(AppConfig):
    name = 'profiles'

    def ready(self):
        import profiles.signals  # This imports the signals.py file
