from jinja2 import Environment, FileSystemLoader

from src.settings import path_settings


env = Environment(loader=FileSystemLoader('core/templates'))

class EmailService:
    def __init__(self):
        self.env = env
    
    def render_email_template(self, token: str, template_name: str, path: str) -> str:
        template = self.env.get_template(template_name)
        verify_link = f"{path_settings.BASE_URL}{path}?token={token}"

        return template.render(verify_link=verify_link)