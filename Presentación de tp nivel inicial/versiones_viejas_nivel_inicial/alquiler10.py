from ast import Delete
from cgitb import text
from ctypes import alignment
from faulthandler import disable
from operator import delitem
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *
from turtle import heading
from typing import Any
from typing_extensions import Self
from winreg import DeleteValue
from tkcalendar import Calendar
from tkcalendar import DateEntry
import datetime
from datetime import timedelta, date
import sqlite3
import os


os.system("cls")

reserva = []
id_datos = 0


# ****************************************************************
# Funcion del Boton Disponibilidad
# ****************************************************************
def f_boton_disponibilidad():
    fechas = cargar_lista_de_disponibilidad()
    print(fechas)
    print(len(fechas[0].split(" ")))

    fechas_temporales = []

    a = fecha_inicio.get().split("/")
    b = fecha_fin.get().split("/")
    x, y, z = a[2], a[1], a[0]
    f_inicio = date(int("20" + x), int(y), int(z))

    f, j, q = b[2], b[1], b[0]
    f_fin = date(int("20" + f), int(j), int(q))

    dias = (f_fin - f_inicio).days
    fechas_temporales.clear()
    for i in range(dias + 1):
        fechas_temporales.append((f_inicio + timedelta(days=i)).strftime("%Y-%m-%d"))

    print("\n\nTmporales >>>>> ", fechas_temporales)

    entrada = len(fechas)
    flag = 0
    for t1 in range(len(fechas_temporales)):
        for t2 in range(entrada):
            if fechas_temporales[t1] == fechas[t2].split(" ")[0]:
                print(fechas_temporales[t1], "  ", fechas[t2].split(" ")[0])
                print(len(fechas[t2].split(" ")))
                if len(fechas[t2].split(" ")) == 4:
                    flag = 1

    if flag == 0:
        marcador_disponibilidad.configure(background="green")
        marcador_disponibilidad.delete(0, 100)
        marcador_disponibilidad.insert(0, "Disponible")
    else:
        marcador_disponibilidad.configure(background="red")
        marcador_disponibilidad.delete(0, 100)
        marcador_disponibilidad.insert(0, "No disponible")


