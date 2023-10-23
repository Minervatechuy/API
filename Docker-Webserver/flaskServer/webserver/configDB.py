
import mariadb

def connect():
    config = {'host': '172.24.0.2','port': 3306,'user': 'minervatech','password': 'MinervallTech.','database': 'minervatech'}
    return mariadb.connect(**config)