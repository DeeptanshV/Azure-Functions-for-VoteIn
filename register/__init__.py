import logging
import json
import azure.functions as func
import mysql.connector 
import pathlib

def get_ssl_cert():
    current_path = pathlib.Path(__file__).parent.parent
    print(str(current_path/ 'BaltimoreCyberTrustRoot.crt'))
    return str(current_path/ 'BaltimoreCyberTrustRoot.crt')


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    host = 'main-server.mysql.database.azure.com'
    user ='Deeptansh'
    password = "Tannu@2996"
    port = "3306"
    db="users"
    
    name = req.get_json().get("name")
    email = req.get_json().get("email")
    passw = req.get_json().get("pass")

    
    con = mysql.connector.connect( host=host,port=port,user=user,password=password,db=db,ssl_ca='C:\\Users\\deept\\Desktop\\functions\\vote\\BaltimoreCyberTrustRoot.crt.pem')
    cursor=con.cursor()
    query="insert into userinfo(name,email,pass) values(%s,%s,%s)" 
    records=[(name,email,passw)]
    cursor.executemany(query,records) 
    con.commit()
    return func.HttpResponse(
        json.dumps({"NAME" : name, "Email" : email, "Pass": passw, "ssl" : get_ssl_cert()}),
        mimetype="application/json"
    )

