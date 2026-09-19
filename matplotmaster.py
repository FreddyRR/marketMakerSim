import matplotlib.pyplot as plt
import numpy as np
import random

def coinToss(n):
    yValues = [i for i in range(1, n+1)]
    heads = 0
    for i in range(n):
        heads += random.randint(0, 1)
        yValues[i] = 2*heads - i - 1

    xValues = [i for i in range(1, n+1)]
    fig, ax = plt.subplots()
    ax.plot(xValues, yValues)
    plt.title("1D Random Walk")
    ax.set_xlim([0, n])
    plt.show()


def twoDWalk(steps):
    xValues = [i for i in range(0, steps+1)]
    yValues = [i for i in range(0, steps+1)]
    x, y = 0, 0
    for i in range(steps):
        choice = random.randint(1, 4)
        match choice:
            case 1:
                x = x+1
            case 2:
                x = x-1
            case 3:
                y = y+1
            case _:
                y = y-1
        xValues[i+1] = x
        yValues[i+1] = y
    fig, ax = plt.subplots()
    ax.plot(xValues, yValues, "purple", linewidth=1.5)
    ax.grid(True)
    plt.title("2D Random Walk")
    plt.show()

def twoDGauss(steps):
    xValues = [i for i in range(0, steps+1)]
    yValues = [i for i in range(0, steps+1)]
    x, y = 0, 0
    for i in range(steps):
        x += random.gauss(0, 1)
        y += random.gauss(0, 1)
        xValues[i+1] = x
        yValues[i+1] = y
    fig, ax = plt.subplots()
    ax.plot(xValues, yValues, "orange", linewidth=1.5)
    ax.grid(True)
    plt.title("2D Gaussian Walk")
    plt.show()

def oneDGauss(steps, mu, sigma):
    yValues = [i for i in range(0, steps+1)]
    y = 0
    for i in range(steps):
        y += random.gauss(mu, sigma)
        yValues[i+1] = y

    xValues = [i for i in range(0, steps+1)]
    fig, ax = plt.subplots()
    ax.plot(xValues, yValues, "pink")
    plt.title("1D Gaussian Walk")
    ax.set_xlim([0, steps])
    plt.show()
oneDGauss(1000000, 0.01, 6)