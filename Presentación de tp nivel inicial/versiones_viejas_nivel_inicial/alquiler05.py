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

os.system("cls")

reserva = []
vehiculos = ["Chevrolet", "Fiar", "Renault"]
id_datos = []


# ****************************************************************
# Funcion del Boton Disponibilidad
# ****************************************************************
def f_boton_disponibilidad():  # actualizar base de datos
    var_fecha_inicio = fecha_inicio.get()
    var_fecha_fin = fecha_fin.get()
    print(var_fecha_inicio, var_fecha_fin)
    if var_fecha_inicio == "1/9/22":
        marcador_disponibilidad.configure(background="green")
    else:
        marcador_disponibilidad.configure(background="red")


# ****************************************************************
# Funcion del boton reservar
# ****************************************************************
def f_boton_reservar(con):
    ultimo_id = 0
    cursor = con.cursor()
    datos_reserva = (
        e_nombre.get(),
        e_direccion.get(),
        e_telefono.get(),
        e_mail.get(),
        vehiculos[0],
        fecha_inicio.get(),
        fecha_fin.get(),
    )
    sql = "INSERT INTO reservas(nombre, direccion, telefono, mail, vehiculo, inicio, fin) VALUES (?,?,?,?,?,?,?)"
    cursor.execute(sql, datos_reserva)
    con.commit()

    # ************ carga de treeview *******************
    cursor = con.cursor()
    cursor.execute("SELECT * FROM reservas")
    for fila in cursor:
        ultimo_id = ultimo_id + 1
        # print(fila, "  ", ultimo_id)

    tree.insert(
        "",
        "end",
        values=(ultimo_id, var_vehiculo, fecha_inicio.get(), fecha_fin.get()),
    )

    e_nombre.delete(0, 710)
    e_telefono.delete(0, 710)
    e_direccion.delete(0, 710)
    e_mail.delete(0, 710)


# ****************************************************************
# Funcion del boton Baja
# ****************************************************************
def f_boton_baja():  # falta actualizar treeview
    global id_datos
    # item = tree.focus()
    # print("baja " + str(item))

    cursor = con.cursor()
    mi_id = int(id_datos)
    data = (mi_id,)
    sql = "DELETE FROM reservas WHERE id=?;"
    cursor.execute(sql, data)
    con.commit()

    # tree.delete(item)
    # print("*******" + type(item) + "  " + item)


# ****************************************************************
# Funcion del boton Modificar
# ****************************************************************
def f_boton_modificar():  # falta actualizar treeview
    global id_datos
    cursor = con.cursor()
    mi_id = int(id_datos)
    datos_reserva = (
        e_nombre.get(),
        e_direccion.get(),
        e_telefono.get(),
        e_mail.get(),
        vehiculos[0],
        fecha_inicio.get(),
        fecha_fin.get(),
        mi_id,
    )

    sql = "UPDATE reservas SET nombre=?, direccion=?, telefono=?, mail=?, vehiculo=?, inicio=?, fin=? WHERE id=?;"
    cursor.execute(sql, datos_reserva)
    con.commit()


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
# ********************************************************************
def crear_base():
    con = sqlite3.connect("alquiler.db")
    return con


def crear_tabla(con):
    cursor = con.cursor()
    sql = "CREATE TABLE IF NOT EXISTS reservas(\
        id integer PRIMARY KEY,\
        nombre VARCHAR(128),\
        direccion VARCHAR(128),\
        telefono VARCHAR(128),\
        mail VARCHAR(128),\
        vehiculo VARCHAR(128),\
        inicio VARCHAR(128),\
        fin VARCHAR(128))"
    cursor.execute(sql)
    con.commit()


def inicializar_treview():
    cursor = con.execute("select id,vehiculo, inicio,fin from reservas")
    for fila in cursor:
        tree.insert(
            "",
            "end",
            values=(fila[0], fila[1], fila[2], fila[3]),
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
var_vehiculo = "Vehiculo " + vehiculos[0] + ": Reserva --> "
var_nombre = StringVar()
var_direccion = StringVar()
var_telefono = StringVar()
var_mail = StringVar()


# ****************************************************************
# ventana principal
# ****************************************************************
root.title("Alquiler de Autos - Reservas")
root.geometry("840x600")

# ****************************************************************
# Marcador de disponibilidad (Labael por ahora)
# ****************************************************************
marcador_disponibilidad = Entry(root)
marcador_disponibilidad.place(x=340, y=20, width=25, height=25)

# ****************************************************************
# Botonnes
# ****************************************************************
boton_disponibilidad = Button(
    root, text="Disponibilidad", command=f_boton_disponibilidad
)
boton_disponibilidad.place(x=230, y=20, width=100, height=25)

boton_reservar = Button(root, text="Reservar", command=lambda: f_boton_reservar(con))
boton_reservar.place(x=10, y=565, width=100, height=25)

boton_baja = Button(root, text="Baja", command=f_boton_baja)
boton_baja.place(x=120, y=565, width=100, height=25)

boton_modificar = Button(root, text="Modificar", command=f_boton_modificar)
boton_modificar.place(x=230, y=565, width=100, height=25)

boton_salir = Button(root, text="Salir", command=f_boton_salir)
boton_salir.place(x=490, y=565, width=100, height=25)

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

# ****************************************************************
# calendario
# ****************************************************************
cal = Calendar(root, selectmode="day", year=2022, month=8, day=28)

cal.place(x=30, y=55)

# ****************************************************************
# Datos del cliente
# ****************************************************************
label_nombre = Label(root, text="Nombre:")
label_nombre.place(x=10, y=385)

label_telefono = Label(root, text="Telefono:")
label_telefono.place(x=10, y=420)

label_direccion = Label(root, text="Direccion:")
label_direccion.place(x=10, y=455)

label_mail = Label(root, text="Mail:")
label_mail.place(x=10, y=490)

e_nombre = Entry(root, textvariable=var_nombre)
e_nombre.place(x=120, y=385, width=710, height=25)

e_direccion = Entry(root, textvariable=var_direccion)
e_direccion.place(x=120, y=420, width=710, height=25)

e_telefono = Entry(root, textvariable=var_telefono)
e_telefono.place(x=120, y=455, width=710, height=25)

e_mail = Entry(root, textvariable=var_mail)
e_mail.place(x=120, y=490, width=710, height=25)

# ****************************************************************
# lista de reservas
# ****************************************************************
tree = ttk.Treeview(root, show="headings")
tree["columns"] = ("col1", "col2", "col3", "col4")

tree.heading("col1", text="ID")
tree.heading("col2", text="Vehiculo")
tree.heading("col3", text="Desde")
tree.heading("col4", text="Hasta")

tree.column("col1", width=10, minwidth=10, anchor=W)
tree.column("col2", width=120, minwidth=80, anchor=W)
tree.column("col3", width=20, minwidth=20, anchor=W)
tree.column("col4", width=20, minwidth=20, anchor=W)

tree.place(x=330, y=55, width=500, height=220)

inicializar_treview()

tree.bind("<<TreeviewSelect>>", bind_accion)  # accion al seleccionar un tree


root.mainloop()
con.close()
