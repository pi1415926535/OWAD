from neural_network.data_manipulation import load_data
import numpy as np
from genetic.neat import NEAT
import copy
from neural_network.plots import plot_data_2d, plot_measure_results_data
import matplotlib.pyplot as plt
from sklearn.preprocessing import OneHotEncoder
from neural_network.activations import softmax

# load dataset
train, test = load_data(file_name='rings3-regular', folder='classification', classification=True)

# x and y - observations and values for them
x = train[:, 0:2]
y = train[:, 2:3]
ohe = OneHotEncoder(sparse=False)
y_ohe = ohe.fit_transform(train[:, 2:3])


# create score function for easy
def score_function(res, type="score"):
    results = np.vstack([res[2], res[3], res[4]])
    results = softmax(results).transpose()
    if type == "score":
        return - np.sum((results - y_ohe)**2) / res[2].shape[0] / 3
    else:
        results = results.transpose()
        return np.sum(train[:, 2] == np.argmax(results, axis=0)) / res[2].shape[0]


# res = {2: np.array([1,2,3]), 3: np.array([3,1,2]), 4: np.array([0,4,0])}
data = {0: train[:, 0], 1: train[:, 1]}

# plot data classes
plt.figure(figsize=(12.8, 9.6))
plt.subplot(2, 2, 1)
plot_data_2d(x[:, 0], x[:, 1], y[:, 0], title='True classes of points on the plane', show=False)

n_input = 2
n_output = 3
n = 200
scores, accuracies = [], []
labels = ["Without speciation, maximize accuracy", "With speciation, maximize accuracy", "With speciation, maximize score"]
for index, score_type, speciation in zip([2, 3, 4], ["accuracy", "accuracy", "score"], [False, True, True]):
    neat = NEAT(n_input, n_output, n, score_function, data, 1.3, 15, score_type, use_speciation=speciation)

    for i in range(50):
        print(f'Start of epoch: {i+1}')
        neat.epoch(i)

    scores.append(neat.best_scores)
    accuracies.append(neat.best_accuracies)

    best = neat.get_best_population("accuracy")[0]
    res = neat.population[best].evaluate(copy.deepcopy(data))
    results = np.vstack([res[2], res[3], res[4]])
    y_predicted = np.argmax(results, axis=0)
    plt.subplot(2, 2, index)
    plot_data_2d(x[:, 0], x[:, 1], y_predicted, title=labels[index-2], show=False)

plt.show()

# plot_measure_results_data(scores, title_base="Score ", ylabel="Score ", labels=labels, from_error=0, y_log=True)
plot_measure_results_data(accuracies, title_base="Accuracy ", ylabel="Accuracy ", labels=labels, from_error=0)

