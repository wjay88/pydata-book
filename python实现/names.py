import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# import pylab as pl


####################################
#       S1：第一步：加载数据        #
####################################
####################################
#       S2:第二步：数据预处理       #
####################################
# 由于数据集通过年份year被分割成了多个文件，所以第一步所有数据组装到一个DataFrame中。
# 由于是根据年分割，所以加上year字段。查看原始数据。了解情况。
years = range(1880, 2011)

pieces = []
columns = ['name', 'sex', 'births']

for year in years:
    path = "../datasets/babynames/yob%d.txt" % year
    frame = pd.read_csv(path, names=columns)

    frame['year'] = year
    pieces.append(frame)


####################################
#    S3:第三步：数据转换合成大表    #
####################################
# 将所有数据整合到一个DataFrame中
names = pd.concat(pieces, ignore_index=True)
# concat默认按行将多个DataFrame组合到一起
# 指定ignore_index = True不保留read_csv返回的原始行号。

# print(names)

####################################
#      S4:第四步：数据建模计算      #
####################################

# 数据聚合，year和sex聚合。
total_births = names.pivot_table('births', index='year', columns='sex', aggfunc=sum)
# print(total_births.tail())


####################################
#      S5:第五步：数据结果展示      #
####################################

total_births.plot(title='Total Birth by sex and year')
# plt.show()
# 原书中代码不显示图：
# 此时增加import matplotlib.pylot as plt
# 和plt.show()

def add_prop(group):
    # 整数除法会向下圆整
    births = group.births.astype(float)

    group['prop'] = births / births.sum()
    return group

# 按照年龄和性别分组。统计比例。
names = names.groupby(['year', 'sex']).apply(add_prop)

# print(names)
# print(names[names.year == 2010][names.sex == 'M'].prop.sum())

# 分组处理后：有效性检查：检验prop总和为1。由于浮点型，所以用np.allclose来检查总计值是否足够近似1.
np.allclose(names.groupby(['year', 'sex']).prop.sum(), 1)

# 取出每对sex/year组合的前1000个名字。

# def get_top1000(group):
#     return group.sort_index(by='births', ascending=False)[:1000]
#
# group = names.groupby(['year', 'sex'])
# top1000 = group.apply(get_top1000)

# 或者这样写：
pieces1 = []
for year, group in names.groupby(['year', 'sex']):
    pieces1.append(group.sort_index(by='births', ascending=False)[:1000])
top1000 = pd.concat(pieces1, ignore_index=True)
# print(top1000)

boys = top1000[top1000.sex == 'M']
girls = top1000[top1000.sex == 'F']

# 按year和name统计总出生数透视表
total_births1 = top1000.pivot_table('births', index='year', columns='name', aggfunc=sum)
# print(total_births1)


# 绘制几个名字的曲线图。
subset = total_births1[['John', 'Harry', 'Mary', 'Marilyn']]
subset.plot(subplots=True, figsize=(12, 10), grid=False, title='Number of births per year')
# plt.show()

# 计算最流行的1000个名字所占比例。按year和sex聚合并绘图。

table = top1000.pivot_table('prop', index='year', columns='sex', aggfunc=sum)
table.plot(title='Sum of table1000.prop by year and sex', yticks=np.linspace(0, 1.2, 13), xticks=range(1880, 2020, 10))
# plt.show()

df = boys[boys.year == 2010]  # 第68行计算基于此处表达方式。
# print(df)
# print(df.prop.sum())

# 想知道多少名字的人数加起来才够50%。
# NumPy有一种非常聪明的矢量方式：计算prop的累加和cumsum。然后通过searchsorted方式找出0.5应该被插入而不破坏顺序的位置。

prop_cumsum = df.sort_index(by='prop', ascending=False).prop.cumsum()
# print(prop_cumsum[:10])

# print(prop_cumsum.searchsorted(0.5))   #由于索引是从0开始的，因此我们给这个结果加1.即最终结果为117。

df = boys[boys.year == 1900]
in1900 = df.sort_index(by='prop', ascending=False).prop.cumsum()
# print(in1900.searchsorted(0.5) + 1)


def get_quantile_count(group, q=0.5):
    group = group.sort_index(by='prop', ascending=False)
    return group.prop.cumsum().searchsorted(q) + 1

diversity = top1000.groupby(['year', 'sex']).apply(get_quantile_count)
# print(diversity)
# print('-'*30 + "华丽的分割线" + '-'*30)
diversity = diversity.unstack('sex')
# print(diversity)
# print('-'*30 + "华丽的分割线" + '-'*30)
# unstack和stack(堆砌，堆积，堆叠)函数的使用：
# stack从“表格结构”变成“花括号结构”，将行索引变成列索引。

# print(diversity.head())

diversity.plot(title="Number of popular names in top 50%")
plt.show()
# print(diversity)



