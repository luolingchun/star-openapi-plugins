import os.path

from jinja2 import Template
from star_openapi.plugins import BasePlugin
from starlette.responses import HTMLResponse
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles

from .templates import rapidoc_html_string


class RegisterPlugin(BasePlugin):
    def __init__(self):
        self.name = "rapidoc"
        self.display_name = "RapiDoc"
        self.doc_url = "/openapi.json"

    def rapidoc_endpoint(self, request):
        template = Template(request.app.config.get("RAPIDOC_HTML_STRING") or rapidoc_html_string)
        return HTMLResponse(
            content=template.render(
                {
                    "doc_url": self.doc_url,
                    "rapidoc_config": request.app.config.get("RAPIDOC_CONFIG")
                }
            )
        )

    def register(self, doc_url: str) -> list[Route]:
        self.doc_url = doc_url
        static_folder = os.path.join(os.path.dirname(__file__), "templates", "rapidoc")

        routes = [
            Route(
                f"/{self.name}",
                endpoint=self.rapidoc_endpoint
            ),
            Mount("/rapidoc", app=StaticFiles(directory=static_folder), name="static"),
        ]

        return routes
