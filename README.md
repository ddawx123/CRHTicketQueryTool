# 12306余票监控后台服务
## China Railway Ticket Query Tool

## 安装方法

```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
```

## 使用方法

```bash
python 12306.py [出发站点名] [终到站点名] [乘车时间] [车次编号]
```

## 使用示例

```bash
#查询2019年1月5日绍兴北站到杭州东站的所有列车票务信息
python 12306.py 绍兴北 杭州东 2019-01-05

#查询2019年1月12日杭州东站到深圳北站且车次编号为D3111的票务信息
python 12306.py 杭州东 深圳北 2019-01-12 D3111

#交互式运行（不传入任何参数将启动交互式查询模式，需手动输入）
python 12306.py
```

## 注意事项
```python
import requests
import ssl
# More code ...
```
如上所示，本脚本使用了requests和ssl库。而python3默认并没有自带该库，因此请务必在运行脚本前安装相关依赖。详细操作见“安装方法”！

## 更多辅助
建议将此程序与linux系统的crontab或windows系统的schedule task配合使用，并通过类似短信（SMS）服务、邮箱、微信推送等及时通知用户抢票的监控信息！

### Copyright 2012-2019 DingStudio Technology All Rights Reserved
