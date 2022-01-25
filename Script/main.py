# Major module
from datetime import datetime, timedelta, timezone
from logging import getLogger
from time import sleep
import pandas as pd
from tqdm import tqdm # pip3 install tqdm
import gc
import json
import os

# Selenium: pip3 install selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# Self-made module
import log

PRODUCTION = True
PARENT_DIR = './Web/'

HTML_DIR = PARENT_DIR + 'pages/'

if PRODUCTION == False:    
    DELAY = 0

else:
    DELAY = 0.1 #ループのディレイ。ラズパイでは処理能力不足のためリソース開放しないとWeb側の処理ができない。

READ_DATA_FLAG = True
CYCLE = 1 # 1 cycle 15 days

PST = timezone(timedelta(hours=-8))


### Log ###
LOG_DIR = './Script/Log/'
logger = getLogger(__name__)
log.set_log_config(logger, LOG_DIR, 'get_site_availability.log')

class RecreationGov:

    def __init__(self, name, url):
        
        self.site_name = name
        self.address = url

        # Headless Chromeをあらゆる環境で起動させるオプション
        options = Options()
        if PRODUCTION == True:
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-extensions')
            options.add_argument('--proxy-server="direct://"')
            options.add_argument('--proxy-bypass-list=*')
            options.add_argument('--start-maximized')
            options.add_argument('--headless')

            self.driver = webdriver.Chrome(options=options)
            self.driver.implicitly_wait(10) #sec

        else:
            #options.add_argument('--headless')

            self.driver = webdriver.Chrome(options=options)
            self.driver.set_window_size(800,1000)
            self.driver.set_window_position(0,0)
            self.driver.implicitly_wait(10) #sec

    def get_reservation(self):

        try:
            # Open web page
            logger.info(f'Open: {self.address}')
            self.driver.get(self.address)
            sleep(1)

            # 毎回Popupが表示されるページあり -> Popupのクローズボタンがある場合はクリックして閉じる
            # idが無いのでXPathを使用
            # body > div:nth-child(14) > div > div > div > div > div > div > div > button
            # <button data-component="Button" type="button" class="sarsa-button sarsa-modal-close-button sarsa-button-subtle sarsa-button-md" aria-label="Close modal"><span class="sarsa-button-inner-wrapper"><span aria-hidden="true" class="sarsa-button-icon-content left-icon is-only-child"><svg data-component="Icon" class="sarsa-icon rec-icon-close" viewBox="0 0 24 24" role="presentation" focusable="false" height="24" width="24"><g><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"></path></g></svg></span><span class="sarsa-button-content"></span></span></button>
            # /html/body/div[10]/div/div/div/div/div/div/div/button
            #xpath = '/html/body/div[9]/div/div/div/div/div/div/div/button'
            xpath = '/html/body/div[10]/div/div/div/div/div/div/div/button'
            self.__close_popup_by_xpath(xpath)


            # 適当なid取ってPAGE_DOWNキーを投げる
            # 別にスクロールする必要はないけど、テーブル見えないとやってる感が無い
            id="campsite-filter-search"
            self.__send_key_by_id(id, Keys.PAGE_DOWN)

            # 取り出した情報格納用リスト
            availability_list = [] #[[Date][Status][1]]

            start = 0
            #CYCLE = 1
            for i in range(start,CYCLE):

                # 初回だけ飛ばす
                if i > start:
                    # 15日分のデータが一回で取得可能なため5daysボタン3回クリック

                    sleep(1)
                    #id="campsite-filter-search"
                    #self.__click_by_id(id)

                    xpath = '//*[@id="rec-campground-availability-title"]/div/div[2]/div/button[3]'
                    self.__click_by_xpath(xpath)
                    sleep(1)
                    self.__click_by_xpath(xpath)
                    sleep(1)
                    self.__click_by_xpath(xpath)
                    sleep(2)

                # テーブルのボタン内に空き情報が埋め込まれているのでそれを取得
                # テーブルのクラス名から全要素取得
                cls = "rec-availability-date"
                elms = self.driver.find_elements_by_class_name(cls)
                logger.debug(f'rec-availability-date 要素数: {len(elms)}')


                # 取得した全要素を1個ずつ確認
                for elm in tqdm(elms):

                    # aria-label内に埋め込まれている情報を取得
                    text = elm.get_attribute('aria-label')
                    # 埋まってる情報
                    # Oct 25, 2021 - Site 085 is available
                    # Oct 31, 2021 - Not Available
                    # Nov 7, 2021 - Not Available
                    #logger.debug(text)

                    # 結果を分解してリストに格納 [[Datetime][Status][1]] 1はpivotのカウント用
                    rtn_list = self.__get_dt_and_status(text)
                    availability_list.append(rtn_list)

                    del text
                    del rtn_list
                    gc.collect()
                    sleep(DELAY)

                logger.debug(f'availability len: {len(availability_list)}')

            # 二次元リストをDataFrame化
            df = pd.DataFrame(availability_list, columns=['Datetime','Status','Count'])
            #logger.debug(df)

            # 項目をカウント
            df_pivot = pd.pivot_table(df, index='Datetime', columns='Status', values='Count', aggfunc='count', fill_value=0)
            #logger.debug(df_pivot)

            # 1個も空いてないときに0を追加
            if 'Available' in df_pivot.columns:
                pass
            else:
                df_pivot['Available'] = 0

            return df_pivot


        except Exception as e:
            logger.exception(e)

        finally:
            self.driver.close()

    ### Private method ###

    def __send_key_by_id(self, id, text):
        
        try:
            elm = self.driver.find_element_by_id(id)
            logger.debug(elm)
            elm.send_keys(text)
            sleep(0.1)

        except Exception as e:
            logger.exception(e)

    def __click_by_id(self, id):
        
        try:
            elm = self.driver.find_element_by_id(id)
            logger.debug(elm)
            elm.click()
            sleep(1)

        except Exception as e:
            logger.exception(e)

    def __click_by_xpath(self, xpath):
        
        try:
            elm = self.driver.find_element_by_xpath(xpath)
            logger.debug(elm)
            elm.click()
            sleep(1)

        except Exception as e:
            logger.exception(e)

    def __close_popup_by_xpath(self, xpath):

        try:
            if self.driver.find_element_by_xpath(xpath).is_displayed():
                elm = self.driver.find_element_by_xpath(xpath)
                logger.debug(elm)
                self.__click_by_xpath(xpath)

        except Exception as e:
            logger.exception(e)

    def __get_dt_and_status(self, date_and_status_str):
    
        # カンマ削除
        s1 = date_and_status_str.replace(',', '')
    
        # スペースで区切ってリストに格納
        s2 = s1.split()
        #print(s2)
    
        # 日付文字列に変換
        date_str = f'{s2[2]}/{s2[0]}/{s2[1]}'
        #print(date_str)
    
        # datetime型で格納
        dt = datetime.strptime(date_str, '%Y/%b/%d')
        #print(dt)
    
        status = ''
        if s2[4] == 'Site':
            status = 'Available'

        elif s2[4] == 'First-come':
            status = 'Available'
        
        #elif s2[4] == 'Reserved':
        #    status = 'Reserved'
        
        #elif s2[4] == 'Not':
        #    status = 'Unavailable'
        
        else:
            status = 'Unavailable'
    
        return dt, status, 1


