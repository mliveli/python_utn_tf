from cgitb import text
from ctypes import alignment
from tkinter import *
import calendar
from tkinter import ttk
from tkinter.messagebox import *
from turtle import bgcolor, heading, xcor
from tkcalendar import Calendar
from tkcalendar import DateEntry
import os
import datetime
from datetime import timedelta, date

os.system("cls")

id_reserva = 0
tuple_reserva = []
# vehiculos = ["v1", "v2", "v3"]
lista_fechas = []
lista_fiat = []
lista_chevrolet = []
lista_renault = []
lista_volkswagen = []


################################################################
##MODELO-TODAS LAS FUNCIONES DEL PROGRAMA
################################################################
# ****************************************************************
# Funcion del Boton Disponibilidad
# ****************************************************************


def f_disponibilidad():
    global lista_volkswagen
    global lista_fiat
    global lista_chevrolet
    global lista_renault

    cal.calevent_remove("all")

    if variable_autos.get() == "Volkswagen":
        for x in lista_volkswagen:
            a, b, c = x.split(",")
            day = datetime.date(int(a), int(b), int(c))
            cal.calevent_create(day, "", tags="1")
            cal.tag_config("1", background="red")
            cal.tag_config("2", background="grey")
            cal.tag_config("3", background="grey")
            cal.tag_config("4", background="grey")

    elif variable_autos.get() == "Fiat":
        for x in lista_fiat:
            a, b, c = x.split(",")
            day = datetime.date(int(a), int(b), int(c))
            cal.calevent_create(day, "", tags="2")
            cal.tag_config("2", background="red")
            cal.tag_config("3", background="grey")
            cal.tag_config("1", background="grey")
            cal.tag_config("4", background="grey")

    elif variable_autos.get() == "Chevrolet":
        for x in lista_chevrolet:
            a, b, c = x.split(",")
            day = datetime.date(int(a), int(b), int(c))
            cal.calevent_create(day, "", tags="3")
            cal.tag_config("3", background="red")
            cal.tag_config("1", background="grey")
            cal.tag_config("2", background="grey")
            cal.tag_config("4", background="grey")

    elif variable_autos.get() == "Renault":
        for x in lista_renault:
            a, b, c = x.split(",")
            day = datetime.date(int(a), int(b), int(c))
            cal.calevent_create(day, "", tags="4")
            cal.tag_config("4", background="red")
            cal.tag_config("1", background="grey")
            cal.tag_config("3", background="grey")
            cal.tag_config("2", background="grey")

    elif variable_autos.get() == "Total":
        for x in lista_fechas:
            a, b, c = x.split(",")
            day = datetime.date(int(a), int(b), int(c))
            print(day)
            cal.calevent_create(day, "", tags="5")
            cal.tag_config("5", background="red")


# ****************************************************************
# Funcion del boton reservar
# ****************************************************************


def f_boton_reservar():
    global id_reserva
    global reserva
    global vehiculos
    global lista_fechas
    global lista_fiat
    global lista_chevrolet
    global lista_renault
    global lista_volkswagen

    id_reserva += 1

    tree.insert(
        "",
        "end",
        values=(
            id_reserva,
            e_nombre.get(),
            variable_autos.get(),
            fecha_inicio.get(),
            fecha_fin.get(),
        ),
    )

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

        if variable_autos.get() == "Volkswagen":
            lista_volkswagen.append(dt.strftime("%Y,%m,%d"))
        elif variable_autos.get() == "Fiat":
            lista_fiat.append(dt.strftime("%Y,%m,%d"))
        elif variable_autos.get() == "Chevrolet":
            lista_chevrolet.append(dt.strftime("%Y,%m,%d"))
        elif variable_autos.get() == "Renault":
            lista_renault.append(dt.strftime("%Y,%m,%d"))
        else:
            None

    tuple_reserva.append(
        (
            id_reserva,
            e_nombre.get(),
            variable_autos.get(),
            fecha_inicio.get(),
            fecha_fin.get(),
        )
    )
    lista_fechas = lista_fiat + lista_chevrolet + lista_renault + lista_volkswagen
    # print(tuple_reserva)


# **********************************************************************************************

# ****************************************************************
# Funcion del boton Baja
# ****************************************************************


def f_boton_baja():
    global id_reserva
    global tuple_reserva
    item = tree.focus()
    # print(tree.item(item))
    tree.delete(item)

    id_reserva = 1
    for x in tuple_reserva:
        id_reserva += 1
        x[0] = id_reserva
    print(tuple_reserva)


