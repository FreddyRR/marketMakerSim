import matplotlib.pyplot as plt
import random
import math

def getPrices(startPrice, totalTime, mu, sigma):
    priceValues = [startPrice for i in range(totalTime+1)]
    price = startPrice
    for i in range(totalTime):
        price += random.gauss(mu, sigma * math.sqrt(1 / totalTime))
        priceValues[i+1] = price
    return priceValues

# A mirror of avStrategy.py
def avStrategy(prices, totalTime, sigma, gamma, liquidity, A, detailed):
    price = prices[0]       # Starting values
    inventory, cash, buyers, sellers, pnl = 0, 0, 0, 0, 0
    resPriceValues = [price for i in range(totalTime+1)]
    pnlValues = [0 for i in range(totalTime+1)]
    spreadValues = [0 for i in range(totalTime+1)]
    spreadValues[0] = gamma * sigma**2 + (2 / gamma) * math.log(1 + (gamma / liquidity))
    bidValues = [price - spreadValues[0]/2 for i in range(totalTime+1)]
    askValues = [price + spreadValues[0]/2 for i in range(totalTime+1)]

    for i in range(totalTime):
        price = prices[i+1]
        timeRemaining = (totalTime - i - 1) / totalTime     # timeRemaining as a *proportion* of total time left
        reservationPrice = price - inventory * gamma * sigma**2 * timeRemaining     # What the product is worth to us, adjusted by our inventory skew
        spread = gamma * sigma**2 * timeRemaining + (2 / gamma) * math.log(1 + (gamma / liquidity))   # Spread gets tighter, less risk-averse as time goes on
        bid = reservationPrice - spread/2       # Update bid and ask
        ask = reservationPrice + spread/2
        # Update the lists
        resPriceValues[i+1], bidValues[i+1], askValues[i+1], spreadValues[i+1] = reservationPrice, bid, ask, spread

        # ask - price is delta^a and price - bid is delta^b in the research paper
        # for either case, the Poisson rate is directly proportional to exp(-k * delta) because traders want to buy or sell close to the mid price
        # at most one of each bid and ask orders may be handled in a single step, but the probability of receiving more is relatively small anyway
        deltaA, deltaB = ask - price, price - bid
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
        ax.plot(prices, "black", label="Price", linewidth=1.5)
        ax.plot(resPriceValues, "purple", label="Reservation Price", linewidth=1.5)
        ax.plot(bidValues, "green", label="Bid", linewidth=1.5)
        ax.plot(askValues, "red", label="Ask", linewidth=1.5)
        plt.legend()
        fig, ax = plt.subplots()
        ax.plot(pnlValues, "pink", label="PNL")     # PNL graph on its own
        plt.show()
    return pnl


# A mirror of naiveStrategy2.py
def naiveStrategy(prices, spreadRadius, totalTime, liquidity, A, detailed):
    price = prices[0]       # Starting values
    inventory, cash, buyers, sellers, pnl = 0, 0, 0, 0, 0
    bidValues = [price - spreadRadius for i in range(totalTime+1)]
    askValues = [price + spreadRadius for i in range(totalTime+1)]
    pnlValues = [0 for i in range(totalTime+1)]
    pBuyer = (A / totalTime) * math.exp(-liquidity * spreadRadius)
    pSeller = (A / totalTime) * math.exp(-liquidity * spreadRadius)
    for i in range(totalTime):
        price = prices[i+1]
        bid = price - spreadRadius
        ask = price + spreadRadius
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
        fig, ax = plt.subplots()    # Plot three lines on the same graph
        ax.plot(prices, "black", label="Price", linewidth=1.5)
        ax.plot(bidValues, "green", label="Bid", linewidth=1.5)
        ax.plot(askValues, "red", label="Ask", linewidth=1.5)
        plt.legend()
        fig, ax = plt.subplots()
        ax.plot(pnlValues, "pink", label="PNL")     # PNL graph on its own
        plt.show()
    return pnl

def monteCarlo(n):
    # Start tracking PNL per list of prices for each simulation
    avPNLList = [0 for i in range(n)]
    naivePNLList = [0 for i in range(n)]
    avTotalPNL, avSquareSum, naiveTotalPNL, naiveSquareSum = 0, 0, 0, 0

    for i in range(n):
        prices = getPrices(startPrice, totalTime, mu, sigma)    # A random list of prices used by both simulations
        avPNLList[i] = avStrategy(prices, totalTime, sigma, gamma, liquidity, A, False)
        naivePNLList[i] = naiveStrategy(prices, spreadRadius, totalTime, liquidity, A, False)
        avTotalPNL += avPNLList[i]
        avSquareSum += (avPNLList[i])**2
        naiveTotalPNL += naivePNLList[i]
        naiveSquareSum += (naivePNLList[i])**2

    print("AV Mean PNL: " + str(avTotalPNL / n))     # Output results
    print("AV Sample Variance: " + str((avSquareSum - avTotalPNL**2 / n) / (n-1)))
    print("Naive Mean PNL: " + str(naiveTotalPNL / n))
    print("Naive Sample Variance: " + str((naiveSquareSum - naiveTotalPNL**2 / n) / (n-1)))

# Main program finished, use the below space to perform Monte Carlo simulations or generate graphs

startPrice = float(input("Enter startPrice: "))
totalTime = int(input("Enter totalTime: "))
mu = float(input("Enter mu: "))
sigma = float(input("Enter sigma: "))
gamma = float(input("Enter gamma: "))
liquidity = float(input("Enter liquidity: "))
A = float(input("Enter A: "))
spreadRadius = (1 / gamma) * math.log(1 + (gamma / liquidity))
n = int(input("Enter number of trials: "))
monteCarlo(n)