from main import app
from flask import render_tamplate

#rotas
@app.route("/")
def homepage():
 return render_tamplate("index.html")