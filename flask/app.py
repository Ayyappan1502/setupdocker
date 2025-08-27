import os
from flask import Flask, request
from psycopg_pool import ConnectionPool as pool


def dbConnect():
    pass

app = Flask(__name__)

@app.route('/about',methods=['GET'])
def about():
    # get the version of server to show in response
    version = os.environ.get('APP_VERSION')
    return "Welcome to the Home Page!"

@app.route('/secrets',methods=['GET'])
def secrets():
    creds = dict()
    creds['db_password']= os.environ.get('DB_PASSWORD')
    creds['app_token']= os.environ.get('APP_TOKEN')
    creds['api_key'] = open("/run/secrets/api_key","r").read()
    creds['api_key_v2'] = open("/api_key.txt","r").read()
    return creds,200

@app.route('/config',methods=['GET'])
def config():
    conf = dict()
    conf['config_dev'] = open("/config-dev.yaml", "r").read()
    conf['config_dev_v2'] = open("/config-dev.yaml","r").read()
    
    return conf, 200

@app.route('/volumes',methods=['GET','POST'])
def volumes():
    filename='/data/test.txt'
    
    if request.method =='POST':
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename,'w') as f :
            f.write('Customer record')
        return 'saved:)',201
    else:
        f = open(filename,'r')
        return f.read(),200
    
def saveItems(priority, task, table, pool):
    """instert new category"""
    
    #Connect to an existing database
    with pool.connection() as conn:
        # Open cursor  to perform database operation
        with conn.cursor() as cur:
             #prepare the query to db
             query = f'INSERT INTO {table} (priority, task) VALUES (%s, %s)'
             #send the query to postgresSQL
             cur.execute(query, (priority, task))
             
             #make the changes  to the db persistent
             conn.commit()
             
             
def getItems(table, pool):
    
    with pool.connection()  as conn:
        with conn.cursor() as cur:
            
            query = f'SELECT item_id, priority, task FROM {table}'
            
            cur.execute(query)
            
            items = []
            
            for rec in cur:
                item =  {'id':rec[0],'priority':rec[1],'task': rec[2]}
                items.append(item)
                # return list of item
            return items
        
    @app.route('/items',methods=['GET',POST])
    def items():
        match request.method:
            case 'POST' :
                req = request.get_json()
                saveItems(req['priority'],req['task'],'item',pool)
                
                return {'message' : 'item saved!'},200
            case 'GET':
                items = getItems('item',pool)
                
                return items,200
            case _:
                return {'message': 'method not allowed'},405
                
            
    