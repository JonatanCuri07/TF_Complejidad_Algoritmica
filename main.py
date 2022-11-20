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

def divideyvenceras(hospital):
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
        lst_left=divideyvenceras(lst_left)
    if not len(lst_right)<=1:
        lst_right=divideyvenceras(lst_right)
    current = [current]
    hospital = lst_left + current + lst_right
    return(hospital)

def get_closer_pharmacy(name, max_range, price):
  #se obtienen los datos de la dataset subida al repositorio de GitHub
  hospitals_csv = pd.read_csv("https://raw.githubusercontent.com/JonatanCuri07/TF_Complejidad_Algoritmica/master/Hospitales_Final.csv").to_numpy()
  farmacias_csv = pd.read_csv("https://raw.githubusercontent.com/JonatanCuri07/TF_Complejidad_Algoritmica/master/Farmacias_Final_VF.csv").to_numpy()
  index_hospital = np.where(hospitals_csv==name)[0][0]
  print(name, max_range, price)
  
  hospitals = making_adjacency_list(hospitals_csv, farmacias_csv, float(max_range), price)
  hospital = hospitals[index_hospital]
  hospital = divideyvenceras(hospital)
  
  print("La farmacia más cercana es ",hospital[0][0][0], ", está ubicada en ", hospital[0][0][1]," a una distancia de ", hospital[0][1], "km")

  resultado["text"] = f"La farmacia más cercana es {hospital[0][0][0]}, está ubicada en {hospital[0][0][1]} a una distancia de {hospital[0][1]} km"
