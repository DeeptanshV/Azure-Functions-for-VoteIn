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
    
    email = req.get_json().get("email")
    passw = req.get_json().get("pass")

    try:
        con = mysql.connector.connect( host=host,port=port,user=user,password=password,db=db,ssl_ca='C:\\Users\\deept\\Desktop\\functions\\vote\\BaltimoreCyberTrustRoot.crt.pem')
        cursor=con.cursor()
        query=f"select * from userinfo where email=%s" 
        print(query)
        cursor.execute(query,(email,)) 
        # con.commit()
        data=cursor.fetchall()[0]
        
        if(passw==data[2]):
            return func.HttpResponse(
            json.dumps({
                "name":data[0],
                "email":data[1],
                "password":data[2],
                "VotedTo":data[3]
                }),
            mimetype="application/json"
        )
        else:
            return func.HttpResponse(
                json.dumps({
                    "message":"No account found"
                }),
                mimetype="application/json"
            )

        
       
        
    except Exception as e:
        return func.HttpResponse(
            json.dumps({"message":"server error"}),
            mimetype="application/json"
        )