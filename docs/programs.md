# Programs

This project contain 2 main programs :

## serialize.py

This program will inspect all the raw data and serialize them. It only need to be executed once for a given data set. It will automatically save all the serialized data in JSON files in the `data` folder. On the main repo of this project, the initial data are already available in a JSON format. These file are needed to use the second program. You can adapt this program to your own data by editing the functions listed in the file `interface.py`.

## train_ai.ipynb

This Jupyter Notebook file is the heart of the project, where you can perform some tests on the AI.

Several parameters can be found at the top of the file:

- `subset_multiplier : int = 100`: increase the size of the subset by taking random composition of CCD
- `epoch : int = 60`: number of epochs for each AI training
- `n : int = 25`: number of generations for the genertic algorithm
- `K : int = 3`: number of folds (= number of independant AI per generation)
- `train_prop : float = 0.7`: proportion of the dataset used for training

All the results are stored in the `archive` folder, organized by date and version of the code (git hash) and then by a unique number followed by a parameters description.

In this folder, you can find:
- `model.ckpy` that contain the final model exported from TensorFlow. This folder is excluded from git because it can be heavy.
- `output.csv` which contain the accuracies of the AI over the generations.
- `tno_efficiency_rate.png` which is contain the graphs of the predictions made at the end of each generation.