#!/usr/bin/env python3

import numpy as np
import imageio
from PIL import Image
import sys

    
def classify_dequantizer(value, centroids): #metode per retornar el valor representatiu de cada conjunt
    return centroids[value]


print("convertint el .bin a imatge")
with open(sys.argv[1], "rb") as f:
    vec2=[]
    centroidsReconstructed = [[0 for x in range(2)] for y in range(4)]
    cont1 =0
    cont2 = 0

    read = f.read()

    # treiem header
    shape_x = int.from_bytes(read[:2], byteorder="big")
    shape_y = int.from_bytes(read[2:4], byteorder="big")

    #centroides de reconstruccio
    contRead = 4
    for i in range(4):
        for j in range(2):
            centroidsReconstructed[i][j] = int.from_bytes(read[contRead : contRead + 2], byteorder="big")
            contRead += 2

    print('Centroides recuperats:', centroidsReconstructed)
    
    
    read = read[contRead:]

    b = (shape_x * shape_y) // 2
    
    vecAux = [0 for i in range(b)]
        
    for i in range(b):
        #print(i)            
        if cont1 ==0:
            r = (int.from_bytes(read[cont2:cont2+3], byteorder='big'))
            
            for x in range(8):
                #print(r)
                r = bin(r)[2:]

                if (len(r[-2:])==2):
                    last=int(r[-2:], 2)
                    vecAux[i+7-x] = last
                    r = int(r, 2)
                    r -= last
                    r = r >> 2
                elif (len(r[-2:])==1):
                    last=int(r[-1:], 2)
                    if (i+7-x < b):
                        vecAux[i+7-x] = last
                    r = int(r, 2)
                    r -= last
                    r = r >> 1
            

            cont2+=3
        cont1+=1
        
        if cont1 == 8:
            cont1=0

    vecAux = np.asarray(vecAux)


imatgeRecuperada=[]

for i in range(len(vecAux)):
    imatgeRecuperada.append(classify_dequantizer(vecAux[i], centroidsReconstructed)[0])
    imatgeRecuperada.append(classify_dequantizer(vecAux[i], centroidsReconstructed)[1])

imatgeRecuperada = np.asarray(imatgeRecuperada)
imatgeRecuperada = np.asarray(imatgeRecuperada.reshape(shape_x, shape_y))
imatgeRecuperada = imatgeRecuperada.astype(dtype=np.uint8)

imgToSave = Image.fromarray(imatgeRecuperada)
imgToSave.save(sys.argv[2])
print("Imatge", sys.argv[2], "creada")
