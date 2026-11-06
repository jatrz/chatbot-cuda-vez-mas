"""Punto de entrada de CUDA Vez Más Chatbot."""

from flask import Flask, render_template

from api.routes import api_bp

app = Flask(__name__)
app.register_blueprint(api_bp)


@app.get("/")
def index():
    """Muestra la página principal del chatbot."""
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
