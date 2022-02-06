# Major module
from logging import getLogger
import json
import os

# Self-made module
import log
import common as com

config = com.read_json_from_current_folder('config.json')
TEMPLATE_COUNT_DIR = config['template_count_dir']
TABLE_HTML_DIR = config['table_html_dir']

### Log ###
LOG_DIR = config['log_dir']
logger = getLogger(__name__)
log.set_log_config(logger, LOG_DIR, 'update_count.log')


def update_num_of_parks_and_sites():

    # キャンプ場をまとめたJSONファイル読み出し
    sites_json = com.read_json_from_current_folder('sites.json')

    # HTML置き換え用辞書
    page_dict = {}

    # 国立公園数数
    logger.debug(len(sites_json["parks"]))
    page_dict["num_of_parks"] = str(len(sites_json["parks"]))

    # サイト
    count_sites = 0
    for park in sites_json["parks"]:
        count_sites = count_sites + len(park["sites"])

    logger.debug(count_sites)
    page_dict["num_of_sites"] = str(count_sites)

    # テンプレートHTMLを読み込み、置換して出力
    

    with open(TEMPLATE_COUNT_DIR, 'r') as f:
        html_body = f.read()

    # {% %}をpage_dataに置換え
    for key, value in page_dict.items():
        html_body = html_body.replace('{% ' + key + ' %}', value)

    # 出力
    with open(TABLE_HTML_DIR, 'w') as f:
        f.write(html_body)

if __name__ == '__main__':

    update_num_of_parks_and_sites()


