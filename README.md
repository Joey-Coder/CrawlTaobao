## 淘宝爬虫   
### 介绍  
* 一个淘宝爬虫的雏形。    
* 基于selenium，取消图片加载，消除webdrive指纹。   
### 使用   
1,在taobao_cookie中写入cookie值，保存。cookie格式为       
```python
[{key1:values1,...},{key1:value1,...}]
```   
推荐一个Chrome插件:[EditThisCookie](https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg?hl=zh-CN)    
该插件可以在你登陆淘宝后将cookie导出，导出的cookie值需要将cookie里面的true和false修改为对应的python的关键字True,Fasle。
* 在setting中设置需要爬取的页数PAGE和cookie的路径COOKIE_PATH   
* 运行爬取命令：   
```python
cd CrawlTaobao/crawltapbao   
python3 browsercrawl.py
```   
爬取过程在终端输入你要爬取的商品信息，回车即可。   

### 待完成
* 添加爬取信息，包括title，商家，销量等
* 实现自动登陆功能
* 验证码自动处理功能


