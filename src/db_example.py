from urllib.parse import quote_plus
from sqlalchemy import create_engine

USER = "root"
PASSWORD = "your_mysql_password"   
HOST = "localhost"
DATABASE = "streampulse"

def get_engine():
    return create_engine(
        f"mysql+pymysql://{USER}:{quote_plus(PASSWORD)}@{HOST}:3306/{DATABASE}"
    )