#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Robótica Computacional
# Grado en Ingeniería Informática (Cuarto)
# Práctica: Resolución de la cinemática directa mediante Denavit-Hartenberg.

# Ejemplo:
# ./cdDH.py 30 45

import sys
from math import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from mpl_toolkits.mplot3d import Axes3D

# ******************************************************************************
# Declaración de funciones

def ramal(I,prev=[],base=0):
  # Convierte el robot a una secuencia de puntos para representar
  O = []
  if I:
    if isinstance(I[0][0],list):
      for j in range(len(I[0])):
        O.extend(ramal(I[0][j], prev, base or j < len(I[0])-1))
    else:
      O = [I[0]]
      O.extend(ramal(I[1:],I[0],base))
      if base:
        O.append(prev)
  return O

def muestra_robot(O,ef=[]):
  # Pinta en 3D
  OR = ramal(O)
  OT = np.array(OR).T
  fig = plt.figure()
  ax = fig.add_subplot(111, projection='3d')
  # Bounding box cúbico para simular el ratio de aspecto correcto
  max_range = np.array([OT[0].max()-OT[0].min()
                       ,OT[1].max()-OT[1].min()
                       ,OT[2].max()-OT[2].min()
                       ]).max()
  Xb = (0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][0].flatten()
     + 0.5*(OT[0].max()+OT[0].min()))
  Yb = (0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][1].flatten()
     + 0.5*(OT[1].max()+OT[1].min()))
  Zb = (0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][2].flatten()
     + 0.5*(OT[2].max()+OT[2].min()))
  for xb, yb, zb in zip(Xb, Yb, Zb):
     ax.plot([xb], [yb], [zb], 'w')
  ax.plot3D(OT[0],OT[1],OT[2],marker='s')
  ax.plot3D([0],[0],[0],marker='o',color='k',ms=10)
  if not ef:
    ef = OR[-1]
  ax.plot3D([ef[0]],[ef[1]],[ef[2]],marker='s',color='r')
  ax.set_xlabel('X')
  ax.set_ylabel('Y')
  ax.set_zlabel('Z')
  plt.show()
  return

def arbol_origenes(O,base=0,sufijo=''):
  # Da formato a los origenes de coordenadas para mostrarlos por pantalla
  if isinstance(O[0],list):
    for i in range(len(O)):
      if isinstance(O[i][0],list):
        for j in range(len(O[i])):
          arbol_origenes(O[i][j],i+base,sufijo+str(j+1))
      else:
        print('(O'+str(i+base)+sufijo+')0\t= '+str([round(j,3) for j in O[i]]))
  else:
    print('(O'+str(base)+sufijo+')0\t= '+str([round(j,3) for j in O]))

def muestra_origenes(O,final=0):
  # Muestra los orígenes de coordenadas para cada articulación
  print('Orígenes de coordenadas:')
  arbol_origenes(O)
  if final:
    print('E.Final = '+str([round(j,3) for j in final]))

def matriz_T(d,theta,a,alpha):
  # Calcula la matriz T (ángulos de entrada en grados)
  th=theta*pi/180;
  al=alpha*pi/180;
  return [[cos(th), -sin(th)*cos(al),  sin(th)*sin(al), a*cos(th)]
         ,[sin(th),  cos(th)*cos(al), -sin(al)*cos(th), a*sin(th)]
         ,[      0,          sin(al),          cos(al),         d]
         ,[      0,                0,                0,         1]
         ]
# ******************************************************************************

plt.ion() # Modo interactivo
# Introducción de los valores de las articulaciones
nvar=6 # Número de variables
if len(sys.argv) != nvar+1:
  sys.exit('El número de articulaciones no es el correcto ('+str(nvar)+')')
p=[float(i) for i in sys.argv[1:nvar+1]]

#-#-# Manipulador 4

# Parámetros D-H:
#         0' 1     2        3     4   4.1    4.2   5.1       7    5.2   6.1    6.2
d  = [ p[0], 0,    0,       0,    5,    0,     0,    1, 1+p[5],     1, p[5], p[5]]
th = [    0, 0, p[1], p[2]+90, p[3],    0,     0,    0,      0,     0,    0,    0]
a  = [    0, 2,    2,       0,    0, p[4], -p[4],    0,      0,     0,    0,    0]
al = [    0, 0,   90,      90,    0,    0,     0,    0,      0,     0,    0,    0]


