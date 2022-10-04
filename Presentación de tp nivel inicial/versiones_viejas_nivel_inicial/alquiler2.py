from cgitb import text
from ctypes import alignment
from tkinter import *
import calendar
from tkinter import ttk
from tkinter.messagebox import *
from turtle import heading
from tkcalendar import Calendar
from tkcalendar import DateEntry
import os

os.system("cls")

id_reserva = 0
reserva = []
vehiculos = ["v1", "v2", "v3"]


# ****************************************************************
# Funcion del Boton Disponibilidad
# ****************************************************************
def f_boton_disponibilidad():
    var_fecha_inicio = fecha_inicio.get()
    var_fecha_fin = fecha_fin.get()
    print(var_fecha_inicio, var_fecha_fin)
    if var_fecha_inicio == "28/8/22":
        marcador_disponibilidad.configure(background="green")
    else:
        marcador_disponibilidad.configure(background="red")


# ****************************************************************
# Funcion del boton reservar
# ****************************************************************
def f_boton_reservar():
    global id_reserva
    global reserva
    global vehiculos
    id_reserva += 1
    print("reserva " + str(id_reserva))
    tree.insert(
        "",
        "end",
        values=(id_reserva, var_vehiculo, fecha_inicio.get(), fecha_fin.get()),
    )

    d_cliente = {
        "nombre": e_nombre.get(),
        "direccion": e_direccion.get(),
        "telefono": e_telefono.get(),
        "mail": e_mail.get(),
        "vehiculo": vehiculos[0],
        "inicio": fecha_inicio.get(),
        "fin": fecha_fin.get(),
    }

    e_nombre.delete(0, 710)
    e_telefono.delete(0, 710)
    e_direccion.delete(0, 710)
    e_mail.delete(0, 710)

    reserva.append(d_cliente)
    for i in reserva:
        print(i["nombre"])
    print("")


# ****************************************************************
# Funcion del boton Baja
# ****************************************************************
def f_boton_baja():
    global id_reserva
    global reserva
    item = tree.focus()
    tree.delete(item)
    # tree.update()
    print("baja " + str(item))
    del reserva[int(id_reserva) - 1]
    id_reserva -= 1


# ****************************************************************
# Funcion del boton Modificar
# ****************************************************************
def f_boton_modificar():
    global id_reserva
    item = tree.focus()
    print(item)


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
    global id_reserva
    global reserva
    item = tree.focus()
    contenido = tree.item(item)
    id_datos = contenido.get("values")[0]
    e_nombre.delete(0, 710)
    e_nombre.insert(0, reserva[id_datos - 1].get("nombre"))
    e_telefono.delete(0, 710)
    e_telefono.insert(0, reserva[id_datos - 1].get("telefono"))
    e_direccion.delete(0, 710)
    e_direccion.insert(0, reserva[id_datos - 1].get("direccion"))
    e_mail.delete(0, 710)
    e_mail.insert(0, reserva[id_datos - 1].get("mail"))


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

boton_reservar = Button(root, text="Reservar", command=f_boton_reservar)
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
tree.column("col3", width=80, minwidth=80, anchor=W)
tree.column("col4", width=80, minwidth=80, anchor=W)

tree.place(x=330, y=55, width=500, height=220)

tree.bind("<<TreeviewSelect>>", bind_accion)  # accion al seleccionar un tree


root.mainloop()
