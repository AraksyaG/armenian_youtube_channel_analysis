
# Download YouTube channel Feeds
# Last run: 2025-06-28

import requests
from datetime import datetime
from bs4 import BeautifulSoup
import json
from xml.etree import ElementTree
import re


# current date and time
now = datetime.now()
timestamp = datetime.timestamp(now) # 1751237132.123456
date = datetime.today().isoformat() # 2025-06-30T12:45

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'
}
Armenian_YouTube_Channels = {"CivilNet":"https://www.youtube.com/feeds/videos.xml?channel_id=UCxPJyX0oQWmqZ5akbuN5DTg",
                             "Armenian_News_Radio_FM_106.5":"https://www.youtube.com/feeds/videos.xml?channel_id=UCaJCNkhSa84QcuOSoM2WfcA",
                             "Sputnik_Armenia":"https://www.youtube.com/feeds/videos.xml?channel_id=UCUmFQ5MCeNAQacrcmswznMg",
                             "Novosti_Armenia":"https://www.youtube.com/feeds/videos.xml?channel_id=UCD6gGqwiP_zdW-sOL8-BBnw",
                             "MediaMax_Red_Thread":"https://www.youtube.com/feeds/videos.xml?channel_id=UCjXOU0n243ioE1P2oGWIC3w",
                             "News_AM":"https://www.youtube.com/feeds/videos.xml?channel_id=UCDv-XtfgNGHXcpwu4ab0WnA",
                             "Grey_Zone":"https://www.youtube.com/feeds/videos.xml?channel_id=UCG9fK8CsL8u4NbBtcofd8lQ",
                             "VOMA":"https://www.youtube.com/feeds/videos.xml?channel_id=UCDtZm9GdMGe_Dt3C5n-1UXw",
                             "Article_3_Club":"https://www.youtube.com/feeds/videos.xml?channel_id=UCFlFXHs6PGIs28RZsdGcJFw",
                             "IDeA_Foundation_Yerevan":"https://www.youtube.com/feeds/videos.xml?channel_id=UCHY0FwP_cZqjT0mYvb_JSGA",
                             "RusArm_Info":"https://www.youtube.com/feeds/videos.xml?channel_id=UC-0e2T58K9GUM1Fbf9Qrg_g",
                             "SHANT_TV":"https://www.youtube.com/feeds/videos.xml?channel_id=UCBoGmjONeZ6PL5IbK6qZv0Q",
                             "Army_Life":"https://www.youtube.com/feeds/videos.xml?channel_id=UCLNYK33KbPFfC3-4hD736bQ",
                             "Armenian_National_Network":"https://www.youtube.com/feeds/videos.xml?channel_id=UCbe0S5mznRiPdNFd9dtwxJA",
                             "1in_TV_Armenia":"https://www.youtube.com/feeds/videos.xml?channel_id=UCcku2B0bzJi6H5gxspIuchw",
                             "Armenian_Public_TV":"https://www.youtube.com/feeds/videos.xml?channel_id=UCSnr4wFDHDZZMeeHQvaHpjA",
                             "24TV":"https://www.youtube.com/feeds/videos.xml?channel_id=UCsRKb5x9Rem0UW-pjl_7Bog",
                             "Arm_Public_TV":"https://www.youtube.com/feeds/videos.xml?channel_id=UCqi9r70a6DuOrXnOra4VLQQ",
                             "Factor_TV":"https://www.youtube.com/feeds/videos.xml?channel_id=UCkI5KAJDh9S-BQFc6QzSUiA",
                             "Batc_TV":"https://www.youtube.com/feeds/videos.xml?channel_id=UCf2o81mWr-bZsLbq2-kOYTQ",
                             "Arm_Daily_News_TV":"https://www.youtube.com/feeds/videos.xml?channel_id=UC8k_9xHrn82EV_oSFXBE6Cw",
                             "Arm_News_TV":"https://www.youtube.com/feeds/videos.xml?channel_id=UC8HwfxKgBPeTrwbWNmowzgQ",
                             "Noyan_Tapan_TV":"https://www.youtube.com/feeds/videos.xml?channel_id=UCCAQbNU87xy-ykE98-PdVVg",
                             "Shoghakat_TV":"https://www.youtube.com/feeds/videos.xml?channel_id=UCpDmKr8LFapW_-45tEW5tmg",
                             "infocom. am": "https://www.youtube.com/feeds/videos.xml?channel_id=UC5XszYyC_a09pXFoqlkRznQ"
                             }

xmlElements=[]

for i,j in Armenian_YouTube_Channels.items():
    file_name = i+"_"+str(date[0:10])+"_"+str(timestamp)+".xml"
    URL_Link = j
    response = requests.get(URL_Link, headers=headers)
    open("C:/Users/User/Desktop/youtube_channel_analysis/XML_Files/" + file_name, 'wb').write(response.content)

    print("Feed file download complete: ", file_name)

