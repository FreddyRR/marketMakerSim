import matplotlib.pyplot as plt
import random
import math

def simulation(startPrice, totalTime, pBuyer, pSeller, mu, sigma, gamma, liquidity, detailed):
    inventory, cash, buyers, sellers, pnl = 0, 0, 0, 0, 0
    priceValues = [startPrice for i in range(totalTime+1)]
    resPriceValues = [startPrice for i in range(totalTime+1)]
    pnlValues = [0 for i in range(totalTime+1)]
    spreadValues = [0 for i in range(totalTime+1)]
    spreadValues[0] = gamma * sigma**2 * totalTime + (2 / gamma) * math.log(1 + (gamma / liquidity))
    bidValues = [startPrice - spreadValues[0]/2 for i in range(totalTime+1)]
    askValues = [startPrice + spreadValues[0]/2 for i in range(totalTime+1)]
    price = startPrice

    for i in range(totalTime):
        price += random.gauss(mu, sigma)
        timeRemaining = totalTime - i - 1
        reservationPrice = price - inventory * gamma * sigma**2 * timeRemaining
        spread = gamma * sigma**2 * timeRemaining + (2 / gamma) * math.log(1 + (gamma / liquidity))   # Spread gets tighter, less risk-averse as time goes on
        bid = reservationPrice - spread/2
        ask = reservationPrice + spread/2
        priceValues[i+1] = price
        resPriceValues[i+1] = reservationPrice
        bidValues[i+1] = bid
        askValues[i+1] = ask
        spreadValues[i+1] = spread
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
        fig, ax = plt.subplots()
        ax.plot(spreadValues, "orange", label="Spread")
        plt.show()
    return pnl

'''totalPNL = 0
for i in range(5000):
    totalPNL += simulation(100, 1000, 0.1, 0.1, 0, 1, 1, 1.5, False)
print("Total PNL: " + str(totalPNL))
print("Average PNL: " + str(totalPNL/50000))'''

simulation(100, 200, 0.1, 0.1, 0, 1, 0.01, 1.5, True)