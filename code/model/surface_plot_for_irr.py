import numpy as np
import matplotlib.pyplot as plt
from code.model.inner_return_rate_cal import irr_cal


# 设置市场参数
S = 1
# H = 3
# L = 0.4
C = 0.2
r = 0.05
mu = 0
sigma = 0.7

# 创建网格点
# sample_number用来规定x轴,y轴的参数点，为了方便用一个变量控制了，比如这里的20表明将会有20*20个参数点
sample_number = 20
L_list = np.linspace(0.01, 0.93, sample_number)
H_list = np.linspace(1.05, 5, sample_number)
irr_value = np.zeros((sample_number, sample_number))
# 循环，每个点单独计算然后放进irr_value里
# for L in L_list:
#     for H in H_list:
#         try:
#             result_value = irr_cal_version_2(1, L, H, sigma, C, r, mu)
#             L_index = np.where(L_list == L)[0][0]
#             H_index = np.where(H_list == H)[0][0]
#             irr_value[L_index][H_index] = result_value
#         except:
#             print(L, H)
#             pass
for L in L_list:
    for H in H_list:
        result_value = irr_cal(1, L, H, sigma, C, r, mu)
        L_index = np.where(L_list == L)[0][0]
        H_index = np.where(H_list == H)[0][0]
        irr_value[L_index][H_index] = result_value
# L, H坐标话
L_axis, H_axis = np.meshgrid(L_list, H_list)

# 创建图形对象
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# 绘制曲面
surf = ax.plot_surface(L_axis, H_axis, irr_value, cmap='viridis')  # 使用颜色图 viridis

# 添加颜色条
fig.colorbar(surf)

# 设置轴标签
ax.set_xlabel('L axis')
ax.set_ylabel('H axis')
ax.set_zlabel('irr value axis')

# 显示图形
plt.show()

# 这套代码已经成功
