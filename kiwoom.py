from PyQt5.QAxContainer import *
import pythoncom

class Kiwoom:
    def __init__(self):
        self.login = False
        self.ocx = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.ocx.OnEventConnect.connect(self.OnEventConnect)

    #로그인 메서드 호출
    def CommConnect(self):
        self.ocx.dynamicCall("CommConnect()")
        while not self.login:
            pythoncom.PumpWaitingMessages()

    # 로그인 성공 여부
    def OnEventConnect(self, err_code):
        if err_code == 0:
            print("로그인 성공")
            self.login = True
        else:
            print("로그인 실패")


#     def SetInputValue(self, id, value):
#         self.ocx.dynamicCall("SetInputValue(QString, QString)", id, value)
#
#     def CommRqData(self, rqname, trcode, next, screen):
#         self.ocx.dynamicCall("CommRqData(QString, QString, int, QString)", rqname, trcode, next, screen)
#
#     def GetCommData(self, trcode, rqname, index, item):
#         data = self.ocx.dynamicCall("GetCommData(QString, QString, int, QString)", trcode, rqname, index, item)
#         return data.strip()

    # 종목코드의 종목명을 반환
    def GetMasterCodeName(self, code):
        name = self.ocx.dynamicCall("GetMasterCodeName(QString)", code)
        return name

    # 통신 접속 상태 반환
    def GetConnectState(self):
        result = self.ocx.dynamicCall("GetConnectState()")
        return result

    # 사용자 정보 및 계좌 정보
    # ACCOUNT_CNT - 전체 계좌 개수를 반환
    # ACCNO - 전체 계좌를 반환, 계좌별 구분은 ';'이다
    # USER_ID - 사용자의 ID를 반환
    # USER_NAME - 사용자명을 반환한다
    # KEY_BSECGB - 키보드보안 해지여부 0:정상 1:해지
    # FIREW_SECGB - 방화벽 설정 여부 0:미설정 1:설정 2:해지
    def GetLoginInfo(self, tag):
        result = self.ocx.dynamicCall("GetLoginInfo(QString)", tag)
        return result


