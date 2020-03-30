"""
@uthor: Shanthanu Varma
querying.py
A module to query a MySQL database
You will need the python-dev and mysql dev and client installed for this to work
"""

from sshtunnel import SSHTunnelForwarder
import MySQLdb as db
import pandas as pd
import sys

def query(q):
    host = 'some-host-address'
    port = 3306
    username = 'username_for_db'
    password = 'password_for_db'
    proxy_host = 'ssh_proxy_ip_address'
    proxy_port = 00 # port number for the ssh host
    proxy_user = 'username_for_ssh'
    proxy_key = 'absolute_path_for_pem_file'
    database = 'name_of_the_db_to_query'
    result = None
    server = SSHTunnelForwarder((proxy_host, proxy_port),
            ssh_username=proxy_user, ssh_private_key=proxy_key,
            remote_bind_address=(host, 3306))
    server.start()
    conn = db.connect(host='127.0.0.1',
            port=server.local_bind_port,
            user=username,
            passwd=password,
            db=database)
    result = pd.read_sql_query(q, conn) # this returns a dataframe
    conn.close()
    server.close()
    return result
