import threading
import requests
from typing import Union
import xml.etree.ElementTree as ET
import os
from price.dto.eps import EPS
from price.dto.net_income import NetIncome
from price.dto.per import PER
from price.dto.stock_total_quantity import StockTotalQuantity
import price.constants as constants

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

# EPS 구하기
def calculateEPS(code: str, start_year: int = 2016, result: [EPS] = []):
    total_qty: [StockTotalQuantity] = []
    incomes: [NetIncome] = []
    threads_incomes = []
    threads_totqy = []
    corp_code = get_corpcode_from_xml(code)

    try:
        for year in range(start_year, 2023):
            thread_incomes = threading.Thread(target=get_net_incomes_from_single_financial_statement,
                                              args=(corp_code, year, incomes))
            thread_totqy = threading.Thread(target=get_stock_quantity, args=(corp_code, year, total_qty))

            thread_incomes.start()
            thread_totqy.start()

            threads_incomes.append(thread_incomes)
            threads_totqy.append(thread_totqy)

        for ti in threads_incomes:
            ti.join()
        for tt in threads_totqy:
            tt.join()

        incomes = sort_by_bsns_year(incomes)
        total_qty = sort_by_bsns_year(total_qty)
        for i in range(2023 - start_year):
            sp_eps = float(incomes[i].sp_fs) / float(total_qty[i].qty)
            cs_eps = float(incomes[i].cs_fs) / float(total_qty[i].qty)
            result.append(EPS(incomes[i].bsns_year, sp_eps, cs_eps))

        return result
    except Exception as e:
        print("Errrrrrrrrrrr", e)
        return False

# PER = 시가 총액 / 당기순 이익
def calculate_PER(code: str, start_year: int = 2016, result: [PER] = []):
    corp_code = get_corpcode_from_xml(code)
    total_price = []
    incomes: [NetIncome] = []
    m_threads = []

    thread_get_total_price = threading.Thread(target=get_total_price, args=(code, total_price))
    thread_get_total_price.start()

    m_threads.append(thread_get_total_price)
    for year in range(start_year, 2023):
        m_thread = threading.Thread(target=get_net_incomes_from_single_financial_statement,
                                    args=(corp_code, year, incomes))
        m_thread.start()
        m_threads.append(m_thread)

    for run_thread in m_threads:
        run_thread.join()

    incomes = sort_by_bsns_year(incomes)
    for i in range(2023 - start_year):
        sp_per = total_price[0] / float(incomes[i].sp_fs)
        cs_per = total_price[0] / float(incomes[i].cs_fs)
        bsns_year = 2016 + i
        per = PER(bsns_year, sp_per, cs_per)
        result.append(per)

    return result

# 단일회사 당기순이익 정보 가져오기
def get_net_incomes_from_single_financial_statement(corp_code: str, bsns_year: str, results: [NetIncome]):  # 단일회사 재무정보
    net_income = NetIncome("", "", bsns_year)

    # 재무제표는 12월에 공시하는 사업보고서를 기준으로 찾는다
    get_url = f"{constants.GET_FNLTT_SINGLE_ACNT}?crtfc_key={constants.API_KEY}&corp_code={corp_code}&" \
              f"bsns_year={bsns_year}&reprt_code={constants.ReportCode.BUSINESS}"
    response = requests.get(get_url)
    body = response.json()
    contents = body['list']

    for el in contents:
        # 연결 재무제표와 별도 재무제표 모두 반환
        if el["account_nm"] == "당기순이익" and el["fs_nm"] == "연결재무제표":
            net_income.cs_fs = el["thstrm_amount"].replace(",", "")
        if el["account_nm"] == "당기순이익" and el["fs_nm"] == "재무제표":
            net_income.sp_fs = el["thstrm_amount"].replace(",", "")

    results.append(net_income)
    return


# 회사의 총 주식 수 구하기 (보통주)
def get_stock_quantity(corp_code: str, bsns_year: int, totqy: [StockTotalQuantity]):
    stock = StockTotalQuantity(bsns_year, "")
    get_url = f"{constants.GET_ISSTK_CNT}?crtfc_key={constants.API_KEY}&corp_code={corp_code}&" \
              f"bsns_year={bsns_year}&reprt_code={constants.ReportCode.BUSINESS}"
    response = requests.get(get_url)
    body = response.json()
    contents = body["list"]

    for content in contents:
        if content["se"] == "보통주":  # 구분(증권의 종류(우선주, 보통주), 합계 비고) -> 합계만 고려
            stock.qty = content["istc_totqy"].replace(",", "")
            totqy.append(stock)
            break  # 발행주식의 총 수
    return

# 주식 종목 코드로 Dart 기업 코드 가져오기
def get_corpcode_from_xml(code: str) -> str:
    print(os.path.dirname(os.path.abspath(__file__)) + '/static/CORPCODE.xml')
    tree = ET.parse(os.path.dirname(os.path.abspath(__file__)) + '/static/SAMPLE.xml')
    root = tree.getroot()
    is_find = False
    for el in root.iter("result"):
        for ele in el.iter("list"):
            if ele.find("stock_code").text == code:
                is_find = True
                return ele.find("corp_code").text

    if not is_find:
        return ""

def get_total_price(code: str, total_price: [int]) -> None:  # 시가 총액 가져오기
    driver = init_driver()
    prices_str = get_prices_str(driver, code)
    total_price_calculated = calculate_total_price(prices_str.text)  # 시가 총액
    total_price.append(total_price_calculated)
    driver.quit()
    return


# 시가 총액 구하기
def init_driver(strategy: Union[None | str] = "eager"):
    options = Options()
    options.page_load_strategy = strategy
    options.add_argument("headless")
    return webdriver.Chrome(options=options)


# driver = selenium.driver
# code : 주식 종목 코드
def get_prices_str(driver, code: str) -> WebElement:
    driver.get(f"https://finance.naver.com/item/main.naver?code={code}")
    return driver.find_element(By.CSS_SELECTOR, "#_market_sum")


def calculate_total_price(prices_str: str) -> int:
    prices = prices_str.split("조")
    print(prices)
    if len(prices) == 2:
        return int(prices[0].replace(",", "")) * 1000000000000 + int(prices[1].replace(',', '')) * 100000000
    else:
        return int(prices[0].replace(",", "")) * 100000000

# 사업 연도로 정렬하기
def sort_by_bsns_year(_list: list[any]) -> list[any]:
    _list = sorted(_list, key=lambda x: x.bsns_year)
    return _list