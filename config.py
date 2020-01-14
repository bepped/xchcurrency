import pandas as pd
import xml.etree.ElementTree as ET
import requests
import re
from requests.exceptions import ConnectionError, HTTPError

def get_ndec(strfloat):
    tmplist = strfloat.strip().split('.')    
    return 0 if len(tmplist) == 1 else len(tmplist[1])

class Config:

    XML_URI = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist-90d.xml"
    CUBE_NS = "{http://www.ecb.int/vocabulary/2002-08-01/eurofxref}"
    DB_EXCH_CURRENCY = pd.DataFrame()
    CURRENCY_NDEC = {'EUR': 2}
    STARTUP_STATUS = "NOK"
    HTTP_ERROR = ""
    DATE_REGEX = re.compile('\d\d\d\d\-\d\d\-\d\d')

    @classmethod
    def init_app(cls, app):
        try:
            response = requests.get(cls.XML_URI)
            response.raise_for_status()
        except HTTPError as he:
            cls.HTTP_ERROR = f'Error on startup: requests will not be fulfilled: {he}'
        except ConnectionError as ce:
            cls.HTTP_ERROR = f'Error on startup: requests will not be fulfilled: {ce}'
        else:
            xml_eurofxref = response.content
            root = ET.XML(xml_eurofxref)
            root_cube = root.find(f'{cls.CUBE_NS}Cube')

            if root_cube is None:
                app.config['HTTP_ERROR'] = f'Error on startup: unknown namespace {cls.CUBE_NS}'
                return
                
            for cube_time in root_cube:
                time_val = cube_time.attrib['time']
                cls.DB_EXCH_CURRENCY.loc[time_val, 'EUR'] = 1.00   
                for cube in cube_time:
                    curr = cube.attrib['currency'] 
                    rate = cube.attrib['rate'] 
                    cls.DB_EXCH_CURRENCY.loc[time_val, curr] = float(cube.attrib['rate'])   
                    ndec = get_ndec(cube.attrib['rate'])
                    if curr not in cls.CURRENCY_NDEC or cls.CURRENCY_NDEC[curr] < ndec:
                        cls.CURRENCY_NDEC[curr] = ndec
                        
            cls.STARTUP_STATUS = "OK"           

        app.config['HTTP_ERROR'] = cls.HTTP_ERROR
        app.config['STARTUP_STATUS'] = cls.STARTUP_STATUS
        
class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True

class ProductionConfig(Config):

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.ERROR)
        app.logger.addHandler(file_handler)

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
