from cgitb import text
from ctypes import alignment
from tkinter import *

# import calendar
from tkinter import ttk
from tkinter.messagebox import *
from turtle import heading
from tkcalendar import Calendar
from tkcalendar import DateEntry
import sqlite3
import os
import datetime
from datetime import timedelta, date

os.system("cls")

reserva = []
vehiculos = ["Chevrolet", "Fiat", "Renault"]
id_datos = 0
lista_fechas = []
lista_fiat = []
lista_chevrolet = []
lista_renault = []

# ****************************************************************
# Funcion del Boton Disponibilidad
# ****************************************************************
def f_disponibilidad():
    global lista_fechas
    global lista_fiat
    global lista_chevrolet
    global lista_renault

    cal.calevent_remove("all")

    if var_vehiculo.get() == "Renault":
        for x in lista_renault:
            a, b, c = x.split(",")
            day = datetime.date(int(a), int(b), int(c))
            cal.calevent_create(day, "", tags="4")
            cal.tag_config("4", background="red")
            cal.tag_config("1", background="grey")
            cal.tag_config("3", background="grey")
            cal.tag_config("2", background="grey")

    elif var_vehiculo.get() == "Fiat":
        for x in lista_fiat:
            a, b, c = x.split(",")
            day = datetime.date(int(a), int(b), int(c))
            cal.calevent_create(day, "", tags="2")
            cal.tag_config("2", background="red")
            cal.tag_config("3", background="grey")
            cal.tag_config("1", background="grey")
            cal.tag_config("4", background="grey")

    elif var_vehiculo.get() == "Chevrolet":
        for x in lista_chevrolet:
            a, b, c = x.split(",")
            day = datetime.date(int(a), int(b), int(c))
            cal.calevent_create(day, "", tags="3")
            cal.tag_config("3", background="red")
            cal.tag_config("1", background="grey")
            cal.tag_config("2", background="grey")
            cal.tag_config("4", background="grey")


# ****************************************************************
# Funcion del boton reservar
# ****************************************************************
def f_boton_reservar(con):
    ultimo_id = 0
    global lista_fechas
    global lista_fiat
    global lista_chevrolet
    global lista_renault
    cursor = con.cursor()
    ultimo_id += 1

    tree.insert(
        "",
        "end",
        values=(
            ultimo_id,
            e_nombre.get(),
            var_vehiculo.get(),
            fecha_inicio.get(),
            fecha_fin.get(),
        ),
    )

    datos_reserva = (
        e_nombre.get(),
        e_direccion.get(),
        e_telefono.get(),
        e_mail.get(),
        var_vehiculo.get(),
        fecha_inicio.get(),
        fecha_fin.get(),
    )
    sql = "INSERT INTO reservas(nombre, direccion, telefono, mail, vehiculo, inicio, fin) VALUES (?,?,?,?,?,?,?)"
    cursor.execute(sql, datos_reserva)
    con.commit()

    # *********************Subfuncion marca con color disponibilidad en calendario*******************

    a = fecha_inicio.get().split("/")
    b = fecha_fin.get().split("/")

    def daterange(date1, date2):
        for n in range(int((date2 - date1).days) + 1):
            yield date1 + timedelta(n)

    x, z, y = a[2], a[1], a[0]
    start_dt = date(int("20" + x), int(z), int(y))

    f, j, q = b[2], b[1], b[0]
    end_dt = date(int("20" + f), int(j), int(q))

    for dt in daterange(start_dt, end_dt):

        if var_vehiculo.get() == "Fiat":
            lista_fiat.append(dt.strftime("%Y,%m,%d"))
            print(lista_fiat)
        elif var_vehiculo.get() == "Chevrolet":
            lista_chevrolet.append(dt.strftime("%Y,%m,%d"))
        elif var_vehiculo.get() == "Renault":
            lista_renault.append(dt.strftime("%Y,%m,%d"))
        else:
            None

    # lista_fechas = lista_fiat + lista_chevrolet + lista_renault + lista_volkswagen
    # print(tuple_reserva)
    # ************ carga de treeview *******************
    cursor = con.cursor()
    cursor.execute("SELECT * FROM reservas")
    for fila in cursor:
        ultimo_id = ultimo_id + 1

    for item in tree.get_children():
        tree.delete(item)
    inicializar_treview()


