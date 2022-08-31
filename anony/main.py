from flask import Flask, render_template, request, session, redirect, url_for
import mysql.connector
import random
#from flask_socketio import SocketIO

connect = mysql.connector.connect(host="localhost",
                                  database="anony_db", user="root",
                                  password="META100Kk#")

cursor = connect.cursor(buffered=True)

app = Flask(__name__)
#io = SocketIO(app)
app.secret_key="srct&566"

'''
@io.on("message")
def handle_message(message):
    print("Mensagem recebida: " + message)
    if message != "Usuario conectado!":
        send(message, broadcast=True)
'''
@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/inbox")
def home():
    title = "SELECT Titulo FROM mensagens ORDER BY RAND() LIMIT 1;"
    mensagem = "SELECT Mensagem FROM mensagens ORDER BY RAND() LIMIT 1;"

    conn = mysql.connector.connect(host="localhost",
                                  database="anony_db", user="root",
                                  password="META100Kk#")

    ku = conn.cursor(buffered=True)

    cursor.execute(title)
    ku.execute(mensagem)

    

    title = cursor.fetchone()
    nms2 = [str(i) for i in title]
    ti = str("".join(nms2))

    men = ku.fetchone()
    nms = [str(i) for i in men or []]
    msg = str("".join(nms))

    
    
    return render_template("home.html", ti=ti, msg=msg)                                 


@app.route("/mandar_msg", methods=["GET", "POST"])


def enviar():
    
    if request.method=="POST":
        titulo = request.form["title"]
        texto = request.form["text"]
        cursor.execute("INSERT INTO mensagens(id, Titulo, Mensagem) VALUES(null, %s, %s)", (titulo, texto))

        connect.commit()
        connect.close()

        #msg = "SELECT * FROM mensagens ORDER BY RAND() LIMIT 1;"
        #kur = connect.cursor()
        #kur.execute(msg)
        #nm = kur.fetchone()
        #nms = [str(i) for i in nm]
        #resultados_nome = str("".join(nms))
        #return resultados_nome

        
        
    return render_template("criar.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    msg = ""
    if request.method=="POST":
        emails = request.form["email"]
        senhas = request.form["senha"]
        cursor.execute("SELECT * FROM usuario WHERE email=%s AND senha=%s",(emails, senhas))
        resposta = cursor.fetchone()
        if resposta:
            session["loggedin"] = True
            session["email"] = resposta[1]
            return redirect(url_for("home"))
        else:
            msg="Email/Senha incorretos"
    return render_template("login.html", msg=msg)

#SELECT * FROM mensagens ORDER BY RAND() LIMIT 1; deve aparacer    no inbox
#SELECT * FROM usuario ORDER BY RAND() LIMIT 1; usuario aleatorio
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method=="POST":
        nome=""
        name = request.form["nome"]
        email = request.form["email_sign"]
        senha = request.form["senha_sign"]
        respostas = cursor.execute("INSERT INTO usuario(id, Nome, Email, Senha) VALUES(null, %s, %s, %s)", (name, email, senha))
        connect.commit()
        connect.close()
        #if respostas:
            #session["loggedin"] = True
            #session["name"] = respostas[1]
        return redirect(url_for("home", nome=name))
            
    return render_template("signup.html")


if __name__ == "__main__":
    app.run(debug=True, port="9500")
