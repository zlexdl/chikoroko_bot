import traceback

import requests
from bs4 import BeautifulSoup
import time
from util import get_random_useragent

import tweepy


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, BigInteger, Integer, String, Text, DateTime, ForeignKey, Float
from sqlalchemy.orm import sessionmaker
from util import send_pushplus




engine = create_engine('mysql+pymysql://root:123456@127.0.0.1:3306/discord_bots?charset=utf8mb4')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

auth = tweepy.OAuthHandler('consumer_key',
                            'consumer_secret')
auth.set_access_token('key',
                      'secret')

api = tweepy.API(auth)




class Chikoroko(Base):
    __tablename__ = "chikoroko"  # 数据库中保存的表名字

    id = Column(Integer, index=True, primary_key=True)
    name = Column(String(200), nullable=True)



while True:
    url = 'https://expo.chikoroko.art/'
    key = "Collect now for free"
    tomorrow = "Come tomorrow to collect"
    try:

        res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'})


        soup = BeautifulSoup(res.text, 'html.parser')
        for mobile in soup.find_all('span', class_='mobile-toy-info'):
            span = mobile.find('span', class_='info-content')
            title = span.find('span', class_='text-wrapper h2').text
            print("title: {}".format(title))
            session.commit()
            if session.query(Chikoroko).filter(Chikoroko.name == title).count() == 0:
                if str(mobile).find(tomorrow) > 0:
                    print("tomorrow:{}".format(tomorrow))
                    continue

                if str(mobile).find(key) > 0:
                    print("发现新的了")
                    message = "大家好!我是机器人.\n\n世博会新NFT:\n\n {} 出现了!\n\n 快去领取吧!\n\n {}".format(title, "https://expo.chikoroko.art/referral/x28kalbqlq") + \
                    "\n\n如果你还没有交易所账号, 请点击以下链接进行注册.已经有的请联系我.\n\nOkex: https://www.ouyicn.kim/join/1897781\n\n" \
                    "币安: https://accounts.binance.com/zh-CN/register?ref=10251511"


                    print("message: {}".format(message))
                    re = api.update_status(message)
                    print("转推结果：" + str(re.id_str))
                    try:
                        send_pushplus('世博会新NFT报警', message, 'TW001')
                        send_pushplus('世博会新NFT报警', message, '002')
                    except Exception as e:
                        traceback.print_exc()
                        print("微信推送失败")

                    entry = Chikoroko(
                        name=title)

                    session.add(entry)
                    session.commit()

                else:
                    print("没有发现")



    except Exception as e:
        traceback.print_exc()
        session.rollback()
        print("sleep 30s")
        time.sleep(30)
        continue
    print("sleep 30s")
    time.sleep(30)