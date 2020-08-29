# -*- coding: utf-8 -*-
import app.inspector.engines.interface as interface

from app.definitions.models import Datastore

from app.inspector.engines.postgresql_inspector import PostgresqlInspector
from app.inspector.engines.mysql_inspector import MySQLInspector
from app.inspector.engines.sqlserver_inspector import SQLServerInspector
from app.inspector.engines.oracle_inspector import OracleInspector


HIVE_METASTORE_DEFINITIONS_QUERY = """
SELECT source.* FROM
(
    SELECT
        d.NAME as table_schema,
        d.DB_ID as schema_object_id,
        t.TBL_NAME as table_name,
        t.TBL_ID as table_object_id,
        t.TBL_TYPE,
        MD5(CONCAT(t.TBL_ID, '/', p.PKEY_NAME)) as column_object_id,
        p.PKEY_NAME as column_name,
        p.INTEGER_IDX as ordinal_position,
        p.PKEY_TYPE as data_type,
        0 as "is_nullable",
        1 as "is_primary",
        '' as default_value
    FROM TBLS t
    JOIN DBS d ON t.DB_ID = d.DB_ID
    JOIN PARTITION_KEYS p ON t.TBL_ID = p.TBL_ID
    LEFT JOIN TABLE_PARAMS tp ON (t.TBL_ID = tp.TBL_ID AND tp.PARAM_KEY='comment')
    UNION
    SELECT
            d.NAME as table_schema,
            d.DB_ID as schema_object_id,
            t.TBL_NAME as table_name,
            t.TBL_ID as table_object_id,
            t.TBL_TYPE,
            MD5(CONCAT(t.TBL_ID, '/', c.COLUMN_NAME)) as column_object_id,
            c.COLUMN_NAME as column_name,
            c.INTEGER_IDX as ordinal_position,
            c.TYPE_NAME as data_type,
            0 as "is_nullable",
            0 as "is_primary",
            '' as default_value
    FROM TBLS t
    JOIN DBS d ON t.DB_ID = d.DB_ID
    JOIN SDS s ON t.SD_ID = s.SD_ID
    JOIN COLUMNS_V2 c ON s.CD_ID = c.CD_ID
    LEFT JOIN TABLE_PARAMS tp ON (t.TBL_ID = tp.TBL_ID AND tp.PARAM_KEY='comment')
) source
ORDER by table_schema, table_name, ordinal_position
"""


supported_external_metastores = {
    Datastore.MYSQL: MySQLInspector,
    Datastore.POSTGRESQL: PostgresqlInspector,
    Datastore.SQLSERVER: SQLServerInspector,
    Datastore.ORACLE: OracleInspector,
}


class HiveMetastoreInspector(object):
    """Access external Hive metastore via JDBC connection. Supports schema version >= 2.0.0 on every datastore.
    """
    sys_schemas = []

    table_properties = []

    definitions_sql = HIVE_METASTORE_DEFINITIONS_QUERY

    def __init__(self, host, username, password, port, database, extras=None):
        self.extras = extras or {}
        self.inspector = supported_external_metastores[self.dialect](
            host,
            username,
            password,
            port,
            database,
        )
        self.inspector.override_definitions_sql(HIVE_METASTORE_DEFINITIONS_QUERY)

    @classmethod
    def has_indexes(self):
        return False

    @property
    def dialect(self):
        return self.extras.get('dialect')

    def get_db_version(self):
        result = self.get_first('SELECT SCHEMA_VERSION FROM VERSION')
        if len(result):
            return result['SCHEMA_VERSION']
        return None

    def verify_connection(self):
        """bool: Verify the ability to connect to the datastore.
        """
        return self.inspector.verify_connection()

    def get_tables_and_views(self, *args, **kwargs):
        """generator: Retrieve the full list of table definitions for the provided datastore.
        """
        return self.inspector.get_tables_and_views(*args, **kwargs)

    def get_indexes(self, *args, **kwargs):
        """list: Retrieve indexes from the database.
        """
        return []