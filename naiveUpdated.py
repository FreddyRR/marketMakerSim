import matplotlib.pyplot as plt
import random
import math

def simulation(startPrice, spreadRadius, totalTime, pBuyer, pSeller, mu, sigma, detailed):
    inventory, cash, buyers, sellers, pnl = 0, 0, 0, 0, 0
    priceValues = [startPrice for i in range(totalTime+1)]
    bidValues = [startPrice - spreadRadius for i in range(totalTime+1)]
    askValues = [startPrice + spreadRadius for i in range(totalTime+1)]
    pnlValues = [0 for i in range(totalTime+1)]
    price = startPrice
    for i in range(totalTime):
        price += random.gauss(mu, sigma * math.sqrt(1 / totalTime))
        bid = price - spreadRadius
        ask = price + spreadRadius
        priceValues[i+1] = price
        bidValues[i+1] = bid
        askValues[i+1] = ask
        # Fixed probabilities of a single order for each of buy and sell separately
        if random.random() < pBuyer:
            buyers += 1
            inventory -= 1
            cash += ask
        if random.random() < pSeller:
            sellers += 1
            inventory += 1
            cash -= bid
        pnl = cash + inventory * price
        pnlValues[i+1] = pnl

    # This displays some nice graphs
    if detailed:
        fig, ax = plt.subplots()
        ax.plot(priceValues, "black", label="Price", linewidth=1.5)
        ax.plot(bidValues, "green", label="Bid", linewidth=1.5)
        ax.plot(askValues, "red", label="Ask", linewidth=1.5)
        plt.legend()
        fig, ax = plt.subplots()
        ax.plot(pnlValues, "pink", label="PNL")
        plt.show()
    return pnl

# Messing around with repeated simulations to find long-term PNL
def monteCarlo(n):
    totalPNL, squareSum = 0, 0
    simulationPNLList = [0 for i in range(n)]
    for i in range(n):
        simulationPNLList[i] = simulation(100, 0.1, 200, 0.1, 0.1, 0, 2, False)
        totalPNL += simulationPNLList[i]
        squareSum += (simulationPNLList[i])**2
    print("Total PNL: " + str(totalPNL))
    print("Mean PNL: " + str(totalPNL/n))
    print("Sample Variance: " + str((squareSum - totalPNL**2/n) /(n-1)))

simulation(100, 0.1, 200, 0.1, 0.1, 0, 2, True)
simulation(100, 0.1, 200, 0.1, 0.1, 0, 2, True)
monteCarlo(5000)