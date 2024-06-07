import nashpy as nash
import numpy as np

# 定义收益矩阵
# 使用 -1e9 表示无限大的负值
A_payoff_matrix = np.array([
    [-3000, 10000],
    [-1e9, 0]
])

B_payoff_matrix = np.array([
    [-3000, -1e9],
    [10000, 0]
])

# 创建博弈
game = nash.Game(A_payoff_matrix, B_payoff_matrix)

# 求解纳什均衡
equilibria = list(game.support_enumeration())

# 打印结果
for eq in equilibria:
    A_strategy, B_strategy = eq
    A_value = np.sum(A_strategy[:, None] * B_strategy[None, :] * A_payoff_matrix)
    B_value = np.sum(A_strategy[:, None] * B_strategy[None, :] * B_payoff_matrix)
    print("国家X的策略：[扩军概率，裁军概率]，收益：xx")
    print(f"国家A的策略: {A_strategy}, 收益: {A_value}")
    print(f"国家B的策略: {B_strategy}, 收益: {B_value}")
