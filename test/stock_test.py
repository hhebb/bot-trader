from Application.Analyzer import AnalyzerWorker
from Core.TechnicalAnalysis import *

an = AnalyzerWorker()
an.Simulate()
res = an.GetResult()
ticker = res[3]

print(ticker.GetTickChart())
candle = ticker.GetTickChart()
vol = ticker.GetVolumeChart()

ta = TechnicalAnalyzer(tickData=candle, volData=vol)
ta.MakeDataframe()