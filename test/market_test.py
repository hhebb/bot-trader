from Core import Market
from Application import Runner

'''
마켓 데이터 시뮬레이션 테스트.
시뮬레이션에 필요한 데이터가 문제없이 스트리밍 되는지 확인.
'''

if __name__ == '__main__':
    runner = Runner.Runner()
    runner.Simulate()