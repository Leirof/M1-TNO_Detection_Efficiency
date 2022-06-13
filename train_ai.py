
print("⌛ Loading libs...")

import os,sys
import data_io
import numpy             as np
import matplotlib.pyplot as plt
import pandas            as pd
import tensorflow        as tf
from   IPython.display   import display
from   tensorflow        import keras
from   classes.block     import Block
from   classes.triplet   import Triplet
from   classes.shot      import Shot
from   classes.ccd       import CCD

print("🧮 Collecting dataset...")

data = data_io.get_ai_ready(func="tan",subsets_per_block=500)

# Normalization
mean = data[:,:-4].mean()
std  = data[:,:-4].std()
data[:,:-4] = (data[:,:-4] - mean) / std

n = 100 # number of loops
model = None
for i in range(n):
  print(f"🔁 Loop {i+1}/{n}")

  print("🔀 Dataset shuffling...")

  np.random.shuffle(data)

  print("🗃️ Creating folds...")

  K=5
  folds = []
  for j in range(K):
    folds.append(data[j::K])

  print("📊 Splitting data for training and test...")

  x_train = []; y_train = []; x_test = []; y_test = []
  for j, fold in enumerate(folds):
    train_prop = 0.7
    train_sets = int(len(fold)*train_prop)
    index = np.zeros(len(fold),dtype=bool)
    index[:train_sets] = True
    np.random.shuffle(index)

    data_train = fold[index]
    data_test  = fold[~index]

    x_train.append(data_train[:,:-4])
    y_train.append(data_train[:,-4:])
    x_test.append(data_test [:,:-4])
    y_test.append(data_test [:,-4:])
  
  x_train = np.array(x_train); y_train = np.array(y_train); x_test = np.array(x_test); y_test = np.array(y_test)
  
  print("🧬 Creating model...")
    
  def get_model(x_train):
    model = keras.models.Sequential()
    model.add(keras.layers.Input((len(x_train[0]),), name="InputLayer"))
    model.add(keras.layers.Dense(64, activation='relu', name='Dense_n1'))
    model.add(keras.layers.Dense(64, activation='relu', name='Dense_n2'))
    model.add(keras.layers.Dense(64, activation='relu', name='Dense_n3'))
    model.add(keras.layers.Dense(4, name='Output'))
    model.compile(optimizer = 'adam', loss = 'mse', metrics = ['accuracy'])#['mae', 'mse'] )
    return model

  models = []; history = []; scores = []
  for j in range(K):
    X = np.concatenate(x_train[np.arange(len(x_train))!=j])
    Y = np.concatenate(y_train[np.arange(len(y_train))!=j])

    if model is None: models.append(get_model(X))
    else: models.append(model)

    print(f"🏃‍♀️ Training AI with fold {j} as test...")

    history.append(models[j].fit(X, Y, epochs = 60, batch_size = 10, verbose = 0, validation_data = (x_test[j], y_test[j])))

    # print("👀 Evaluation...")

    scores.append(models[j].evaluate(x_test[j], y_test[j], verbose=0))
    print(f"Score of this training: {scores[j][0]}")

  maxScore = scores[0][0]
  model = models[0]
  for j,s in enumerate(scores):
    if s[0] > maxScore:
      maxScore = s[0]
      model = models[j]

  print("🔮 Prediction...")
  
  new_data = Block.all["2015BD"].to_ai_ready(func="square")

  new_x = new_data[:-4]
  new_y = new_data[-4:]

  new_x = (new_x - mean) / std

  new_x=np.array(new_x).reshape(1,len(new_x))

  predictions = model.predict(new_x)
  print(predictions)

  def ft(m,a,b,c,d):
      return a/4 * (1-np.tanh((m-b)/c)) * (1-np.tanh((m-b)/d))

  def fs(m,a,b,c,d):
      return (a-b*(m-21)**2) / (1+np.exp((m-c)/d))

  m = np.linspace(21,25.5,1000)

  plt.subplot(int(np.ceil(np.sqrt(n))),int(np.ceil(np.sqrt(n))),i+1)
  plt.plot(m,ft(m,*predictions[0]), label="Machine Learning")
  plt.plot(m,fs(m,new_y[0],new_y[1],new_y[2],new_y[3]), label="Excpected")
  if i == 0: plt.title("TNO efficiency rate")
  if i+1>n-np.ceil(np.sqrt(n)):    plt.xlabel("Magnitude")
  if i%np.ceil(np.sqrt(n))==0: plt.ylabel("Efficiency")
  plt.grid()
  if i==0: plt.legend()

plt.save("tno_efficiency_rate.png")
model.save("model.ckpt")
plt.show()