import os.path

from jinja2 import Template
from star_openapi.plugins import BasePlugin
from starlette.responses import HTMLResponse
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles

from .templates import rapipdf_html_string


class RegisterPlugin(BasePlugin):
    def __init__(self):
        self.name = "rapipdf"
        self.display_name = "RapiPDF"
        self.doc_url = "/openapi.json"

    def rapipdf_endpoint(self, request):
        template = Template(request.app.config.get("RAPIPDF_HTML_STRING") or rapipdf_html_string)
        return HTMLResponse(
            content=template.render(
                {
                    "doc_url": self.doc_url,
                    "rapipdf_config": request.app.config.get("RAPIPDF_CONFIG")
                }
            )
        )

    def register(self, doc_url: str) -> list[Route]:
        self.doc_url = doc_url
        static_folder = os.path.join(os.path.dirname(__file__), "templates", "rapipdf")

        routes = [
            Route(
                f"/{self.name}",
                endpoint=self.rapipdf_endpoint
            ),
            Mount("/rapipdf", app=StaticFiles(directory=static_folder), name="static"),
        ]

        return routes
