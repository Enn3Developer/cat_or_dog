import asyncio
import numpy as np
import os
import sys
import cv2
from tqdm import tqdm
import random
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Flatten
from tensorflow.keras.layers import Conv2D, MaxPooling2D

DATADIR = "PetImages"
CATEGORIES = ["Dog", "Cat"]
IMG_SIZE = 100

# per scaricare il dataset vai su:
# https://www.microsoft.com/en-us/download/confirmation.aspx?id=54765

async def prepare_data(filepath):
    img_array = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)  # legge l'immagine e la converte in scala grigi
    new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))  # ridimensiona l'immagine per ottenere le dimensioni che si aspetta il modello
    return new_array.reshape(-1, IMG_SIZE, IMG_SIZE, 1)  # ritorna l'immagine con la forma che si aspetta il modello

async def create_training_data():
    training_data = []
    for category in CATEGORIES:  # cani e gatti
        path = os.path.join(DATADIR,category)  # crea un percorso ai cani e gatti
        class_num = CATEGORIES.index(category)  # ricevi una classificazione (0 o 1). 0=cane 1=gatto
        for img in tqdm(os.listdir(path)):  # itera per ogni immagine di cani e gatti
            try:
                img_array = cv2.imread(os.path.join(path,img) ,cv2.IMREAD_GRAYSCALE)  # converti in array
                new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))  # normalizza i dati
                training_data.append([new_array, class_num])  # aggiungi ai dati di allenamento
            except Exception as e:  # meglio prevenire che curare
                pass
    random.shuffle(training_data)  # mischia i dati per evitare che il modello venga allenato male
    return training_data

async def train():
    x = []
    y = []
    for features, label in await create_training_data():
        x.append(features)
        y.append(label)
    x = np.array(x).reshape(-1, IMG_SIZE, IMG_SIZE, 1)
    x = x / 255.0
    x = np.array(x)
    y = np.array(y)
    model = Sequential()
    model.add(Conv2D(64, (3, 3), input_shape=x.shape[1:]))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    # 3 conv layers -- START --
    # 1:
    model.add(Conv2D(64, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    # 2:
    model.add(Conv2D(64, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    # 3:
    model.add(Conv2D(64, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    # 3 conv layers -- END --
    model.add(Flatten())  # questo converte la nostra mappa delle feature in 3D ad un vettore di feature in 1D
    model.add(Dense(1))
    model.add(Activation('sigmoid'))
    model.compile(loss='binary_crossentropy',
                optimizer='adam',
                metrics=['accuracy'])
    model.fit(x, y, batch_size=32, epochs=10, validation_split=0.3)
    model.save("cat_or_dog.model")
    return model

async def get_model():
    if not os.path.exists("cat_or_dog.model"):
        model = await train()
    else:
        model = tf.keras.models.load_model("cat_or_dog.model")
    return model

async def predict(model: Sequential, filepath):
    prediction = model.predict([await prepare_data(filepath)])
    return CATEGORIES[round(prediction[0][0])], prediction[0][0]


# test
async def test():
    model = await get_model()
    prediction = await predict(model, "./dog_0.jpg")
    print(f"Type expected: Dog; Acc: {(1 - prediction[1]) * 100: .2f}%")
    prediction = await predict(model, "./cat_0.jpg")
    print(f"Type expected: Cat; Acc: {prediction[1] * 100: .2f}%")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())