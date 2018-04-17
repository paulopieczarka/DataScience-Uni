from matplotlib import pyplot as plt
import numpy as np

def gen_barh(data, names, xlabel="", title=""):
    y_pos = np.arange(len(data))
    plt.barh(y_pos, data, align='center', alpha=0.5)
    plt.yticks(y_pos, names)
    plt.xlabel(xlabel)
    plt.title(title)
    return plt

def plot_barh(data, names, xlabel="", title=""):
    plt = gen_barh(data, names, xlabel, title)
    plt.show()

def gen_line(data, xlabel="", ylabel="", title=""):
    plt.plot(data)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.title(title)
    return plt

def plot_line(data, xlabel="", ylabel="", title=""):
    plt = gen_line(data, xlabel, ylabel, title)
    plt.show()