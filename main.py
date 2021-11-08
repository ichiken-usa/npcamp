# https://tanuhack.com/selenium-bs4-heroku/

# Major module
from datetime import datetime, timedelta, timezone
from logging import getLogger
from time import sleep
import pandas as pd
from tqdm import tqdm # pip3 install tqdm
import gc

# Selenium: pip3 install selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# Self-made module
import log

production = True
parent_dir = '/home/ichi/VSCode/npcamp/'
production_dir = '/usr/share/nginx/html/'

index_org_dir = parent_dir + 'html/index_template.html'

if production == False:
    index_dir = parent_dir + 'index.html'

else:
    index_dir = production_dir + 'index.html'

read_data_flag = True
cycle = 4 # 1 cycle 15 days

PST = timezone(timedelta(hours=-8))


### Log ###
log_dir = parent_dir + 'Log/'
logger = getLogger(__name__)
log.set_log_config(logger, log_dir, 'get_site_availability.log')

class RecreationGov:

    def __init__(self, target):
        
        self.site_name = target[0]
        self.address = target[1]

        # Headless Chromeをあらゆる環境で起動させるオプション
        options = Options()
        if production == True:
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-extensions')
            options.add_argument('--proxy-server="direct://"')
            options.add_argument('--proxy-bypass-list=*')
            options.add_argument('--start-maximized')
            options.add_argument('--headless')

            self.driver = webdriver.Chrome(chrome_options=options)
            self.driver.implicitly_wait(20) #sec

        else:
            options.add_argument('--headless')

            self.driver = webdriver.Chrome(chrome_options=options)
            self.driver.set_window_size(800,1000)
            self.driver.set_window_position(0,0)
            self.driver.implicitly_wait(10) #sec

    def get_reservation(self, cycle):

        try:
            # Open web page
            logger.info(f'Open: {self.address}')
            self.driver.get(self.address)
            sleep(1)

            # 毎回Popupが表示されるページあり -> Popupのクローズボタンがある場合はクリックして閉じる
            # idが無いのでXPathを使用
            xpath = '/html/body/div[9]/div/div/div/div/div/div/div/button'
            self.__close_popup_by_xpath(xpath)

            # 適当なid取ってPAGE_DOWNキーを投げる
            # 別にスクロールする必要はないけど、テーブル見えないとやってる感が無い
            id="campsite-filter-search"
            self.__send_key_by_id(id, Keys.PAGE_DOWN)

            # 取り出した情報格納用リスト
            availability_list = [] #[[Date][Status][1]]

            start = 0
            #cycle = 1
            for i in range(start,cycle):

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
                logger.info(f'rec-availability-date 要素数: {len(elms)}')


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

if __name__ == '__main__':


    if read_data_flag == True:

        targets = [
            ['Yosemite Upper Pines','https://www.recreation.gov/camping/campgrounds/232447'],
            ['Yosemite Lower Pines','https://www.recreation.gov/camping/campgrounds/232450'],
            ['Yosemite North Pines','https://www.recreation.gov/camping/campgrounds/232449'],
            #['Grand Canyon Mather Campground', 'https://www.recreation.gov/camping/campgrounds/232490'],
            #['Grand Canyon Desert View Campground', 'https://www.recreation.gov/camping/campgrounds/258825'],
            #['Grand Canyon North Rim Campground', 'https://www.recreation.gov/camping/campgrounds/232489'],
            ]

        df_dict = {} # {キャンプ場名: df index=Datetime columns=[Available, Unavailable]}

        # targetsを1個ずつ取得
        for target in targets:
            rc = RecreationGov(target)

            #リンク付きのヘッダー作成
            header = f'<a href="{target[1]}" target="_blank" rel="noopener noreferrer">{target[0]}</a>'
            
            df_dict[header] = rc.get_reservation(cycle)

            del rc
            del header
            gc.collect()

        logger.debug(df_dict)

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


    page_dict['dataframe_html'] = df_for_html.T.to_html(escape=False, justify='center', classes='table-hover')

    page_dict['dataframe_html'] = page_dict['dataframe_html'].replace('<td>0</td>','<td bgcolor="666666">0</td>')
    page_dict['dataframe_html'] = page_dict['dataframe_html'].replace('<td>0.0</td>','<td bgcolor="666666">0</td>')

    #logger.debug(page_dict)
    
    # 更新時刻
    dt_now = datetime.now(PST)
    page_dict['sync_datetime'] = dt_now.strftime('%Y/%m/%d %H:%M:%S PST')
    logger.info(page_dict['sync_datetime'])

    logger.debug(page_dict)

    # MainのHTMLを読み込み
    with open(index_org_dir, 'r') as f:
        index_str = f.read()

    # {% %}をpage_dataに置換え
    for key, value in page_dict.items():
        index_str = index_str.replace('{% ' + key + ' %}', value)

    #logger.debug(index_str)
    with open(index_dir, 'w') as f:
        f.write(index_str)
    


    # Bootstrapテーブルの横スクロール 
    # https://marmooo.blogspot.com/2019/05/bootstrap.html
    # https://qumeru.com/magazine/354