# TF_Complejidad_Algoritmica
Repositorio creado a fin de desarrollar el Trabajo Parcial y Final de Complejidad Alogritmica

# Integrantes

| * | Integrantes |
| ------ | ------ |
| 1 | Kendall Ramiro Contreras Salazar |
| 2 | Gabriela Soledad Nomberto Ramos |
| 3 | Jonatan Omar Curi Montero |

# Planteamiento de la Problematica

El problema es de obtención de medicamentos lo más pronto posible, debido a que usualmente los usuarios no les alcanzan los medicamentos brindados por los hospitales.
Para ello desarrollamos los siguientes puntos:
- La variable de costo fue realizada de manera aleatoria
- Multiples farmacias para cada hospital 
- El usuario elegirá sus preferencias en cuanto a los costos


# Video del primer hito
https://www.youtube.com/watch?v=w9Fq17Of3KM

# Conceptos a considerar

Para empezar necesitamos calcular la distancia entre 2 puntos utilizando la libreria geopy, y nos la devolverá en kilometros. El punto de inicio siempre será el hospital elegido y el punto 2 las farmacias con las que se va a comprobar.

```python
def distance_between_points(point1, point2): #point1 / punto de inicio, point2 / punto final
    #se calcula la distancia entre puntos de longitud y latitud en kilometros
    return geopy.distance.geodesic((float(point1[3]), float(point1[2])), (float(point2[3]),float(point2[2]))).km
```


La siguiente función, realizará una lista de adyacencia para los hospitales utilizando fuerza bruta. Asimismo, se hace una comparación con el rango máximo y el precio ingresado por el usuario.
```python
def making_adjacency_list(hospitals_csv, farmacias_csv, max_range, price = "Economico"):
  hospitals = []
  for _ in range(len(hospitals_csv)):
    hospitals.append([])

  for x in range(len(hospitals_csv)):
    for y in range(len(farmacias_csv)):
      dis = distance_between_points(hospitals_csv[x],farmacias_csv[y]) #obtener la distancia entre el hospital y la farmacia
      if dis <= max_range and farmacias_csv[y][4] == price and len(hospitals[x])<50: #se compara si la farmacia cumple requisitos del usuario
        hospitals[x].append((farmacias_csv[y], dis))
  return hospitals #se retorna arreglo de hospitales con sus farmacias cercanas
```


El objetivo de esta funcion es ordenar el arreglo ingresado, para tener las farmacias de manera ascendente para escoger el primer valor, el cual será el más cercano, debido a que se está ordenando según la proximidad.

```python
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
```

En la siguiente función se lee el data set de hospitales para utilizar el ingresado por el usuario, luego llamaremos las funcio,es anteriores para escoger la farmacia más cercana y se dibujará la conexión de 50 farmacias como máximo por cada hospital.
```python
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
  draw_all(hospitals_csv, hospitals)
  plt.show()
```
![image](https://user-images.githubusercontent.com/48858578/203430062-41957fe2-877d-46df-84f4-dd202211fa0c.png)

# Video del Trabajo Final
https://youtu.be/gNqUcKklvzE
