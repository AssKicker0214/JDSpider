# 京东笔记本电脑爬虫

***务必看完***
> 南京大学云计算组队作业，实现京东笔记本电脑评论的爬虫。需要各成员共同爬取。

## 大体过程
1. 已经从笔记本列表页爬取了所有笔记本的`productId`，存入阿里服务器的mongodb
2. 运行程序可以从服务器获取没有被任何人爬取的笔记本，然后在本地爬取，结果存在本地mongodb
3. 爬取完全部数据以后，将结果集导出为`json`，并传给我


## 使用方式
### 环境准备
1. `Python 3` ***[一定是python3.x，不是python2.x]***
2. `Scrapy` 安装完python3以后，安装scrapy
3. `Mongodb 3.X` 在本地开启mongodb以后才能运行程序

### 开始爬取
环境准备完成后需要做以下步骤
1. 更改`JDCommentSpider.py`文件中第29行，将`self.aliyun = AliyunMongo("qhb")`中的`qhb`替换为自己名字的缩写
2. 启动mongodb，`mongod --dbpath [指定一个存放数据的文件夹]`。 如果是第一次，需要建立数据库`jd`，在其下建立集合`comments_part`
3. `JDCommentSpider.py`第36行`product_ids = self.aliyun.get_task()`中，`get_task`可以传入参数：一次爬取多少件商品的评论，默认5. *不要太大，会被封 ip*
4. 运行方式：1. 在项目根目录，在命令行输入`scrapy crawl jd-comment`，运行程序; 2. 运行driver文件，可以在该文件末尾修改爬取时间间隔

### 备注
- 可以自行去阿里云查询当前大家整体爬取的结果。地址为101.132.40.25，端口号27072。连接命令`mongo --host 101.132.40.25 --port 27072`。***看看就好了，不要改数据……***