def update_np_availability(park):

    df_dict = {} # {キャンプ場名: df index=Datetime columns=[Available, Unavailable]}
    area_name = park['area']

    # targetsを1個ずつ取得
    for site in park['sites']:

        name = site['name']
        url = site['url']

        rc = RecreationGov(name, url)

        #リンク付きのヘッダー作成
        header = f'<a href="{url}" target="_blank" rel="noopener noreferrer">{name}</a>'
        
        df_dict[header] = rc.get_reservation()

        del rc
        del header
        gc.collect()

    logger.info(df_dict)

    # HTML表用のDF作成
    df_for_html = pd.DataFrame()
    for k, v_df in df_dict.items():
        # 文字列にしておかないと勝手に小数点が入ったり入らなかったりする
        #df_for_html[k] = v_df['Available'].apply(lambda x: str(int(x)))
        df_for_html[k] = v_df['Available'].astype(str)

    # NaNを0埋め
    df_for_html = df_for_html.fillna(0)
    
    # HTML出力用にDatetimeのindexを文字列にして上書き そのままだと00:00:00も出力される
    # https://note.nkmk.me/python-datetime-day-locale-function/
    df_for_html.index = df_for_html.index.strftime('%m/%d<br/>%a')
    #logger.debug(df_for_html)

    # HTML出力 T属性で行列転置 日付をカラムへ
    # Classで直接hover用のクラスを入れる


    page_dict = {} # {置換対象 : 中身}

    # 出力したHTMLを読み込んで背景色を条件に従って追加
    # テンプレ読み込んで置換する方法 https://1-notes.com/python-replace-html/

    # 表のHTML出力
    
    page_dict['dataframe_html'] = df_for_html.T.to_html(escape=False, justify='center', classes='table-hover')

    page_dict['dataframe_html'] = page_dict['dataframe_html'].replace('<td>0</td>','<td bgcolor="666666">0</td>')
    page_dict['dataframe_html'] = page_dict['dataframe_html'].replace('<td>0.0</td>','<td bgcolor="666666">0</td>')

    #logger.debug(page_dict)
    
    # 更新時刻
    dt_now = datetime.now(PST)
    page_dict['sync_datetime'] = dt_now.strftime('%Y/%m/%d %H:%M:%S PST')

    # hタグ用国立公園名
    page_dict['park'] = area_name

    # テンプレートHTMLを読み込んで出力
    # 入力
    template_html_dir = './Web/templates/template.html'
    # 出力
    table_html_dir = HTML_DIR + area_name + '.html'

    with open(template_html_dir, 'r') as f:
        html_body = f.read()

    # {% %}をpage_dataに置換え
    for key, value in page_dict.items():
        html_body = html_body.replace('{% ' + key + ' %}', value)

    # 出力
    with open(table_html_dir, 'w') as f:
        f.write(html_body)
    


if __name__ == '__main__':

    while True:

        try:        
            # キャンプ場をまとめたJSONファイル読み出し
            dir = os.path.join(os.path.dirname(__file__), 'sites.json')
            with open(dir, mode="r") as f:
                json_obj = json.load(f)

            logger.debug(json_obj)

            # 各国立公園ごとにデータを渡してHTMLファイルを作成
            for park in json_obj["parks"]:

                logger.info(f'Area: {park["area"]}')
                update_np_availability(park)

            # 非本番の場合はループしない
            if PRODUCTION == False:
                break

        except Exception as e:
            logger.exception(e)
            sleep(60)