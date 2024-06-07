import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from pulp import LpProblem, LpVariable, lpSum, LpMinimize, value

# 行政区域和行车时间数据
districts = ['1', '2', '3', '4', '5', '6', '7', '8']
drive_times = [
    [0, 10, 11, 13, 15, 16, 10, 17],
    [10, 0, 12, 14, 15, 13, 19, 16],
    [11, 12, 0, 9, 9, 10, 14, 12],
    [13, 14, 9, 0, 10, 9, 12, 11],
    [15, 15, 9, 10, 0, 10, 16, 18],
    [16, 13, 10, 9, 10, 0, 12, 9],
    [10, 19, 14, 12, 16, 12, 0, 14],
    [17, 16, 12, 11, 18, 9, 14, 0]
]

# 创建线性规划问题
prob = LpProblem("Ambulance_Center", LpMinimize)

# 创建变量，表示是否在每个区建立救护中心
centers = LpVariable.dicts("Center", districts, cat='Binary')

# 创建变量，表示每个区域被覆盖的情况
cover = LpVariable.dicts("Cover", (districts, districts), cat='Binary')

# 目标函数：最小化建立的救护中心数量
prob += lpSum([centers[i] for i in districts])

#将时间矩阵转换成覆盖矩阵
for i in range(len(districts)):
    for j in range(len(districts)):
        if drive_times[i][j] <= 10:
            cover[districts[i],districts[j]] = 1
        else:
            cover[districts[i],districts[j]] = 0

# 约束条件：每个区到最近的救护中心的行车时间都不超过10分钟且确保存在一个
for i in range(len(districts)):
    prob += lpSum([centers[districts[j]]*cover[districts[i],districts[j]]  for j in range(len(districts))]) >= 1

# 解决问题
prob.solve()

# 输出结果
print("建立的救护中心数量:", int(value(prob.objective)))
print("救护中心位置:")
center_nodes = []
for i in districts:
    if centers[i].varValue == 1:
        print("在区域", i)
        center_nodes.append(i)


# 找到每个区域最近的救护中心
closest_center = {}
for i in range(len(districts)):
    min_time = float('inf')
    for center in center_nodes:
        j = districts.index(center)
        if drive_times[i][j] < min_time:
            min_time = drive_times[i][j]
            closest_center[districts[i]] = center

# 绘制图
G = nx.Graph()

# 添加节点
for district in districts:
    G.add_node(district)

# 生成布局
pos = nx.spring_layout(G, seed=42)

# 绘制节点
nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=16, font_weight='bold')

# 高亮救护中心
nx.draw_networkx_nodes(G, pos, nodelist=center_nodes, node_color='red', node_size=2500)

# 绘制10分钟为半径的圆
for center in center_nodes:
    circle = plt.Circle(pos[center], 0.1, color='red', fill=False, linestyle='--', linewidth=2)
    plt.gca().add_patch(circle)

# 添加每个区域到最近救护中心的边和标签
for district in districts:
    if district != closest_center[district]:
        G.add_edge(district, closest_center[district])
        edge_labels = {(district, closest_center[district]): drive_times[districts.index(district)][districts.index(closest_center[district])]}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=12)
        
nx.draw_networkx_edges(G, pos, edgelist=G.edges, width=2, alpha=0.5, edge_color='gray')

plt.title('每一个区域到达最近救护中心的图 (线的长度用时间表示)')
plt.gca().set_aspect('equal', adjustable='box')
plt.show()