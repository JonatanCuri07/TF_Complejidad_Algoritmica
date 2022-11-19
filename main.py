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