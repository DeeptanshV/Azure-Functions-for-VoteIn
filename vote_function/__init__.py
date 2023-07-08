import logging
import pathlib
import mysql.connector 
import json
import azure.functions as func

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
    
    username=req.get_json().get("email")
    participant=req.get_json().get("participant-id")
    
    try:
        con = mysql.connector.connect( host=host,port=port,user=user,password=password,db=db,ssl_ca='C:\\Users\\deept\\Desktop\\functions\\vote\\BaltimoreCyberTrustRoot.crt.pem')
        cursor=con.cursor()
        query=f"update userinfo set VotedTo=%s where email=%s" 
        print(query)
        cursor.execute(query,(participant,username)) 
        # data=cursor.fetchall()
        con.commit()
        return func.HttpResponse(
            json.dumps({
                "Message":"Thank you, Your vote has been registered"
            }),
            mimetype="application/json"
        )
        
        
    except Exception as e:
        print(e)
        return func.HttpResponse(
            json.dumps({"Message":"Could not register your vote"}),
            mimetype="application/json"
        )
