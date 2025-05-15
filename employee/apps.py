from django.apps import AppConfig

class EmployeeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'employee'
class StateConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'state'