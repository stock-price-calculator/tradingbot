class StockTotalQuantity:

    def __init__(self, bsns_year, qty):
        self.__bsns_year = bsns_year # 사업 연도
        self.__qty = qty  # 해당 년도 총 주식 발행 수

    @property
    def bsns_year(self):
        return self.__bsns_year

    @property
    def qty(self):
        return self.__qty

    @qty.setter
    def qty(self, value):
        self.__qty = value

    def to_string(self):
        print(f"bsns_year: {self.bsns_year}\nqty: {self.qty}")

