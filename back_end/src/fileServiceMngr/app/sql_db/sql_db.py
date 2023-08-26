from typing import List, Dict
from sql_db.sql_dbconf import dbCon


def clients_history(clientId)-> List[Dict]:
    connection = dbCon()
    cursor = connection.cursor()
    query = "SELECT id, fileId, fileName, activity FROM client_history1 WHERE clientId="+str(clientId)
    cursor.execute(query)
    results = [{"id":id,"fileId":fileId,"fileName":fileName,"activity":activity} for (id, fileId, fileName, activity) in cursor]
    cursor.close()
    connection.close()
    return results


def update_client_history(req_data,id,filename):
    connection = dbCon()
    cursor = connection.cursor()
    # query = "INSERT INTO client_history1 (clientName,clientId,fileId,mongo_fileId,fileName,activity) VALUES (%s,%s,%s,%s,%s,%s)"
    # val   =  (req_data["clientName"],1,req_data["fileId"],inserted_id,filename,req_data['activity'])
    query = "INSERT INTO client_history1 (clientName,clientId,fileId,mongo_fileId,filename,activity) VALUES (%s,%s,%s,%s,%s,%s)"
    val   =  (req_data["clientName"],1,req_data["fileId"],str(id),filename,req_data["activity"])

    cursor.execute(query,val)
    connection.commit()
    if (cursor.rowcount == 1):
       cursor.close()
       return True
    else:
       cursor.close()
       return False



