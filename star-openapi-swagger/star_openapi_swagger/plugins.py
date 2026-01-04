import os.path

from jinja2 import Template
from star_openapi.plugins import BasePlugin
from starlette.responses import HTMLResponse
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles

from .templates import swagger_html_string, swagger_oauth2_redirect_html_string


class RegisterPlugin(BasePlugin):
    def __init__(self):
        self.name = "swagger"
        self.display_name = "Swagger"
        self.doc_url = "/openapi.json"

    def swagger_endpoint(self, request):
        template = Template(request.app.config.get("SWAGGER_HTML_STRING") or swagger_html_string)
        return HTMLResponse(
            content=template.render(
                {
                    "doc_url": self.doc_url,
                    "swagger_config": request.app.config.get("SWAGGER_CONFIG"),
                    "oauth_config": request.app.config.get("OAUTH_CONFIG")
                }
            )
        )

    @staticmethod
    def oauth2_endpoint(_request):
        template = Template(swagger_oauth2_redirect_html_string)
        return HTMLResponse(
            content=template.render()
        )

    def register(self, doc_url: str) -> list[Route]:
        self.doc_url = doc_url
        static_folder = os.path.join(os.path.dirname(__file__), "templates", "swagger")

        routes = [
            Route(
                f"/{self.name}",
                endpoint=self.swagger_endpoint
            ),
            Route(
                f"/oauth2-redirect.html",
                endpoint=self.oauth2_endpoint
            ),
            Mount("/swagger", app=StaticFiles(directory=static_folder), name="static"),
        ]

        return routes
