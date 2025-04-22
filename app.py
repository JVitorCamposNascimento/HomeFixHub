
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

profissionais = []
servicos = []
cursos = []
orcamentos_keywords = {
    "Vazamento de agua": 80,
    "Torneira quebrada": 50,
    "Tomada derretida": 70,
    "Chuveiro queimado": 60,
    "Registro Hidráulico Quebrado": 90
}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        nome = request.form.get("nome")
        tipo = request.form.get("tipo")
        descricao = request.form.get("descricao")
        preco_estimado = gerar_orcamento(descricao)
        servicos.append({"nome": nome, "tipo": tipo, "descricao": descricao, "preco": preco_estimado})
    return render_template("index.html", servicos=servicos)

@app.route("/profissionais", methods=["GET", "POST"])
def cadastro_profissionais():
    if request.method == "POST":
        nome = request.form.get("nome")
        especialidade = request.form.get("especialidade")
        profissionais.append({"nome": nome, "especialidade": especialidade})
    return render_template("profissionais.html", profissionais=profissionais)

@app.route("/servicos", methods=["GET", "POST"])
def cadastro_servicos():
    if request.method == "POST":
        tipo = request.form.get("tipo")
        descricao = request.form.get("descricao")
        servicos.append({"nome": "Sistema", "tipo": tipo, "descricao": descricao, "preco": gerar_orcamento(descricao)})
    return render_template("servicos.html", servicos=servicos)

@app.route("/cursos", methods=["GET", "POST"])
def cadastro_cursos():
    if request.method == "POST":
        titulo = request.form.get("titulo")
        descricao = request.form.get("descricao")
        cursos.append({"titulo": titulo, "descricao": descricao})
    return render_template("cursos.html", cursos=cursos)

def gerar_orcamento(descricao):
    for palavra, preco in orcamentos_keywords.items():
        if palavra.lower() in descricao.lower():
            return preco
    return 100

if __name__ == "__main__":
    app.run(debug=True)
