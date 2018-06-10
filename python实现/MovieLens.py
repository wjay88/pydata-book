import pandas as pd
import os


####################################
#       S1：第一步：加载数据        #
####################################
f1 = open("../datasets/movielens/users.dat", 'r+')
unames = ['user_id', 'gender', 'age', 'occupation', 'zip']
users = pd.read_table(f1, sep="::", header=None, names=unames, engine='python')

f2 = open("../datasets/movielens/ratings.dat", 'r+')
rnames = ['user_id', 'movie_id', 'rating', 'timestamp']
ratings = pd.read_table(f2, sep="::", header=None, names=rnames, engine='python')

f3 = open("../datasets/movielens/movies.dat", 'r+', errors='ignore')
# f3 = open("pydata/ch02/movielens/movies.dat", 'r+', encoding='gb18030', errors='ignore')
mnames = ['movie_id', 'title', 'genres']
movies = pd.read_table(f3, sep="::", header=None, names=mnames, engine='python')
# https://blog.csdn.net/shijing_0214/article/details/51971734
# movies文件因为含有特殊符号，所以增加多个参数配置。

# print(users[:5])
# print("-"*50)
# print(ratings[:5])
# print("-"*50)
# print(movies[:5])
# print("-"*50)

# print(ratings.stack())

####################################
#       S2:第二步：数据预处理       #
####################################

# 想要根据性别和年龄计算某部电影的平均得分。
# 将所有数据都合并到一个表中，合并或连接
data = pd.merge(pd.merge(ratings, users), movies)
# print(data)
# print(data.ix[0])

####################################
# S3:第三步：数据转换、产生新数据集 #
####################################

# 想要根据性别和年龄计算某部电影的平均得分。
mean_ratings = data.pivot_table('rating', index='title', columns='gender', aggfunc='mean')
# print(mean_ratings[:5])
# 产生新的DataFrame。

# 先对title进行分组，利用size（）得到分组对象。
ratings_by_title = data.groupby('title').size()
# print(ratings_by_title[:10])
active_titles = ratings_by_title.index[ratings_by_title >= 250]
# print(active_titles)
# 从前面的mean_ratings中选取。
mean_ratings = mean_ratings.ix[active_titles]
# print(mean_ratings)

# 为了解女性观众最喜欢的电影，对F列降序排列：
top_female_ratings = mean_ratings.sort_index(by='F', ascending=False)
# print(top_female_ratings[:10])

# 寻找男女分歧最大的电影
# 方法：给mean_ratings加上一个用于存放平均得分之差的列，并对其进行排序。
mean_ratings['diff'] = mean_ratings['M'] - mean_ratings['F']
sorted_by_diff = mean_ratings.sort_index(by='diff')

# 分歧大且更受女性喜欢的电影：
print(sorted_by_diff[:15])
print("$"*60)
# 分歧大反序取出前15行：男性更喜欢的电影。
print(sorted_by_diff[::-1][:15])
print("￥"*60)
# 不考虑性别：只考虑分歧最大的电影：方差或标准差。
rating_std_by_title = data.groupby('title')['rating'].std()  # 标准差

# 根据 active_titles 进行过滤
rating_std_by_title = rating_std_by_title.ix[active_titles]

# 根据值对Series进行降序排列
# print(rating_std_by_title.order(ascending=False)[:10])
print(rating_std_by_title.sort_values(ascending=False)[:10])
print("￥"*60)



