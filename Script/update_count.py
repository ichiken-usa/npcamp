# Major module
from logging import getLogger
import json
import os

# Self-made module
import log

### Log ###
LOG_DIR = './Script/Log/'
logger = getLogger(__name__)
log.set_log_config(logger, LOG_DIR, 'update_count.log')


def update_num_of_parks_and_sites():

    # キャンプ場をまとめたJSONファイル読み出し
    dir = os.path.join(os.path.dirname(__file__), 'sites.json')
    with open(dir, mode="r") as f:
        json_obj = json.load(f)

    # HTML置き換え用辞書
    page_dict = {}

    # 国立公園数数
    logger.debug(len(json_obj["parks"]))
    page_dict["num_of_parks"] = str(len(json_obj["parks"]))

    # サイト
    count_sites = 0
    for park in json_obj["parks"]:
        count_sites = count_sites + len(park["sites"])

    logger.debug(count_sites)
    page_dict["num_of_sites"] = str(count_sites)

    # テンプレートHTMLを読み込んで出力
    # 入力
    template_html_dir = './Web/templates/count.html'
    # 出力
    table_html_dir = './Web/pages/count.html'

    with open(template_html_dir, 'r') as f:
        html_body = f.read()

    # {% %}をpage_dataに置換え
    for key, value in page_dict.items():
        html_body = html_body.replace('{% ' + key + ' %}', value)

    # 出力
    with open(table_html_dir, 'w') as f:
        f.write(html_body)

if __name__ == '__main__':

    update_num_of_parks_and_sites()


