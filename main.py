import matplotlib.pyplot as plt
from pprint import pprint
from math import ceil
import numpy as np


class Data:
    def __init__(self, dataFileName="data.txt") -> None:
        self.loadFromFile(dataFileName)  # self.data - вариационный ряд
        self.N = len(self.data)
        
    def loadFromFile(self, dataFileName):
        with open(dataFileName, "r") as file:
            self.data = sorted(map(int, file.read().split()))
            
    def getSS(self) -> dict:  # статистический ряд
        res = dict.fromkeys(range(self.data[0], self.data[-1]), 0)
        
        for item in self.data:
            res[item] = res.get(item, 0) + 1
        return res
    
    def getISS(self, delta: int) -> dict:  # интервальный статистический ряд
        def getKey(item) -> tuple:
            return (item-(item-self.data[0])%delta, item-(item-self.data[0])%delta+delta)
        
        res = dict.fromkeys([getKey(item) for item in range(self.data[0], self.data[-1], delta)], 0)
            
        for item in self.data:
            key = getKey(item)
            res[key] = res.get(key, 0) + 1
        return res

    def getM(self) -> float:  # математическое ожидание
        return sum(self.data)/len(self.data)
    
    def getD(self) -> float: # дисперсия
        M = self.getM()
        return sum([(M-val)**2 for val in self.data])/len(self.data)
    
    def drawGistByISS(self, ISS: dict, xLabel=None, yLabel=None, title=None, label=None):
        X, Y = reformingSSToXY(ISS).values()
        
        delta = X[0][1]-X[0][0]
        X = list(map(str, X))
        Y = list(map(lambda item: item/(self.N*delta), Y))
        
        plt.delaxes()
        plt.bar(X, Y)
        plt.xlabel(xLabel)
        plt.ylabel(yLabel)
        plt.title(title)
        plt.legend()
        
        return plt
        
        
def reformingSSToXY(result : dict) -> dict:
        res = {"X": [], "Y": []}
        for x, y in result.items():
            res["X"].append(x)
            res["Y"].append(y)
        return res


def draw(x : list, y : list, fileName : str, xLabel=None, yLabel=None, title=None, label=None) -> None:
        plt.delaxes()
        plt.bar(x, y, label=label)
        plt.xlabel(xLabel)
        plt.ylabel(yLabel)
        plt.title(title)
        plt.legend()
        plt.savefig(fileName)


if __name__ == "__main__":
    data = Data()
    
    # 1
    interval_count = 7
    delta = ceil((data.data[-1] - data.data[0] + 1)/interval_count)
    
    SS = data.getSS()
    ISS = data.getISS(delta)
    pprint(SS)
    pprint(ISS)
        
    # 2
    
    M = data.getM()
    D = data.getD()
    print(f"{M=}")
    print(f"{D=}")
    
    # 3
    
    plt = data.drawGistByISS(
        ISS,
        xLabel="результат измерения, см.",
        yLabel="кол-во участников",
        label="обхват грудной клетки",
        title="Вариант. 5, Результаты измерения обхвата грудной клетки 120 женщин"
        )
    plt.show()
    
    # 4
    
    def normal_dist(x, mean = 2.1, sd=1.5):
        prob_density = (np.pi*sd) * np.exp(-0.5*((x-mean)/sd)**2)
        return prob_density/50
    x = np.linspace(-1,interval_count,70)
    pdf = normal_dist(x)
    plt.plot(x,pdf , color = 'red')
    plt.show()
    
    print("нормальное распределение")