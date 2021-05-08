#!/usr/bin/env python3

import numpy as np
import imageio
from PIL import Image
import sys



def probabilities(image): #calculem la probabilitat dels colors sobre la imatge
    #image = image.reshape(image.shape[0]*image.shape[1]//2, 2)
    
    probs = {}
    
    for x in image:
        x = str(x[0])+str(x[1]) #concateno els dos valors per identificar el punt dins el dict
        if x not in probs:
            probs[x] = 1
        else:
            probs[x] +=1

    for (value, prob) in probs.items():
        probs[value] /= (image.shape[0]*image.shape[1])

    return probs


def quantize(image):
    print('Trobant els centroides que convergeixen...')
    #2. Select N codewords at random, and let that be the initial codebook
    centroids =[[50,50], [100,100], [150,150], [200,200]]
    oldCentroids=[]
    cont =0
    done = False


    while done == False:

        dictPoints ={}    
        dictPoints[0] = []
        dictPoints[1] = []
        dictPoints[2] = []
        dictPoints[3] = []

        #3. Using the Euclidean distance measure clusterize the vectors around each codeword
        image = image.reshape(image.shape[0]*image.shape[1]//2, 2)

        #Calculem quin es el centroide mes proper al punt
        for i in img:
            dist = []
            dist.append(np.average(np.square(i-centroids[0])))
            dist.append(np.average(np.square(i-centroids[1])))
            dist.append(np.average(np.square(i-centroids[2])))
            dist.append(np.average(np.square(i-centroids[3])))
            dist = np.asarray(dist)

            dictPoints[np.argmin(dist)].append([i[0], i[1]])


        probSum = [0 for i in range(4)]
        valRepresentatiu = [[0,0] for i in range(4)]
        pr = probabilities(img)

        for i in dictPoints.keys():
            probSum[i] = 0
            valRepresentatiu[i] = 0

            for pixel in dictPoints[i]:
                #calculem el valor representatiu d'aquest conjunt

                conc = str(pixel[0])+str(pixel[1])
                pixel = np.asarray([pixel[0],pixel[1]])

                if conc in pr.keys():
                    valRepresentatiu[i] += pr[conc] * pixel
                    probSum[i] += pr[conc]
                else:
                    valRepresentatiu[i] += 0 * pixel
                    probSum[i] += 0

                # dividim entre el sumatori de les probabilitsts del conjunt
            if valRepresentatiu[i].any() != 0:
                valRepresentatiu[i] /= probSum[i]

        #print(valRepresentatiu)
        centroids = np.asarray(valRepresentatiu).tolist()

        if oldCentroids == centroids:
            done = True
        else:
            oldCentroids = centroids

        cont+=1
        print('Iteració', cont)
        #print('Centroides:', centroids)

    print('Els centroides que convergeixen son:', centroids)
    return centroids

def classify_quantizer(img, centroids): #per saber a quin centroide pertany cada pixel
    #img = img.reshape(img.shape[0]*img.shape[1]//2, 2)

    distances = []

    for cent in centroids:
        distances.append(np.average(np.square(img-cent), axis =1))

    a = np.vstack(distances)
    #print(a)

    b = np.argmin(a, axis=0)
    return b


img = imageio.imread(sys.argv[1])
shape_x_orig = img.shape[0]
shape_y_orig = img.shape[1]
img = img.reshape(img.shape[0]*img.shape[1]//2, 2)

centroids = quantize(img)
b = classify_quantizer(img, centroids)



print("creant i omplint el fitxer .bin ...")
#envio 8 valors ints cada 3 bytes --> 
cont =0
suma =0
cont2 =0
#print(img)

with open(sys.argv[2], "wb+") as f:

    # header:
    f.write(int(shape_x_orig).to_bytes(2, byteorder="big", signed=False))
    f.write(int(shape_y_orig).to_bytes(2, byteorder="big", signed=False))

    # guardem al header els centroides de reconstruccio
    for i in range(len(centroids)):
        for j in range(len(centroids[i])):
            f.write(int(centroids[i][j]).to_bytes(2, byteorder="big", signed=False))
    
    for i in range(len(b)): #x

        suma  = suma << 2
        suma |= b[i]
        cont+=1

        if cont == 8:
            f.write(int(suma).to_bytes(3, byteorder='big', signed=False))
            cont2+=1
            suma =0
            cont=0
                   
    
print(cont2, 'escritures')