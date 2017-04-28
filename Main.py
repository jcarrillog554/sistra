from flask import Flask, render_template, request, url_for, redirect
from passlib.handlers.sha2_crypt import sha256_crypt
import psycopg2, time, networkx as nx

hostname = 'localhost'
username = 'jonathan'
password = '123'
database = 'postgres'

myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )

myConnection.close()
conn_string = "host='%s' dbname='%s' user='%s' password='%s' port='%i'" \
              % (hostname, database, username, password, 5432)

class valores:
    origen = 0
    destino = 0
    usuarioActual=""
    Grafo = nx.Graph()
    Grafo.add_nodes_from(['Arenal','Dominical','Monteverde','Tortuguero','PJimenez','RinconDeLaVieja','VolcanBarva','Bijagua','PuertoViejoH','TBD','PaloVerde','Barbilla','Quetzales','Uvita','Tapanti','VolcanTenorio','PuertoViejoT','Chirripo','SantaRosa','LaAmistad','Gandoca','CanoNegro','BraulioCarrillo','BarraHonda'])
    Grafo.add_edges_from([('Arenal', 'Monteverde',{'weight':107}), ('Arenal', 'VolcanTenorio', {'weight':72}), ('Dominical', 'Quetzales', {'weight':96}), ('Dominical', 'Uvita', {'weight':18}),
                ('Monteverde', 'PaloVerde', {'weight':110}), ('Monteverde', 'VolcanBarva', {'weight':148}), ('Tortuguero', 'PuertoViejoH', {'weight':88}), ('Tortuguero', 'BraulioCarrillo', {'weight':71}),
                ('PJimenez', 'Uvita', {'weight':150}), ('PJimenez', 'LaAmistad', {'weight':390}), ('RinconDeLaVieja', 'Bijagua', {'weight':134}), ('RinconDeLaVieja', 'SantaRosa', {'weight':52}),
                ('VolcanBarva', 'PuertoViejoH', {'weight':87}), ('VolcanBarva', 'BraulioCarrillo', {'weight':50}), ('Bijagua', 'CanoNegro', {'weight':175}), ('Bijagua', 'VolcanTenorio', {'weight':20}),
                ('PuertoViejoH', 'VolcanBarva', {'weight':87}), ('PuertoViejoH', 'BraulioCarrillo', {'weight':47}), ('TBD', 'Gandoca', {'weight':185}), ('TBD', 'LaAmistad', {'weight':250}),
                ('PaloVerde', 'BarraHonda', {'weight':76}), ('PaloVerde', 'RinconDeLaVieja', {'weight':69}), ('Barbilla', 'Tapanti', {'weight':97}), ('Barbilla', 'BraulioCarrillo', {'weight':84}),
                ('Quetzales', 'Chirripo', {'weight':120}),('Quetzales', 'Tapanti', {'weight':100}), ('Uvita', 'Quetzales', {'weight':100}), ('Uvita', 'Chirripo', {'weight':130}),
                ('Tapanti', 'BraulioCarrillo', {'weight':87}), ('VolcanTenorio', 'RinconDeLaVieja', {'weight':94}),('PuertoViejoT', 'Chirripo', {'weight':220}), ('PuertoViejoT', 'LaAmistad', {'weight':41}),
                ('SantaRosa', 'PaloVerde', {'weight':90}), ('LaAmistad', 'Gandoca', {'weight':28}), ('LaAmistad', 'Chirripo', {'weight':220}), ('CanoNegro', 'Arenal', {'weight':112}),])



app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template("main.html")

