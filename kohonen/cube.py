from kohonen.data_manipulation import load_data
from kohonen.Kohonen import Kohonen
import matplotlib.pyplot as plt
from neural_network.plots import plot_data_2d
from kohonen.train import find_epochs_and_neighbour

# load data
data, classes = load_data("cube")

find_epochs_and_neighbour(data, classes, 5, 5, [5, 10, 20], [0.1, 0.2, 0.5, 1], use_pca=True)
find_epochs_and_neighbour(data, classes, 5, 5, [5, 10, 20], [0.005, 0.01, 0.015, 0.03], distance_type="mexican", use_pca=True)

# Gauss
# create network
network = Kohonen(5, 5, 3, neighbour_param=0.2, distance_type="gauss")
network.learn_epochs(data, epochs=10)

# plot network
plot_data_2d(data[:, :1], data[:, 1:], classes, show=False, title="Cube dataset, Gauss metric")
network.plot_weights()
plt.show()


# Mexican hat
# create network
network = Kohonen(5, 5, 3, neighbour_param=0.015, distance_type="mexican")
network.learn_epochs(data, epochs=10)

# plot network
plot_data_2d(data[:, :1], data[:, 1:], classes, show=False, title="Cube dataset, Mexican hat metric")
network.plot_weights()
plt.show()

# Results:
# Mainly the same as in hexagon, but in 3d it is harder to see it
