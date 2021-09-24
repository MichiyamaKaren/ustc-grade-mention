在中科大教务系统上自动查询成绩并发邮件通知

**目前不可用，登录模块需要添加验证码识别**

## 如何使用

安装依赖：
```
pip install -r requirements.txt
```

在QQ邮箱上开启POP3/SMTP服务（见[QQ邮箱官方教程](https://service.mail.qq.com/cgi-bin/help?subtype=1&no=166&id=28)），记下SMTP授权码。

修改`config.py`，填写对应项。然后运行`main.py`即可。

如果需要修改查询频率，请查阅`APScheduler`的文档，修改`main.py`第26行的参数。请注意不要讲查询频率设置的过于频繁（这也是不必要的），避免给服务器带来过大流量负担。
