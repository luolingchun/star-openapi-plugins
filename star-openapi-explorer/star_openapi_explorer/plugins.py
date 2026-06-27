import os.path

from jinja2 import Template
from star_openapi.plugins import BasePlugin
from starlette.responses import HTMLResponse
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles

from .templates import explorer_html_string


class RegisterPlugin(BasePlugin):
    def __init__(self):
        self.name = "explorer"
        self.display_name = "Explorer"
        self.doc_url = "/openapi.json"

    def explorer_endpoint(self, request):
        template = Template(request.app.config.get("EXPLORER_HTML_STRING") or explorer_html_string)
        return HTMLResponse(
            content=template.render(
                {
                    "doc_url": self.doc_url,
                    "explorer_config": request.app.config.get("EXPLORER_CONFIG")
                }
            )
        )

    def register(self, doc_url: str) -> list[Route | Mount]:
        self.doc_url = doc_url
        static_folder = os.path.join(os.path.dirname(__file__), "templates", "explorer")

        routes = [
            Route(
                f"/{self.name}",
                endpoint=self.explorer_endpoint
            ),
            Mount("/explorer", app=StaticFiles(directory=static_folder), name="static"),
        ]

        return routes