# Orígenes para cada articulación
o00   =[0,0,0,1]
o0P0P   =[0,0,0,1]
o11   =[0,0,0,1]
o22   =[0,0,0,1]
o33   =[0,0,0,1]
o44   =[0,0,0,1]
o4141   =[0,0,0,1]
o4242   =[0,0,0,1]
o5252 =[0,0,0,1]
o5151 =[0,0,0,1]
o6262 =[0,0,0,1]
o6161 =[0,0,0,1]
o77   =[0,0,0,1]
# Cálculo matrices transformación
T00P =matriz_T(d [0],th [0],a [0],al [0])
T0P1 =matriz_T(d [1],th [1],a [1],al [1])
T01 =np.dot(T00P ,T0P1)
T12 =matriz_T(d [2],th [2],a [2],al [2])
T02 =np.dot(T01 ,T12)
T23 = matriz_T(d [3],th [3],a [3],al [3])
T03 =np.dot(T02, T23 )
T34 = matriz_T(d [4],th [4],a [4],al [4])
T04 =np.dot(T03, T34 )
T441 = matriz_T(d [5],th [5],a [5],al [5])
T041 =np.dot(T04, T441 )
T442 = matriz_T(d [6],th [6],a [6],al [6])
T042 =np.dot(T04, T442 )
T4151 = matriz_T(d [7],th [7],a [7],al [7])
T051 =np.dot(T041, T4151 )
T4252 = matriz_T(d [9],th [9],a [9],al [9])
T052 =np.dot(T042, T4252 )
T5161 = matriz_T(d [10],th [10],a [10],al [10])
T061 =np.dot(T051, T5161 )
T5262 = matriz_T(d [11],th [11],a [11],al [11])
T062 =np.dot(T052, T5262 )
T47 = matriz_T(d [8],th [8],a [8],al [8])
T07 =np.dot(T04, T47 )
# Transformación de cada articulación
o0P0  =np.dot(T00P , o0P0P ).tolist()
o10  =np.dot(T01 , o11 ).tolist()
o20  =np.dot(T02 , o22 ).tolist()
o30  =np.dot(T03 , o33 ).tolist()
o40  =np.dot(T04 , o44 ).tolist()
o410  =np.dot(T041 , o4141 ).tolist()
o420  =np.dot(T042 , o4242 ).tolist()
o510  =np.dot(T051 , o5151 ).tolist()
o520  =np.dot(T052 , o5252 ).tolist()
o610  =np.dot(T061 , o6161 ).tolist()
o620  =np.dot(T062 , o6262 ).tolist()
o70  =np.dot(T07 , o77 ).tolist()

# Mostrar resultado de la cinemática directa
muestra_origenes([o00 ,o10 ,o20 ,o30 ,o40, o510, o520, o610, o620, o70])

## Visualización interactiva del robot

ef = o70
OR = ramal([o00 ,o0P0 ,o10 ,o20 ,o30 ,o40 ,[[o410,o510, o610],[o420, o520, o620]]])
OT = np.array(OR).T
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

axcolor = 'lightgoldenrodyellow'
ax1 = fig.add_axes([0.25,0.01,0.65, 0.03])
ax2 = fig.add_axes([0.25,0.06,0.65, 0.03])
ax3 = fig.add_axes([0.25,0.11,0.65, 0.03])
ax4 = fig.add_axes([0.03,0.25,0.0225, 0.63])
ax5 = fig.add_axes([0.08,0.25,0.0225, 0.63])
ax6 = fig.add_axes([0.13,0.25,0.0225, 0.63])
#
v_extensor_slider = Slider(ax4, "L1", 0, 6, valinit=3, valstep=0.01,orientation="vertical")
elbow_slider = Slider(ax1, "theta2", -150, 150, valinit=0)
v_wrist_slider = Slider(ax2, "theta3", -150, 150, valinit=0)
h_wrist_slider = Slider(ax3, "theta4", -180, 180, valinit=0)
v_claw_slider = Slider(ax5, "L5", -90, 90, valinit=2, valstep=0.01,orientation="vertical")
h_claw_slider = Slider(ax6, "L6", -150, 150, valinit=1, valstep=0.01,orientation="vertical")

