from conf.db.db_conf import sql as sql_configuration
from ...src.data.sql.sql import sql

db=sql(sql_configuration, True)


RESERVED_STATUS_NAMES=["Online","Outage","Maintanance"]