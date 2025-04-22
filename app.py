from flask import Flask

app = Flask(__name_)

#rotas 
@app.route("/")
def homepage():
 return "Meu Site No ar !"

if __name__ == "__app__":
app.run()
