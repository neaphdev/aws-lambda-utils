
import sys
sys.path.insert(1,'libs')

import json
#import mysql.rds_config as rds_config
import pymysql as pymysql
import pymysql.cursors
#from sshtunnel import SSHTunnelForwarder
import mysql.rds_config as cfg
class MySQLData:
    """Database connection class."""

    def __init__(self):  # , config):
        self.db_host =cfg.db_host#'10.2.3.243'  # config.db_host
        self.db_username =cfg.db_username #'rstier'  # config.db_user
        self.db_password =cfg.db_password #'tP-axO41gxbKHCscLwZnOG'  # config.db_password
        self.db_port = cfg.db_port#int(3306)  # config.db_port
        self.db_name = cfg.db_name#'pdp_mdw_dev'  # config.db_name
        self.conn = None

    def open_connection(self):
        """Connect to MySQL Database."""
        try:
            if self.conn is None:
                self.conn = pymysql.connect(host=self.db_host, db=self.db_name, port=self.db_port, user=self.db_username,password=self.db_password, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor, connect_timeout=30)
        except pymysql.MySQLError as e:
            print('ERROR pymysql', e)
        except Exception as e:
            print('ERROR otro', e)
        finally:
            print('Connection opened successfully.')

    def select_query(self, query, param):
        """Execute SQL query."""
        try:
            self.open_connection()
            with self.conn.cursor() as cur:
                print(cur.mogrify(query, param))
                records = []
                cur.execute(query,param)
                #columns = tuple([i[1] for i in cur.description])
                for row in cur:
                    records.append(row)
                return records

        except pymysql.MySQLError as e:
            print('ERROR:', e)

        except Exception as e:
            print('ERROR:', e)

        finally:
            if self.conn:
                self.conn.close()
                self.conn = None
                print('Database connection closed.')

    def insert_query(self, query, param):
        """Execute SQL query."""
        try:
            self.open_connection()
            with self.conn.cursor() as cur:
                print(cur.mogrify(query, param))
                result = cur.execute(query,param)
                self.conn.commit()
                affected = cur.rowcount
                cur.close()
                return affected

        except pymysql.MySQLError as e:
            print('ERROR:',e)
            
            raise Exception("Error en BD")
        finally:
            if self.conn:
                self.conn.close()
                self.conn = None
                print('Database connection closed.')
    