# ****************************************************************
# Funcion del boton Baja
# ****************************************************************
def f_boton_baja():
    global id_datos
    cursor = con.cursor()
    mi_id = int(id_datos)
    data = (mi_id,)
    sql = "DELETE FROM reservas WHERE id=?;"
    cursor.execute(sql, data)
    con.commit()

    for item in tree.get_children():
        tree.delete(item)
    inicializar_treview()


# ****************************************************************
# Funcion del boton Modificar
# ****************************************************************
def f_boton_modificar():
    global id_datos
    cursor = con.cursor()
    mi_id = int(id_datos)
    datos_reserva = (
        e_nombre.get(),
        e_direccion.get(),
        e_telefono.get(),
        e_mail.get(),
        var_vehiculo.get(),
        fecha_inicio.get(),
        fecha_fin.get(),
        mi_id,
    )

    sql = "UPDATE reservas SET nombre=?, direccion=?, telefono=?, mail=?, vehiculo=?, inicio=?, fin=? WHERE id=?;"
    cursor.execute(sql, datos_reserva)
    con.commit()

    for item in tree.get_children():
        tree.delete(item)
    inicializar_treview()


# ****************************************************************
# Funcion del boton Salir
# ****************************************************************
def f_boton_salir():
    if askyesno("Salir", "Desea Salir?"):
        root.destroy()


# ****************************************************************
# Funcion al seleccionar un tree
# ****************************************************************
def bind_accion(evt):
    global id_datos
    item = tree.focus()
    contenido = tree.item(item)
    id_datos = contenido.get("values")[0]
    print("************ ", type(id_datos), "  *  ", id_datos)

    cursor = con.cursor()
    cursor = cursor.execute("select * from reservas where id=?", (int(id_datos),))

    fila = cursor.fetchone()

    if fila != None:
        print(fila)
    else:
        print("No existe un artículo con dicho código.")

    e_nombre.delete(0, 710)
    e_nombre.insert(0, fila[1])
    e_telefono.delete(0, 710)
    e_telefono.insert(0, fila[2])
    e_direccion.delete(0, 710)
    e_direccion.insert(0, fila[3])
    e_mail.delete(0, 710)
    e_mail.insert(0, fila[4])
    fecha_inicio.delete(0, 8)
    fecha_inicio.insert(0, fila[6])
    fecha_fin.delete(0, 8)
    fecha_fin.insert(0, fila[7])


# ********************************************************************
# funcion CREAR base de datos y tabla principal (unica en este caso) *
# e inicializar treeview                                             *
# ********************************************************************
def crear_base():
    con = sqlite3.connect("alquiler.db")  # ACTIVAR EL ARCHIVO CUANDO SE USA CON
    return con


def crear_tabla(con):
    cursor = (
        con.cursor()
    )  # CURSOR ME VA A PERMITIR AGREGAR INFO A LA BASE DE DATOS. CON ES EL OBJETO DE CONEXION.
    sql = "CREATE TABLE IF NOT EXISTS reservas(\
        id integer PRIMARY KEY,\
        nombre VARCHAR(128),\
        direccion VARCHAR(128),\
        telefono VARCHAR(128),\
        mail VARCHAR(128),\
        vehiculo VARCHAR(128),\
        inicio VARCHAR(128),\
        fin VARCHAR(128))"  # ES ES EL CODIGO DE BASE DE DATOS.
    cursor.execute(sql)
    con.commit()


def inicializar_treview():
    cursor = con.execute("select id,nombre, vehiculo, inicio,fin from reservas")
    for fila in cursor:
        tree.insert(
            "",
            "end",
            values=(fila[0], fila[1], fila[2], fila[3], fila[4]),
        )


con = crear_base()
crear_tabla(con)


# *******************************************************************
# VISTA VISTA VISTA VISTA VISTA VISTA VISTA VISTA VISTA VISTA VISTA *
# *******************************************************************
root = Tk()

