import matplotlib.pyplot as plt


class Data:
    def __init__(self, dataFileName="data.txt") -> None:
        self.loadFromFile(dataFileName)
        
    def loadFromFile(self, dataFileName):
        with open(dataFileName, "r") as file:
            self.data = list(map(int, file.read().split()))
            
    def getSS(self, showNoneData = True) -> dict:  # статистический ряд
        res = dict()
        
        if showNoneData:
            res = dict.fromkeys(range(min(self.data), max(self.data)), 0)
        
        for item in self.data:
            res[item] = res.get(item, 0) + 1
        return res
    
    def getISS(self, interval: int, showNoneData = True) -> dict:  # интервальный статистический ряд
        def getKey(item) -> tuple:
            return (item-item%interval, item-item%interval+interval)
        
        res = dict()
        if showNoneData:
            res = dict.fromkeys([getKey(item) for item in range(min(self.data), max(self.data), interval)], 0)
            
        for item in self.data:
            key = getKey(item)
            res[key] = res.get(key, 0) + 1
        return res

    def getM(self) -> float:  # математическое ожидание
        return sum(self.data)/len(self.data)
    
    def getD(self) -> float: # дисперсия
        M = self.getM()
        return sum([(M-val)**2 for val in self.data])/len(self.data)
        
def reformingResultToXY(result : dict) -> dict:
        res = {"x": [], "y": []}
        for x, y in result.items():
            res["x"].append(str(x))
            res["y"].append(y)
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
    interval = 5
    # 1
    print(SS:=data.getSS())
    print(ISS:=data.getISS(interval))
    # 2
    print(f"математическое ожидание - {data.getM()}")
    print(f"дисперсия - {data.getD()}")
    # 3
    draw(
        **reformingResultToXY(SS),
        fileName="gist.png",
        xLabel="результат измерения, см.",
        yLabel="кол-во участников",
        label="обхват грудной клетки",
        title="В. 5, Результаты измерения обхвата грудной клетки 120 женщин"
        )
    
    draw(
        **reformingResultToXY(ISS),
        fileName="interval_gist.png",
        xLabel="результат измерения, см.",
        yLabel="кол-во участников",
        label="обхват грудной клетки",
        title="В. 5, Результаты измерения обхвата грудной клетки 120 женщин"
        )
    # 4
    print("нормальное распределение")