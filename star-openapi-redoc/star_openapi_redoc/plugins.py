import os.path

from jinja2 import Template
from star_openapi.plugins import BasePlugin
from starlette.responses import HTMLResponse
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles

from .templates import redoc_html_string


class RegisterPlugin(BasePlugin):
    def __init__(self):
        self.name = "redoc"
        self.display_name = "Redoc"
        self.doc_url = "/openapi.json"

    def redoc_endpoint(self, request):
        template = Template(request.app.config.get("REDOC_HTML_STRING") or redoc_html_string)
        return HTMLResponse(
            content=template.render(
                {
                    "doc_url": self.doc_url,
                    "redoc_config": request.app.config.get("REDOC_CONFIG")
                }
            )
        )

    def register(self, doc_url: str) -> list[Route]:
        self.doc_url = doc_url
        static_folder = os.path.join(os.path.dirname(__file__), "templates", "redoc")

        routes = [
            Route(
                f"/{self.name}",
                endpoint=self.redoc_endpoint
            ),
            Mount("/redoc", app=StaticFiles(directory=static_folder), name="static"),
        ]

        return routes
