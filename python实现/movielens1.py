import pandas as pd
# import os

###################################
#       S1：第一步：加载数据      #
###################################
f = open("../datasets/movielens/ratings.csv", 'r+')
rnames = ['userId', 'movieId', 'rating', 'timestamp']
ratings = pd.read_csv(f, sep=',', engine='python')
# 课本上是pd.read_table(f, sep = '::', header =None, names = rnames)
# 读取的是.dat文件。而现在下载的数据是.csv
# 故分割符号是用“，”
# print(ratings[:5])
# print(ratings)

lnames = ['movieId', 'imdbId', 'tmdbId']
links = pd.read_csv("ml-latest-small/links.csv", sep=",")
# print(links)

mnames = ['movieId', 'title', 'genres']
movies = pd.read_csv("ml-latest-small/movies.csv", sep=",")
# print(movies)

tnames = ['userId', 'movieId', 'tag', 'timestamp']
tags = pd.read_csv("ml-latest-small/tags.csv", sep=",")
# print(tags)

###################################
#       S2:第二步：数据预处理     #
###################################

# 合并根据列名称来合并数据
merge_userid = pd.merge(ratings, tags)
merge_movieid = pd.merge(links, movies)
merge_data = pd.merge(pd.merge(links, movies), tags)
s = merge_data.stack()  # 行列转换。
# print(merge_data[:5])
# print(s[:16:])

# 此处pivot函数应用待学习。数据变换转换。
# mean_ratings = s.pivot("ratings", index="movieId", columns="rating", aggfunc="mean")
# print(mean_ratings[:5])
# 从github上下载源书数据。重新开始。



