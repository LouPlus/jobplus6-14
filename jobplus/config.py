class BaseConfig(object):
    """ 配置基类 """
    SECRET_KEY = 'jobplus-6-14'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    INDEX_PER_PAGE = 9
    ADMIN_PER_PAGE = 15


class DevelopmentConfig(BaseConfig):
    """ 开发环境配置 """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://jobplus:jobplus@localhost:3306/jobplus?charset=utf8'


class ProductionConfig(BaseConfig):
    """ 生产环境配置 """
    pass


class TestingConfig(BaseConfig):
    """ 测试环境配置 """
    pass


configs = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
