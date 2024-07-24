## 课设  
基于scrapy写的一个爬虫  
从一个天气网站上爬取天气数据然后使用flask网页进行展示  
一些简单的制表操作  
~以东京为例子，需要其他城市可以自行修改网址~  
已经爬取了该网站的所有日本城市）
不过要注意，只能是日本的城市  
在chrome开发者中自动转译了一些字符  
重新打印之后才发现需要匹配日本汉字（这里也导致我调试了很久）  
使用flask简单展示了几张折线图和一个描述的表格  
基本算是完成任务  

### 流程  
先运行weather_scraper/spiders中的db_init.py  
这里会创建一个数据库：weather_data.db  
注意这里数据库创建在根目录下，需要将其移动到spiders下  
（忘改创建路径了，反正知道就行）  
然后在weather_scraper中运行脚本
```python
 .\.venv\Scripts\activate//激活虚拟环境
scrapy crawl accuweather//启动爬虫
```
这里会将网站上的信息导入数据库中  
接下来运行data_clean中的clean.py  
数据库中的数据会被转化成csv文件并清洗  
最后运行run.py,进入http://127.0.0.1:5000/ 就行了  
