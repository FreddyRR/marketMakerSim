import matplotlib.pyplot as plt
import numpy as np
import random

def simulation(startPrice, spreadRadius, totalTime, pBuyer, pSeller, mu, sigma, gamma, detailed):
    inventory, cash, buyers, sellers, pnl = 0, 0, 0, 0, 0
    priceValues = [startPrice for i in range(totalTime+1)]
    resPriceValues = [startPrice for i in range(totalTime+1)]
    bidValues = [startPrice - spreadRadius for i in range(totalTime+1)]
    askValues = [startPrice + spreadRadius for i in range(totalTime+1)]
    pnlValues = [0 for i in range(totalTime+1)]
    price = startPrice
    for i in range(totalTime):
        price += random.gauss(mu, sigma)
        timeRemaining = (totalTime - i - 1) / totalTime
        reservationPrice = price - inventory * gamma * sigma**2 * timeRemaining
        bid = price - spreadRadius
        ask = price + spreadRadius
        priceValues[i+1] = price
        resPriceValues[i+1] = reservationPrice
        bidValues[i+1] = bid
        askValues[i+1] = ask
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
    
    if detailed:
        fig, ax = plt.subplots()
        ax.plot(priceValues, "black", label="Price", linewidth=1.5)
        ax.plot(resPriceValues, "purple", label="Reservation Price", linewidth=1.5)
        ax.plot(bidValues, "green", label="Bid", linewidth=1.5)
        ax.plot(askValues, "red", label="Ask", linewidth=1.5)
        plt.legend()
        fig, ax = plt.subplots()
        ax.plot(pnlValues, "pink", label="PNL")
        plt.show()
    return pnl

'''totalPNL = 0
for i in range(5000):
    totalPNL += simulation(100, 0.05, 1000, 0.1, 0.1, 0, 1, 0.1, False)
print("Total PNL: " + str(totalPNL))
print("Average PNL: " + str(totalPNL/50000))'''

simulation(100, 0.1, 100, 0.1, 0.1, 0, 1, 0.1, True)