# ****************************************************************
# Funcion del boton Modificar
# ****************************************************************


def f_boton_modificar():
    global tuple_reserva
    selected = tree.focus()
    temp = tree.item(selected, "values")
    tree.item(
        selected,
        values=(
            temp[0],
            e_nombre.get(),
            variable_autos.get(),
            fecha_inicio.get(),
            fecha_fin.get(),
        ),
    )

    tuple_reserva[int(temp[0]) - 1] = (
        temp[0],
        e_nombre.get(),
        variable_autos.get(),
        fecha_inicio.get(),
        fecha_fin.get(),
    )

    print(tuple_reserva)


# ****************************************************************
# Funcion del boton Salir
# ****************************************************************


def f_boton_salir():
    if askyesno("Salir", "Desea Salir?"):
        root.destroy()


######################################################################################
##VISTA Y CONTROLADOR
#####################################################################################
root = Tk()


# ************************************************************************************
# variables tkinter
# ***************************************************************************************

var_fecha_inicio = StringVar()
var_fecha_fin = StringVar()
var_vehiculo = StringVar()
var_nombre = StringVar()
var_direccion = StringVar()
var_telefono = StringVar()
var_mail = StringVar()
variable_autos = StringVar()


# ****************************************************************
# ventana principal
# ****************************************************************

root.title("Alquiler de Autos - Reservas")
root.geometry("1200x800")


# ****************************************************************
# entrada fecha inicio y fin, tipo de auto a reservar
# ****************************************************************


fecha_inicio = DateEntry(
    width=12, background="darkblue", foreground="white", borderwidth=2
)
fecha_inicio.place(x=10, y=20, width=100, height=25)

fecha_fin = DateEntry(
    width=12, background="darkblue", foreground="white", borderwidth=2
)
fecha_fin.place(x=120, y=20, width=100, height=25)

variable_autos.set("Volkswagen")  # default value

w = OptionMenu(
    root, variable_autos, "Volkswagen", "Fiat", "Chevrolet", "Renault", "Total"
)
w.place(x=235, y=17, height=30)


# ****************************************************************
# boton disponibilidad
# ****************************************************************

boton_disponibilidad = Button(root, text="Disponibilidad", command=f_disponibilidad)
boton_disponibilidad.place(x=350, y=19, width=100, height=25)


# ****************************************************************
# calendario
# ****************************************************************

cal = Calendar(root, selectmode="day", year=2022, month=8, day=28)

cal.place(x=920, y=55)


def grad_date():
    date.config(text="Selected Date is: " + cal.get_date())


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

# tree.bind("<<TreeviewSelect>>", bind_accion)  # accion al seleccionar un tree


# ****************************************************************
# boton reservar
# ****************************************************************

boton_reservar = Button(root, text="Reservar", command=f_boton_reservar)
boton_reservar.place(x=150, y=660, width=100, height=25)


# ****************************************************************
# Boton Baja de reserva
# ****************************************************************

boton_baja = Button(root, text="Baja", command=f_boton_baja)
boton_baja.place(x=275, y=660, width=100, height=25)


# ****************************************************************
# boton baja de modificar
# ****************************************************************

boton_modificar = Button(root, text="Modificar", command=f_boton_modificar)
boton_modificar.place(x=400, y=660, width=100, height=25)


# ****************************************************************
# boton baja de salir
# ****************************************************************

boton_salir = Button(root, text="Salir", command=f_boton_salir)
boton_salir.place(x=500, y=750, width=100, height=25)

# ****************************************************************
# datos del cliente
# ****************************************************************

label_nombre = Label(root, text="Nombre:")
label_nombre.place(x=10, y=500)

label_telefono = Label(root, text="Telefono:")
label_telefono.place(x=10, y=535)

label_direccion = Label(root, text="Direccion:")
label_direccion.place(x=10, y=570)

label_mail = Label(root, text="Mail:")
label_mail.place(x=10, y=605)

e_nombre = Entry(root, textvariable=var_nombre)
e_nombre.place(x=120, y=500, width=710, height=25)

e_direccion = Entry(root, textvariable=var_direccion)
e_direccion.place(x=120, y=535, width=710, height=25)

e_telefono = Entry(root, textvariable=var_telefono)
e_telefono.place(x=120, y=570, width=710, height=25)

e_mail = Entry(root, textvariable=var_mail)
e_mail.place(x=120, y=605, width=710, height=25)


root.mainloop()
