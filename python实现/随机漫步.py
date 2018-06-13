# 从零开始，步长1和-1出现的概率相等。

import sys
import random
import numpy as np

print('Python %s on %s' % (sys.version, sys.platform))
position = 0
walk = [position]
steps = 1000
for i in np.arange(steps):
    step = 1 if random.randint(0, 1) else -1
    position += step
    walk.append(position)

nsteps = 1000
draws = np.random.randint(0, 2, size=nsteps)
steps = np.where(draws > 0, 1, -1)
walk = steps.cumsum()
print("最小值：%d" % walk.min())
print("最大值：%d" % walk.max())
print("首次穿越时间：%d" % (np.abs(walk) >= 10).argmax())




