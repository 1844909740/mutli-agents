from sqlalchemy import create_engine, URL, inspect
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config.setting_sql import settings

engine = create_engine(
    url=URL(
        drivername="mysql+pymysql",
        username=settings.mysql.user,
        password=settings.mysql.password,
        host=settings.mysql.host,
        port=settings.mysql.port,
        database=settings.mysql.database,
        query={}
    ),
    echo=False
)

MysqlBase = declarative_base(
    metadata=None
)

LocalSession = sessionmaker(
    bind=engine,
    autoflush=True
)


def model_to_dict(instance):
    """ instance 可能是 None 或者 []
    metadata_ 需要转为 metadata
    :param instance:
    :return
    """
    return{
        "metadata" if column.key == "metadata_" else column.key: getattr(instance, column.key)
        for column in inspect(instance).mapper.column_attrs
    } if instance else instance


