from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import matplotlib.pyplot as plt
import pandas as pd
import math
import geopy.distance
import numpy as np


def distance_between_points(point1, point2): #point1 / punto de inicio, point2 / punto final
    #se calcula la distancia entre puntos de longitud y latitud en kilometros
    return geopy.distance.geodesic((float(point1[3]), float(point1[2])), (float(point2[3]),float(point2[2]))).km

# HACIENDO LA LISTA PARA CADA HOSPITAL
def making_adjacency_list(hospitals_csv, farmacias_csv, max_range, price = "Economico"):
  hospitals = []
  for _ in range(len(hospitals_csv)):
    hospitals.append([])

  for x in range(len(hospitals_csv)):
    for y in range(len(farmacias_csv)):
      dis = distance_between_points(hospitals_csv[x],farmacias_csv[y]) #obtener la distancia entre el hospital y la farmacia
      if dis <= max_range and farmacias_csv[y][4] == price: #se compara si la farmacia cumple requisitos del usuario
        hospitals[x].append((farmacias_csv[y], dis))
  return hospitals #se retorna arreglo de hospitales con sus farmacias cercanas

def divide_and_conquer(hospital):
    n = len(hospital)
    if n == 0:
        return[]
    current = hospital[0]
    lst_left = []
    lst_right = []
    for i in range(n-1):
      next = hospital[i+1]
      lst_right.append(next) if next[1] > current[1] else lst_left.append(next)

    if not len(lst_left)<=1:
        lst_left=divide_and_conquer(lst_left)
    if not len(lst_right)<=1:
        lst_right=divide_and_conquer(lst_right)
    current = [current]
    hospital = lst_left + current + lst_right
    return(hospital)

def draw_points(csv, index, hospital):
    #se dibuja ubicación de hospital seleccionado
    plt.scatter(x=float(csv[index][2]), y=float(csv[index][3]), color='r', zorder = 1, s=200)
    #se dibuja ubicación de farmacias cercanas
    plt.scatter(x=[float(h[0][2]) for h in hospital], y=[float(h[0][3]) for h in hospital], color='g', zorder = 1, s=15)
    #se dibuja farmacia mas cercana	
    plt.scatter(x=float(hospital[0][0][2]), y=float(hospital[0][0][3]), color='y', zorder = 1, s=50) #farmacia mas cercana	

#lambda para dibujar una linea desde hospital a farmacias cercanas
draw_line = lambda start, end: plt.plot([float(start[2]), float(end[0][2])], [float(start[3]), float(end[0][3])],'b-.', zorder=0, linewidth=0.5)

def get_closer_pharmacy(name, max_range, price):
  #se obtienen los datos de la dataset subida al repositorio de GitHub
  hospitals_csv = pd.read_csv("https://raw.githubusercontent.com/JonatanCuri07/TF_Complejidad_Algoritmica/master/Hospitales_Final.csv").to_numpy()
  farmacias_csv = pd.read_csv("https://raw.githubusercontent.com/JonatanCuri07/TF_Complejidad_Algoritmica/master/Farmacias_Final_VF.csv").to_numpy()
  index_hospital = np.where(hospitals_csv==name)[0][0]
  print(name, max_range, price)
  
  hospitals = making_adjacency_list(hospitals_csv, farmacias_csv, float(max_range), price)
  hospital = hospitals[index_hospital]
  hospital = divide_and_conquer(hospital)
  
  print("La farmacia más cercana es ",hospital[0][0][0], ", está ubicada en ", hospital[0][0][1]," a una distancia de ", hospital[0][1], "km")

  resultado["text"] = f"La farmacia más cercana es {hospital[0][0][0]}, está ubicada en {hospital[0][0][1]} a una distancia de {hospital[0][1]} km"

  for h in hospital:
    #se dibuja una linea para conectar hospital como máximo con las 50 farmacias más cercanas
    draw_line(hospitals_csv[index_hospital], h)
  draw_points(hospitals_csv, index_hospital, hospital)
  plt.show()

def ventana1():
    v1=Tk()
    v1.title("Programa")
    v1.geometry("1200x700")
    v1.configure(bg="black")

    #texto de hospital
    hospital = Label(v1, text="Nombre del Hospital:", font=("Times New Roman",15), bg="black", fg="white").place(x=10,y=10)
    txthospital = ttk.Entry(v1, width=30)
    txthospital.pack()
    txthospital.place(x=200,y=15)

    #eleccion
    eleccion = Label(v1, text="Precio:", font=("Times New Roman",15), bg="black", fg="white").place(x=10,y=50)
    combo = ttk.Combobox(v1, state="readonly", values=["Economico", "Costoso"])
    combo.pack()
    combo.place(x=200,y=55)

    #Rango
    rango = Label(v1, text="Rango de distancia:", font=("Times New Roman",15), bg="black", fg="white").place(x=10,y=90)
    txtrango = ttk.Entry(v1, width=30)
    txtrango.pack()
    txtrango.place(x=200,y=95)

    #boton
    btninicio = Button(v1, text="Comenzar el programa", font=("Times New Roman",15), command=lambda:get_closer_pharmacy(txthospital.get(), txtrango.get(), combo.get())).place(x=450, y = 55)   

    global resultado
    resultado = Label(v1, font=('Calibri', 10), bg="black", fg="white", text="")
    resultado.pack()
    resultado.place(x=10,y=135)


    v1.mainloop()

def mensaje():
    messagebox.showinfo("Creadores", "Creado por: \n *Kendall Contreras \n *Gabriela Nomberto \n *Jonatan Curi")

def salir():
    ventana.destroy()