@app.route('/dashboard/' , methods=['GET', 'POST'])
def dashboard():

    if valores.usuarioActual != "":
        return render_template("dashboard.html",data = {"Origen": [{'name': 'Arenal'},
                       {'name': 'Dominical'},
                       {'name': 'Monteverde'},
                       {'name': 'Tortuguero'},
                       {'name': 'PJimenez'},
                       {'name': 'RinconDeLaVieja'},
                       {'name': 'VolcanBarva'},
                       {'name': 'Bijagua'},
                       {'name': 'PuertoViejoH'},
                       {'name': 'PaloVerde'},
                       {'name': 'Barbilla'},
                       {'name': 'Quetzales'},
                       {'name': 'Uvita'},
                       {'name': 'Tapanti'},
                       {'name': 'VolcanTenorio'},
                       {'name': 'PuertoViejoT'},
                       {'name': 'Chirripo'},
                       {'name': 'SantaRosa'},
                       {'name': 'LaAmistad'},
                       {'name': 'Gandoca'},
                       {'name': 'CanoNegro'},
                       {'name': 'BraulioCarrillo'},
                       {'name': 'BarraHonda'}],

            "Transporte": [{'name': 'Avion'},
                           {'name': 'Taxi'},
                           {'name': 'Bus'},
                           {'name': 'Tren'}],
            }
)
    else:
        return redirect(url_for('login'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

@app.errorhandler(405)
def method_not_found(e):
    return render_template("405.html")

@app.errorhandler(500)
def programer_error(e):
        return render_template("500.html", error=e)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    error = ''
    conn = psycopg2.connect(conn_string)
    conn2 = psycopg2.connect(conn_string)

    try:
        if request.method == "POST":
            attempted_username = request.form['username']
            attempted_password = request.form['password']

            cursor = conn.cursor()
            cursor2 = conn2.cursor()

            salida = ""
            salida2 = ""

            cursor.execute("SELECT nombre FROM usuario where nombre = (%s)", [request.form['username']])
            cursor2.execute("SELECT password FROM usuario where nombre = (%s)", [request.form['username']])

            for row in cursor:
                salida += str(row[0])
            for row in cursor2:
                salida2 += str(row[0])

            if attempted_username == salida and sha256_crypt.verify(attempted_password, salida2):
                valores.usuarioActual = salida
                return redirect((url_for('dashboard')))

            else:
                error = "Invalid Credentials. Please try again"
        return render_template("login.html", error = error)

    except Exception as e:
            return render_template("login.html", error = error)


@app.route('/register/', methods=['GET', 'POST'])
def registro():
    error = ''
    conn = psycopg2.connect(conn_string)
    salida = ''
    try:
        if request.method == "POST":
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            passwordEncrypt = sha256_crypt.encrypt(password)
            confirm = request.form['confirm']
            cursor = conn.cursor()
            if password == confirm:
                cursor.execute("INSERT into usuario (nombre, email, password) values (%s, %s, %s)",
                               [str(username), str(email), str(passwordEncrypt)])
                conn.commit()
                cursor.execute("SELECT nombre FROM usuario where nombre = (%s)", [request.form['username']])
                for row in cursor:
                    salida += str(row[0])
                valores.usuarioActual = salida
                return redirect((url_for('dashboard')))
            else:
                error = "Password does not match each other, please try again"
        return render_template("registro.html", error=error)

    except Exception as e:
        return render_template("registro.html", error=error)


def Avion(origen,destino):
    error = ''
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()

    cursor.execute("INSERT into log (usuario, fecha, accion) values (%s, %s, %s)",
                               [valores.usuarioActual, time.strftime('%d-%m-%Y_%H:%M:%S'), "escogio_destino_dominical"])
    conn.commit()
    mejor_ruta = nx.dijkstra_path(valores.Grafo, origen, destino)
    peso = nx.dijkstra_path_length(valores.Grafo, origen, destino)
    precio = 530 + (530*peso*1.5)
    return render_template("Avion.html",mejor_ruta = mejor_ruta, peso = peso, precio = precio)

def Taxi(origen,destino):
    error = ''
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    cursor.execute("INSERT into log (usuario, fecha, accion) values (%s, %s, %s)",
                               [valores.usuarioActual, time.strftime('%d-%m-%Y_%H:%M:%S'), "escogio_destino_dominical"])
    conn.commit()
    mejor_ruta = nx.dijkstra_path(valores.Grafo, origen, destino)
    peso = nx.dijkstra_path_length(valores.Grafo, origen, destino)
    precio = 530 + (530*peso)
    return render_template("Taxi.html", mejor_ruta=mejor_ruta, peso=peso, precio = precio)


def Bus(origen,destino):
    error = ''
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    cursor.execute("INSERT into log (usuario, fecha, accion) values (%s, %s, %s)",
                               [valores.usuarioActual, time.strftime('%d-%m-%Y_%H:%M:%S'), "escogio_destino_dominical"])
    conn.commit()
    mejor_ruta = nx.dijkstra_path(valores.Grafo, origen, destino)
    peso = nx.dijkstra_path_length(valores.Grafo, origen, destino)
    precio = 300 + (530 * peso/6)
    return render_template("Bus.html", mejor_ruta=mejor_ruta, peso=peso, precio = precio)

def Tren(origen,destino):
    error = ''
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    cursor.execute("INSERT into log (usuario, fecha, accion) values (%s, %s, %s)",
                               [valores.usuarioActual, time.strftime('%d-%m-%Y_%H:%M:%S'), "escogio_destino_dominical"])
    conn.commit()
    mejor_ruta = nx.dijkstra_path(valores.Grafo, origen, destino)
    peso = nx.dijkstra_path_length(valores.Grafo, origen, destino)
    precio = 1000 + (530 * peso / 3)
    return render_template("Tren.html", mejor_ruta=mejor_ruta, peso=peso, precio = precio)


@app.route('/confirmarViaje/')
def confirmar():
    return render_template('confirmarViaje.html')

@app.route('/viaje' , methods=['GET', 'POST'])
def viaje():
    origen = request.form.get('origen_select')
    destino = request.form.get('destino_select')
    transporte = request.form.get('transporte_select')

    if transporte =="Taxi":
        return Taxi(origen,destino)

    elif transporte =="Bus":
        return Bus(origen,destino)

    elif transporte =="Tren":
         return Tren(origen,destino)

    elif transporte=="Avion":
        return Avion(origen,destino)

    else:
        return redirect(url_for('dashboard'))


if __name__ == "__main__":
    app.run(debug=True, port=8000, host='0.0.0.0')