# ****************************************************************
# Funcion del boton reservar
# ****************************************************************
def f_boton_reservar(con, tree):
    # validar que fechafin sea mayor a fechainicio
    # filtrar multiples alquileres por el mismo auto misma fecha
    ultimo_id = 0
    cursor = con.cursor()
    datos_reserva = (
        e_nombre.get(),
        e_direccion.get(),
        e_telefono.get(),
        e_mail.get(),
        variable_autos.get(),
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

    for item in tree.get_children():
        tree.delete(item)
    inicializar_treview(tree)
    inicializar_calendario()


# ****************************************************************
# Funcion del boton Baja
# ****************************************************************
def f_boton_baja(tree):
    global id_datos
    cursor = con.cursor()
    mi_id = int(id_datos)
    data = (mi_id,)
    sql = "DELETE FROM reservas WHERE id=?;"
    cursor.execute(sql, data)
    con.commit()

    for item in tree.get_children():
        tree.delete(item)
    inicializar_treview(tree)


# ****************************************************************
# Funcion del boton Modificar
# ****************************************************************
def f_boton_modificar(tree):
    global id_datos
    cursor = con.cursor()
    mi_id = int(id_datos)
    datos_reserva = (
        e_nombre.get(),
        e_direccion.get(),
        e_telefono.get(),
        e_mail.get(),
        variable_autos.get(),
        fecha_inicio.get(),
        fecha_fin.get(),
        mi_id,
    )

    sql = "UPDATE reservas SET nombre=?, direccion=?, telefono=?, mail=?, vehiculo=?, inicio=?, fin=? WHERE id=?;"
    cursor.execute(sql, datos_reserva)
    con.commit()

    for item in tree.get_children():
        tree.delete(item)
    inicializar_treview(tree)


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
        print("No existe un art??culo con dicho c??digo.")

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


def inicializar_treview(tree):
    cursor = con.execute("select id,vehiculo, inicio,fin from reservas")
    for fila in cursor:
        tree.insert("", "end", values=(fila[0], fila[1], fila[2], fila[3]))


# ********************************************************************
# funcion lista de dias con reserva de vehiculos agotados            *
# ********************************************************************
def cargar_lista_de_disponibilidad():
    fechas = []
    fechas_temporales = []

    cursor = con.execute("select vehiculo, inicio,fin from reservas")
    for fila in cursor:
        a = fila[1].split("/")
        b = fila[2].split("/")

        x, y, z = a[2], a[1], a[0]
        fecha_inicio = date(int("20" + x), int(y), int(z))

        f, j, q = b[2], b[1], b[0]
        fecha_fin = date(int("20" + f), int(j), int(q))

        dias = (fecha_fin - fecha_inicio).days
        fechas_temporales.clear()
        for i in range(dias + 1):
            fechas_temporales.append(
                (fecha_inicio + timedelta(days=i)).strftime("%Y-%m-%d")
            )

        entrada = len(fechas)
        flag = 0
        for t1 in range(dias + 1):
            flag = 0

            for t2 in range(entrada):
                if fechas_temporales[t1] == fechas[t2].split(" ")[0]:
                    fechas[t2] = fechas[t2] + " " + fila[0]
                    flag = 1
            if flag == 0:
                fechas.append(fechas_temporales[t1] + " " + fila[0])

    return fechas


# ********************************************************************
# funcion inicializar calendario                                     *
# ********************************************************************
def inicializar_calendario():
    fechas = cargar_lista_de_disponibilidad()
    cal.calevent_remove("all")

    for t1 in range(len(fechas)):
        if len(fechas[t1].split(" ")) == 4:
            fdesc = fechas[t1].split(" ")
            f = fdesc[0].split("-")

            day = datetime.date(int(f[0]), int(f[1]), int(f[2]))
            cal.calevent_create(day, "", tags="5")
            cal.tag_config("5", background="red")


con = crear_base()
crear_tabla(con)


# *******************************************************************
# VISTA VISTA VISTA VISTA VISTA VISTA VISTA VISTA VISTA VISTA VISTA *
# *******************************************************************
root = Tk()

var_fecha_inicio = StringVar()
var_fecha_fin = StringVar()
var_nombre = StringVar()
var_direccion = StringVar()
var_telefono = StringVar()
var_mail = StringVar()
variable_autos = StringVar()

# ****************************************************************
# ventana principal
# ****************************************************************
root.title("Alquiler de Autos - Reservas")
root.geometry("840x600")

# ****************************************************************
# Marcador de disponibilidad (Labael por ahora)
# ****************************************************************
marcador_disponibilidad = Entry(root)
marcador_disponibilidad.place(x=340, y=20, width=100, height=25)

# ****************************************************************
# Botonnes
# ****************************************************************
boton_disponibilidad = Button(
    root, text="Disponibilidad", command=f_boton_disponibilidad
)
boton_disponibilidad.place(x=230, y=20, width=100, height=25)

boton_reservar = Button(
    root, text="Reservar", command=lambda: f_boton_reservar(con, tree)
)
boton_reservar.place(x=10, y=565, width=100, height=25)

boton_baja = Button(root, text="Baja", command=lambda: f_boton_baja(tree))
boton_baja.place(x=120, y=565, width=100, height=25)

boton_modificar = Button(
    root, text="Modificar", command=lambda: f_boton_modificar(tree)
)
boton_modificar.place(x=230, y=565, width=100, height=25)

boton_salir = Button(root, text="Salir", command=f_boton_salir)
boton_salir.place(x=490, y=565, width=100, height=25)

variable_autos.set("Volkswagen")
boton_autos = OptionMenu(root, variable_autos, "Volkswagen", "Fiat", "Chevrolet")
boton_autos.place(x=450, y=17, height=30)


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
now = datetime.datetime.now()
now = str(now).split(" ")
now = now[0].split("-")
cal = Calendar(
    root, selectmode="day", year=int(now[0]), month=int(now[1]), day=int(now[2])
)

cal.place(x=30, y=55)

inicializar_calendario()

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

inicializar_treview(tree)

tree.bind("<<TreeviewSelect>>", bind_accion)  # accion al seleccionar un tree


root.mainloop()
con.close()
