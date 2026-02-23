from django.apps import AppConfig

class EmployeeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'employee'
class StateConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'state'
class AccountsAppConfig(AppConfig):
    name = 'accounts'
class PostsAppConfig(AppConfig):
    name = 'posts'  
class CommentsAppConfig(AppConfig):
    name = 'comments'
class AnalyticsAppConfig(AppConfig):
    name = 'analytics_dashboard'
