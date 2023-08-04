class PER:
    def __init__(self, bsns_year, sp_per, cs_per):
        self._bsns_year = bsns_year
        self._sp_per = sp_per
        self._cs_per = cs_per

    @property
    def bsns_year(self):
        return self._bsns_year

    @property
    def sp_per(self):
        return self._sp_per

    @property
    def cs_per(self):
        return self._cs_per

    def to_string(self):
        print("사업년도 : ", self._bsns_year, "\n연결재무제표 PER : ", self._cs_per, "별도 재무제표 PER : ", self._sp_per)