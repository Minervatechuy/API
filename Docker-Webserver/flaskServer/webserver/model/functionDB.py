import configDB as configDB

def doQuerySQL(SQL):
    conexion = configDB.connect()
    cur = conexion.cursor()
    cur.execute(SQL)
    result = cur.fetchall()
    cur.close()
    conexion.close()
    return result

def doStoredProcedure(name, args):
    conexion = configDB.connect()
    cur = conexion.cursor()
    result = cur.callproc(name, args)
    conexion.commit()
    cur.close()
    conexion.close()
    x=[]
    for result in cur.stored_results():
            x.append(result.fetchall())
    return x