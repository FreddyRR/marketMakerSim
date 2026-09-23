import matplotlib.pyplot as plt
import random
import math

def simulation(startPrice, totalTime, mu, sigma, gamma, liquidity, A, detailed):
    inventory, cash, buyers, sellers, pnl = 0, 0, 0, 0, 0
    priceValues = [startPrice for i in range(totalTime+1)]
    resPriceValues = [startPrice for i in range(totalTime+1)]
    pnlValues = [0 for i in range(totalTime+1)]
    spreadValues = [0 for i in range(totalTime+1)]
    spreadValues[0] = gamma * sigma**2 + (2 / gamma) * math.log(1 + (gamma / liquidity))
    bidValues = [startPrice - spreadValues[0]/2 for i in range(totalTime+1)]
    askValues = [startPrice + spreadValues[0]/2 for i in range(totalTime+1)]
    price = startPrice

    for i in range(totalTime):
        price += random.gauss(mu, sigma * math.sqrt(1 / totalTime))
        timeRemaining = (totalTime - i - 1) / totalTime     # timeRemaining as a *proportion* of total time left
        reservationPrice = price - inventory * gamma * sigma**2 * timeRemaining     # What the product is worth to us, adjusted by our inventory skew
        spread = gamma * sigma**2 * timeRemaining + (2 / gamma) * math.log(1 + (gamma / liquidity))   # Spread gets tighter, less risk-averse as time goes on
        bid = reservationPrice - spread/2       # Update bid and ask
        ask = reservationPrice + spread/2
        # Update the lists
        priceValues[i+1], resPriceValues[i+1], bidValues[i+1], askValues[i+1], spreadValues[i+1] = price, reservationPrice, bid, ask, spread

        # ask - price is delta^a and price - bid is delta^b in the research paper
        # for either case, the Poisson rate is directly proportional to exp(-k * delta) because traders want to buy or sell close to the mid price
        # at most one of each bid and ask orders may be handled in a single step, but the probability of receiving more is relatively small anyway
        deltaA, deltaB = ask - price, price - bid       # Delta variables as stated in the paper
        if random.random() < (A / totalTime) * math.exp(-liquidity * deltaA):
            buyers += 1
            inventory -= 1
            cash += ask     # Gain cash if selling inventory
        if random.random() < (A / totalTime) * math.exp(-liquidity * deltaB):
            sellers += 1
            inventory += 1
            cash -= bid     # Lose cash if buying inventory
        # Now update PNL
        pnl = cash + inventory * price
        pnlValues[i+1] = pnl
    
    if detailed:
        fig, ax = plt.subplots()    # Plot four lines on the same graph
        ax.plot(priceValues, "black", label="Price", linewidth=1.5)
        ax.plot(resPriceValues, "purple", label="Reservation Price", linewidth=1.5)
        ax.plot(bidValues, "green", label="Bid", linewidth=1.5)
        ax.plot(askValues, "red", label="Ask", linewidth=1.5)
        plt.legend()
        fig, ax = plt.subplots()
        ax.plot(pnlValues, "pink", label="PNL")     # PNL graph on its own
        plt.show()
    return pnl

def monteCarlo(n):
    totalPNL, squareSum = 0, 0
    simulationPNLList = [0 for i in range(n)]
    for i in range(n):
        simulationPNLList[i] = simulation(100, 200, 0, 2, 0.1, 1.5, 140, False)
        totalPNL += simulationPNLList[i]
        squareSum += (simulationPNLList[i])**2
    print("Total PNL: " + str(totalPNL))
    print("Mean PNL: " + str(totalPNL/n))
    print("Sample Variance: " + str((squareSum - totalPNL**2/n) /(n-1)))

simulation(100, 200, 0, 2, 0.1, 1.5, 140, True)
monteCarlo(5000)