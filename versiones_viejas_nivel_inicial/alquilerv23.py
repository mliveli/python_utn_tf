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
from tkinter import messagebox
import re


os.system("cls")

reserva = []
id_datos = 0
lista_de_autos = ["Vehiculo", "Volkswagen", "Fiat", "Chevrolet"]


# ****************************************************************
# Funcion del Boton Disponibilidad
# ****************************************************************
def test_disponibilidad():
    pass


# ****************************************************************
# Funcion del boton reservar
# ****************************************************************
def f_boton_reservar(con, tree):
    pass


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

    inicializar_treview(tree)


# ****************************************************************
# Funcion del boton Modificar
# ****************************************************************
def f_boton_modificar(tree):
    pass


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

    if len(contenido.get("values")) > 0:
        id_datos = contenido.get("values")[0]

        cursor = con.cursor()
        cursor = cursor.execute("select * from reservas where id=?", (int(id_datos),))

        fila = cursor.fetchone()

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
    for item in tree.get_children():
        tree.delete(item)
    cursor = con.execute("select id,vehiculo, inicio,fin from reservas")
    for fila in cursor:
        tree.insert("", "end", values=(fila[0], fila[1], fila[2], fila[3]))


# ********************************************************************
# funcion inicializar calendario                                     *
# ********************************************************************
def inicializar_calendario():
    pass


con = crear_base()
crear_tabla(con)


# ********************************************************************
# Controladores                                                      *
# ********************************************************************


def test_fechas():
    a = fecha_inicio.get().split("/")
    b = fecha_fin.get().split("/")
    x, y, z = a[2], a[1], a[0]
    f_inicio = date(int("20" + x), int(y), int(z))

    x, y, z = b[2], b[1], b[0]

    f_fin = date(int("20" + x), int(y), int(z))

    if f_inicio > f_fin:
        messagebox.showinfo(
            message="La fecha final es anterior a la fecha de inicio",
            title="Fecha erronea",
        )
        return False
    else:
        return True


def test_telefono(tel):
    patron = re.compile(r"(\b[0-9][0-9]{9,14}\b)")

    if patron.match(tel) is None:
        messagebox.showinfo(
            message="Formato de telefono erroneo",
            title="Error en Telefono",
        )
        return False
    return True


def fecha_inicio_seleccionada(*args):
    pass


def fecha_fin_seleccionada(*args):

    if not (len(fecha_fin.get()) == 0):
        test_fechas()


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
sel_fecha_inicio = StringVar()
sel_fecha_fin = StringVar()

# ****************************************************************
# ventana principal
# ****************************************************************
root.title("Alquiler de Autos - Reservas")
root.geometry("860x600")

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


variable_autos = ttk.Combobox(state="readonly", values=lista_de_autos)
variable_autos.place(x=30, y=250, height=30)
variable_autos.current(0)
# variable_autos.bind("<<ComboboxSelected>>", actualizar_lista_de_autos())


# ****************************************************************
# Campo entrada fecha inicio y fin
# ****************************************************************
fecha_inicio = DateEntry(
    root,
    width=12,
    background="darkblue",
    foreground="white",
    borderwidth=2,
    textvariable=sel_fecha_inicio,
)
fecha_inicio.place(x=50, y=20, width=100, height=25)
sel_fecha_inicio.trace("w", fecha_inicio_seleccionada)

fecha_fin = DateEntry(
    root,
    width=12,
    background="darkblue",
    foreground="white",
    borderwidth=2,
    textvariable=sel_fecha_fin,
)
fecha_fin.place(x=160, y=20, width=100, height=25)
sel_fecha_fin.trace("w", fecha_fin_seleccionada)


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

e_telefono = Entry(root, textvariable=var_telefono)
e_telefono.place(x=120, y=420, width=710, height=25)

e_direccion = Entry(root, textvariable=var_direccion)
e_direccion.place(x=120, y=455, width=710, height=25)

e_mail = Entry(root, textvariable=var_mail)
e_mail.place(x=120, y=490, width=710, height=25)

# ****************************************************************
# Treeview - lista de reservas
# ****************************************************************
tree_frame = ttk.Frame(root)
tree_frame.config(height=10)
tree_frame.pack()

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

tree.place(x=330, y=20, width=500, height=340)

#       ----------Barra de dezplazamiento-----------------
vsb = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
vsb.place(x=330 + 500 + 2, y=20, height=340)

inicializar_treview(tree)

tree.bind("<<TreeviewSelect>>", bind_accion)  # accion al seleccionar un tree


root.mainloop()
con.close()
