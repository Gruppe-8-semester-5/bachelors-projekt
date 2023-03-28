
import numpy as np
from datasets.winequality.files import read_wine_data
from analysis.lipschitz import lipschitz_binary_neg_log_likelihood
from datasets.winequality.wine import Wine
from models.logistic_regression import predict
from models.logistic_regression import gradient
from algorithms import simple_gradient_descent
from algorithms import GradientDescentResult
from models.utility import accuracy
# Construct np array of features
dataset = read_wine_data()
wines: list[Wine] = list(map(lambda d: Wine(d), dataset))
feature_list = list(map(lambda wine: wine.get_feature_vector(), wines))
feature_array = np.array(feature_list)
lipschitz = lipschitz_binary_neg_log_likelihood(feature_array)
print(f"lipschitz = {lipschitz}")
n = len(dataset)
print(f"n = {n}")


def color_to_label(color):
    if color == "white":
        return 0
    return 1

example_wine = wines[0]
print("feature example", example_wine.get_feature_vector())
print("Label example", color_to_label(example_wine.get_color())) 

color_label_list = list(map(lambda wine: color_to_label(wine.get_color()), wines))
color_label_array = np.array(color_label_list)

feature_size = example_wine.get_feature_vector().size

descent_result: GradientDescentResult = simple_gradient_descent.find_minima(
    np.random.rand(feature_size), 
    1/lipschitz * 00.1, 
    lambda w: gradient(feature_array, color_label_array, w), 
    max_iter=216200,
    epsilon=1.0e-2)

print(descent_result.get_final_point())


w = descent_result.get_final_point()
dataset = read_wine_data()
wines: list[Wine] = list(map(lambda d: Wine(d), dataset))
example_wine = wines[len(wines) - 1].get_feature_vector()
print(wines[len(wines)-1].get_quality())


predictions = []
for wine in wines:
    predictions.append(predict(w, wine.get_feature_vector()))

print(f"Accuracy:{np.round(accuracy(predictions, color_label_array)* 100,decimals=2)}%")

