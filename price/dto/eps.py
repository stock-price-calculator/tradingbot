class EPS:
    def __init__(self, bsns_year, sp_eps, cs_eps):
        self._bsns_year = bsns_year  # 사업 연도
        self._sp_eps = sp_eps  # 별도 재무제표로 구한 EPS
        self._cs_eps = cs_eps  # 연결 재무제표로 구한 EPS

    @property
    def bsns_year(self):
        return self._bsns_year

    @property
    def sp_eps(self):
        return self._sp_eps

    @property
    def cs_eps(self):
        return self._cs_eps

    @sp_eps.setter
    def sp_eps(self,value):
        self._sp_eps = value

    @cs_eps.setter
    def cs_eps(self, value):
        self._cs_eps = value

    def to_string(self):
        print("사업년도 : ", self._bsns_year, "\n연결재무제표 EPS : ", self._cs_eps, "별도 재무제표 EPS : ", self._sp_eps)
