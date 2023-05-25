class Config:
    SECRET_KEY = 'r4-BjvW6g0Aar4L-orvrtSVWlaxWLhgm'


class DevelopmentConfig(Config):
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'tekepre'


config = {
    'development': DevelopmentConfig
}