def update(val): 
  vxs = v_extensor_slider.val
  els = elbow_slider.val
  vws = v_wrist_slider.val
  hws = h_wrist_slider.val
  vcs = v_claw_slider.val
  hcs = h_claw_slider.val
  
  #-#-# Manipulador 4

  # Parámetros D-H:
  #         0' 1     2        3     4   4.1    4.2   5.1       7    5.2   6.1    6.2
  d  = [ vxs, 0,    0,       0,    5,    0,     0,    1, 1+hcs,     1, hcs, hcs]
  th = [    0, 0, els, vws+90, hws,    0,     0,    0,      0,     0,    0,    0]
  a  = [    0, 2,    2,       0,    0, vcs, -vcs,    0,      0,     0,    0,    0]
  al = [    0, 0,   90,      90,    0,    0,     0,    0,      0,     0,    0,    0]


  # Orígenes para cada articulación
  o00   =[0,0,0,1]
  o0P0P   =[0,0,0,1]
  o11   =[0,0,0,1]
  o22   =[0,0,0,1]
  o33   =[0,0,0,1]
  o44   =[0,0,0,1]
  o4141   =[0,0,0,1]
  o4242   =[0,0,0,1]
  o5252 =[0,0,0,1]
  o5151 =[0,0,0,1]
  o6262 =[0,0,0,1]
  o6161 =[0,0,0,1]
  o77   =[0,0,0,1]
  # Cálculo matrices transformación
  T00P =matriz_T(d [0],th [0],a [0],al [0])
  T0P1 =matriz_T(d [1],th [1],a [1],al [1])
  T01 =np.dot(T00P ,T0P1)
  T12 =matriz_T(d [2],th [2],a [2],al [2])
  T02 =np.dot(T01 ,T12)
  T23 = matriz_T(d [3],th [3],a [3],al [3])
  T03 =np.dot(T02, T23 )
  T34 = matriz_T(d [4],th [4],a [4],al [4])
  T04 =np.dot(T03, T34 )
  T441 = matriz_T(d [5],th [5],a [5],al [5])
  T041 =np.dot(T04, T441 )
  T442 = matriz_T(d [6],th [6],a [6],al [6])
  T042 =np.dot(T04, T442 )
  T4151 = matriz_T(d [7],th [7],a [7],al [7])
  T051 =np.dot(T041, T4151 )
  T4252 = matriz_T(d [9],th [9],a [9],al [9])
  T052 =np.dot(T042, T4252 )
  T5161 = matriz_T(d [10],th [10],a [10],al [10])
  T061 =np.dot(T051, T5161 )
  T5262 = matriz_T(d [11],th [11],a [11],al [11])
  T062 =np.dot(T052, T5262 )
  T47 = matriz_T(d [8],th [8],a [8],al [8])
  T07 =np.dot(T04, T47 )
  # Transformación de cada articulación
  o0P0  =np.dot(T00P , o0P0P ).tolist()
  o10  =np.dot(T01 , o11 ).tolist()
  o20  =np.dot(T02 , o22 ).tolist()
  o30  =np.dot(T03 , o33 ).tolist()
  o40  =np.dot(T04 , o44 ).tolist()
  o410  =np.dot(T041 , o4141 ).tolist()
  o420  =np.dot(T042 , o4242 ).tolist()
  o510  =np.dot(T051 , o5151 ).tolist()
  o520  =np.dot(T052 , o5252 ).tolist()
  o610  =np.dot(T061 , o6161 ).tolist()
  o620  =np.dot(T062 , o6262 ).tolist()
  o70  =np.dot(T07 , o77 ).tolist()
  
  ef = o70
  OR = ramal([o00 ,o0P0 ,o10 ,o20 ,o30 ,o40 ,[[o410,o510, o610],[o420, o520, o620]]])
  OT = np.array(OR).T
  max_range = np.array([OT[0].max()-OT[0].min()
                      ,OT[1].max()-OT[1].min()
                      ,OT[2].max()-OT[2].min()
                      ]).max()
  Xb = (0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][0].flatten()
      + 0.5*(OT[0].max()+OT[0].min()))
  Yb = (0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][1].flatten()
      + 0.5*(OT[1].max()+OT[1].min()))
  Zb = (0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][2].flatten()
      + 0.5*(OT[2].max()+OT[2].min()))
  ax.cla()
  for xb, yb, zb in zip(Xb, Yb, Zb):
      ax.plot([xb], [yb], [zb], 'w')
  ax.plot3D(OT[0],OT[1],OT[2],marker='s')
  ax.plot3D([0],[0],[0],marker='o',color='k',ms=10)
  if not ef:
    ef = OR[-1]
  ax.plot3D([ef[0]],[ef[1]],[ef[2]],marker='s',color='r')
  ax.set_xlabel('X')
  ax.set_ylabel('Y')
  ax.set_zlabel('Z')



# Bounding box cúbico para simular el ratio de aspecto correcto
max_range = np.array([OT[0].max()-OT[0].min()
                      ,OT[1].max()-OT[1].min()
                      ,OT[2].max()-OT[2].min()
                      ]).max()
Xb = (0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][0].flatten()
    + 0.5*(OT[0].max()+OT[0].min()))
Yb = (0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][1].flatten()
    + 0.5*(OT[1].max()+OT[1].min()))
Zb = (0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][2].flatten()
    + 0.5*(OT[2].max()+OT[2].min()))
for xb, yb, zb in zip(Xb, Yb, Zb):
    ax.plot([xb], [yb], [zb], 'w')
ax.plot3D(OT[0],OT[1],OT[2],marker='s')
ax.plot3D([0],[0],[0],marker='o',color='k',ms=10)
if not ef:
  ef = OR[-1]
ax.plot3D([ef[0]],[ef[1]],[ef[2]],marker='s',color='r')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

v_extensor_slider.on_changed(update)
elbow_slider.on_changed(update)
v_wrist_slider.on_changed(update)
h_wrist_slider.on_changed(update)
v_claw_slider.on_changed(update)
h_claw_slider.on_changed(update)
plt.show()

input()

