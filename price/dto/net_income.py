class NetIncome:
    def __init__(self, cs_fs, sp_fs, bsns_year):
        self.__cs_fs = cs_fs  # 연결재무제표
        self.__sp_fs = sp_fs  # 별도재무제표
        self.__bsns_year = bsns_year # 사업 연도

    @property
    def cs_fs(self):
        return self.__cs_fs

    @property
    def sp_fs(self):
        return self.__sp_fs

    @property
    def bsns_year(self):
        return self.__bsns_year

    @cs_fs.setter
    def cs_fs(self, value):
        self.__cs_fs = value

    @sp_fs.setter
    def sp_fs(self, value):
        self.__sp_fs = value

    @bsns_year.setter
    def bsns_year(self, value):
        self.__bsns_year = value

    def to_string(self):
        print(f"bsns_year : {self.__bsns_year}\n"
              f"cs_fs : {self.__cs_fs}\n"
              f"sp_fs : {self.__sp_fs}\n")