from Application.Analyzer import AnalyzerWorker

an = AnalyzerWorker()
an.Simulate()
res = an.GetResult()
print(res)