from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from reactpy.backend.fastapi import configure
from reactpy import html
from backend import app as backend_app
from frontend import RecomendacionForm
from bootstrap import BootstrapCSS

# Crear instancia principal de la aplicación FastAPI
app = FastAPI()

# Montar la aplicación de backend
app.mount("/api", backend_app)

app.mount("/static", StaticFiles(directory="static"), name="static")

# Configurar FastAPI con el componente ReactPy
configure(
    app, 
    component=lambda: html.div(
        html.link({"rel": "stylesheet", "href": "/static/style.css"}), 
        BootstrapCSS(), 
        RecomendacionForm()
    )
)