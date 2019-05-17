import os
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import logging

from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from util import LogUtil

BASE_URL: str = "https://tellburgerking.com.cn/"
BASE_CODE: str = "9977232200950159"
log1 = LogUtil.LogHelper()

options = webdriver.ChromeOptions()
# prefs = {'profile.managed_default_content_settings.images': 2}
# options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(options=options)


def next_page(): driver.find_element_by_id("NextButton").click()


def waiting_for_loading():
    WebDriverWait(driver, 15).until(EC.title_contains("BK"))
    return "谢谢" in driver.title
    # WebDriverWait(driver, 15).until(EC.element_selection_state_to_be((By.ID, idStr)))


try:
    # 第一个页面
    driver.get(BASE_URL)
    # log1.debug("666")

    waiting_for_loading()
    next_page()

    # 第二个页面
    waiting_for_loading()
    for num in range(0, 6):
        driver.find_element_by_id("CN" + str(num + 1)).send_keys(BASE_CODE[3 * num:3 * num + 3])

    next_page()

    # 调查页面
    while 1:
        if waiting_for_loading():
            break
        try:
            WebDriverWait(driver, 1).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "radioSimpleInput")))
            for elem in driver.find_elements_by_class_name("radioSimpleInput")[::-1]: elem.click()
        except TimeoutException as e:
            logging.error("本页没有单选框")
        try:
            WebDriverWait(driver, 1).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "checkboxSimpleInput")))
            driver.find_elements_by_class_name("checkboxSimpleInput")[-1].click()
        except TimeoutException as e:
            logging.error("本页没有复选框")
        try:
            WebDriverWait(driver, 1).until(EC.presence_of_all_elements_located((By.TAG_NAME, "select")))
            for selectEle in driver.find_elements_by_tag_name("select"):
                select = Select(selectEle)
                answer = select.options[-1].text
                select.select_by_visible_text(answer)
        except TimeoutException as e:
            logging.error("本页没有选择框")
        next_page()

    # 获取结果
    baseCodeStr = "调查代码：" + BASE_CODE
    valCodeStr = driver.find_element_by_class_name("ValCode").text

    with open('tellburgerking[%s].txt' % BASE_CODE, 'wt', encoding="utf-8") as f:
        f.writelines([baseCodeStr, "\n", valCodeStr])

except TimeoutException as e:
    logging.exception("超时")
except Exception as e:
    logging.exception("异常")

    # logger = logging.getLogger('mylogger')
    # logger.setLevel(logging.ERROR)
    #
    # # 创建一个handler，用于写入日志文件
    # fh = logging.FileHandler(os.path.join(os.getcwd(), 'log.txt'))
    # fh.setLevel(logging.DEBUG)
    #
    # # 再创建一个handler，用于输出到控制台
    # ch = logging.StreamHandler()
    # ch.setLevel(logging.DEBUG)
    #
    # # 定义handler的输出格式
    # formatter = logging.Formatter('%(asctime)s - %(module)s.%(funcName)s.%(lineno)d - %(levelname)s - %(message)s')
    # fh.setFormatter(formatter)
    # ch.setFormatter(formatter)
    #
    # # 给logger添加handler
    # logger.addHandler(fh)
    # logger.addHandler(ch)
    #
    # logger.error(e)


finally:
    driver.close()
