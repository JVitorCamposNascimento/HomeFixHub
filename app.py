from flask import Flask

app = Flask(__name_)

#rotas 
@app.route("/")
def homepage():
 return "Meu Site No ar !"
app.run()