var_fecha_inicio = StringVar()
var_fecha_fin = StringVar()
var_vehiculo = StringVar()
var_nombre = StringVar()
var_direccion = StringVar()
var_telefono = StringVar()
var_mail = StringVar()


# ****************************************************************
# ventana principal
# ****************************************************************
root.title("Alquiler de Autos - Reservas")
root.geometry("1200x800")

# ****************************************************************
# Marcador de disponibilidad (Labael por ahora)
# ****************************************************************
marcador_disponibilidad = Entry(root)
marcador_disponibilidad.place(x=350, y=19, width=100, height=25)

# ****************************************************************
# Botonnes
# ****************************************************************
boton_disponibilidad = Button(root, text="Disponibilidad", command=f_disponibilidad)
boton_disponibilidad.place(x=350, y=19, width=100, height=25)

boton_reservar = Button(root, text="Reservar", command=lambda: f_boton_reservar(con))
boton_reservar.place(x=150, y=700, width=100, height=25)

boton_baja = Button(root, text="Baja", command=f_boton_baja)
boton_baja.place(x=275, y=700, width=100, height=25)

boton_modificar = Button(root, text="Modificar", command=f_boton_modificar)
boton_modificar.place(x=400, y=700, width=100, height=25)

boton_salir = Button(root, text="Salir", command=f_boton_salir)
boton_salir.place(x=525, y=700, width=100, height=25)

# ****************************************************************
# Campo entrada fecha inicio y fin
# ****************************************************************


fecha_inicio = DateEntry(
    width=12, background="darkblue", foreground="white", borderwidth=2
)
fecha_inicio.place(x=10, y=20, width=100, height=25)

fecha_fin = DateEntry(
    width=12, background="darkblue", foreground="white", borderwidth=2
)
fecha_fin.place(x=120, y=20, width=100, height=25)


w = OptionMenu(root, var_vehiculo, "Fiat", "Chevrolet", "Renault", "Total")
w.place(x=235, y=17, width=120, height=30)


# ****************************************************************
# calendario
# ****************************************************************
cal = Calendar(root, selectmode="day", year=2022, month=8, day=28)

cal.place(x=920, y=55)


def grad_date():
    date.config(text="Selected Date is: " + cal.get_date())


# ****************************************************************
# Datos del cliente
# ****************************************************************
label_nombre = Label(root, text="Nombre:")
label_nombre.place(x=10, y=545)

label_telefono = Label(root, text="Telefono:")
label_telefono.place(x=10, y=580)

label_direccion = Label(root, text="Direccion:")
label_direccion.place(x=10, y=615)

label_mail = Label(root, text="Mail:")
label_mail.place(x=10, y=650)

e_nombre = Entry(root, textvariable=var_nombre)
e_nombre.place(x=120, y=545, width=710, height=25)

e_direccion = Entry(root, textvariable=var_direccion)
e_direccion.place(x=120, y=580, width=710, height=25)

e_telefono = Entry(root, textvariable=var_telefono)
e_telefono.place(x=120, y=615, width=710, height=25)

e_mail = Entry(root, textvariable=var_mail)
e_mail.place(x=120, y=650, width=710, height=25)

# ****************************************************************
# lista de reservas
# ****************************************************************
tree = ttk.Treeview(root, show="headings")
tree["columns"] = ("col1", "col2", "col3", "col4", "col5")

# tree.heading("#0", text="ID")
tree.heading("col1", text="ID")
tree.heading("col2", text="Nombre")
tree.heading("col3", text="Vehiculo")
tree.heading("col4", text="Desde")
tree.heading("col5", text="Hasta")

# tree.column("#0", width=50, minwidth=50, anchor=W)
tree.column("col1", width=10, minwidth=10, anchor=W)
tree.column("col2", width=20, minwidth=10, anchor=W)
tree.column("col3", width=80, minwidth=80, anchor=W)
tree.column("col4", width=80, minwidth=80, anchor=W)
tree.column("col5", width=80, minwidth=80, anchor=W)

tree.place(x=10, y=55, width=890, height=425)

inicializar_treview()

tree.bind("<<TreeviewSelect>>", bind_accion)  # accion al seleccionar un tree


root.mainloop()
con.close()
