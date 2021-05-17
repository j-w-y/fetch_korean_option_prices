import requests
from abc import abstractmethod
from pandas import DataFrame
from datetime import date
import datetime

class Post():
    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0"}
    def read(self, **params):
        resp = requests.post(self.url, headers=self.headers, data=params)
        return resp
    @property
    @abstractmethod
    def url(self):
        return NotImplementedError

class KrxWebIO(Post):
    def read(self, **params):
        #params.update()
        params.update(bld=self.bld)
        resp = super().read(**params)
        return resp.json()
    
    @property
    def url(self):
        return "http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd"
    
    @property
    @abstractmethod
    def bld(self):
        return NotImplementedError
    
    @bld.setter
    def bld(self, val):
        pass
    
    @property
    @abstractmethod
    def fetch(self, **params):
        return NotImplementedError

class option_names(KrxWebIO):
    @property
    def bld(self):
        return "dbms/comm/finder/finder_drvprodisu"
    
    def fetch(self) -> DataFrame:
        result = self.read(
            secugrpId='OP',
            prodId='KRDRVOPEQU',
            prodIdDetail='KRDRVOPEQU',
            expYy='',
            expMm='',
        )
        return DataFrame(result['block1'])

class option_prc(KrxWebIO):
    @property
    def bld(self):
        return "dbms/MDC/STAT/standard/MDCSTAT12602"
    
    def fetch(self, code:str, \
            start= (date.today().replace(day=1) - datetime.timedelta(days=1)).strftime("%Y%m%d"),\
            end=date.today().strftime("%Y%m%d")) -> DataFrame:
        dd = dict(
            strtDd= start,
            endDd= end,
            isuCd= code,
        )
        result = self.read(**dd, rghtTpCd='T')
        return DataFrame(result['output'])

def get_option_names():
    return option_names().fetch()

def get_option_prc(code):
    return option_prc().fetch(code)

