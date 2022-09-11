from flask import Flask, request, abort, Response
from flask import redirect
from twilio.twiml.messaging_response import MessagingResponse
from flask_cors import CORS
from flask import render_template
import json
import sharesteadySmartContract as shalgo
import pymongo

from hashlib import sha256


aclient = shalgo.init_algo()
greenhousepri, greenhousepub = shalgo.get_account(" REDACTED prosper")
plantpri, plantpub = shalgo.get_account("REDACTED")

rate = 1000 ##price of carbon credits, per microAlgos

def initdb():
    
    client = pymongo.MongoClient("hacks.mongo.cosmos.azure.com:10255")

    
    # mongostr = "mongodb+srv://redacted"
    # client = pymongo.MongoClient(mongostr)
    db = client["shellhacks2022"]

    return client, db

app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    return render_template("MNMT.html")

@app.route("/about")
def about():
    return """
    <h1 style='color: red;'>I'm a red H1 heading!</h1>
    <p>This is a lovely little paragraph</p>
    <code>Flask is <em>awesome</em></code>"""



@app.route("/processcarbonator", methods=['GET', 'POST'])
def paybill():
    
    global aclient, greenhousepub, plantpub, plantpri, rate
    
    totalval = 0
    client, db = initdb()
    uvals = []
    
    col = db.regs
    
    for x in col.find():
        totalval += x['dep'] *rate
        uv = {}
        uv['userid'] = x['userid']
        uv['val'] = x['dep'] * rate
        uvals.append (uv)
        
        ##update dep
        col.update_one({"regid":x['regid']}, {"$set": {"dep":0}})
        rate = rate /2  ##progressive

    rate = 1000  ##reset
    
    totalval = int(totalval)
    ##payout
    print (totalval)
    gen, gh, first_valid_round, last_valid_round, fee = shalgo.init2(aclient)
    
    stx = shalgo.sendAmount(plantpub, fee, first_valid_round, last_valid_round, gh, greenhousepub, totalval, plantpri)
    shalgo.confirmTransaction(aclient, stx)
    
    print("carbon credits sequestered")
    
    ##now refund everyone
    
    col = db.users
    
    for x in col.find():
        # dep = x['deposit']
        ref = 0
        for y in uvals:
            if y['userid'] == x['id']:
                ref = x['staked'] - y['val']
                upub = x['public']
                ref = int(ref)
                
                stx =  shalgo.sendAmount(plantpub, fee, first_valid_round, last_valid_round, gh, upub, ref, plantpri)
                shalgo.confirmTransaction(aclient, stx)
                
                print ("refund for "+x['name'] + " paid")
                
                col.update_one({"userid":y['userid']}, {"$set": {"staked":0}})
                
            
    

    res = request.get_json()
    print (res)

    resraw = request.get_data()
    print (resraw)

##    args = request.args
##    form = request.form
##    values = request.values

##    print (args)
##    print (form)
##    print (values)

##    sres = request.form.to_dict()


    status = {}
    status["server"] = "up"
    status["request"] = res
    status["paidamount"] = totalval

    statusjson = json.dumps(status)

    print(statusjson)

    js = "<html> <body>OK THIS WoRKS</body></html>"

    resp = Response(statusjson, status=200, mimetype='application/json')
    ##resp.headers['Link'] = 'http://google.com'

    return resp




@app.route("/stakeandsequester", methods=['POST'])
def makedepositl():
    
    res = request.get_json()
    print (res)

    resraw = request.get_data()
    print (resraw)
    
    global aclient, plantpub, rate
    
    totalval = 0
    client, db = initdb()
    uvals = []
    
    col = db.users
    
    for x in col.find():
        if x['id'] == res['userid']:
##            upub1 = x['public']
            amt = int(res['amount'])
            mne  = x['mnemonic']
            print (mne)
            upri, upub = shalgo.get_account(mne)
            
            print (upub)
##            if upub != upub1:
##                print ("errorred")
##                break
            
            gen, gh, first_valid_round, last_valid_round, fee = shalgo.init2(aclient)
    
            stx = shalgo.sendAmount(upub, fee, first_valid_round, last_valid_round, gh, plantpub, amt, upri)
            shalgo.confirmTransaction(aclient, stx)
            print("deposit made")
            
            odep = int(x['staked'])
            ndep = odep + amt
            ndep = str(ndep)
                           
            col.update_one({"id":x['id']}, {"$set": {"staked":ndep}})
            break
                
            

##    args = request.args
##    form = request.form
##    values = request.values

##    print (args)
##    print (form)
##    print (values)

##    sres = request.form.to_dict()


    status = {}
    status["server"] = "up"
    status["request"] = res 

    statusjson = json.dumps(status)

    print(statusjson)

    js = "<html> <body>OK THIS WoRKS</body></html>"

    resp = Response(statusjson, status=200, mimetype='application/json')
    ##resp.headers['Link'] = 'http://google.com'

    return resp








@app.route("/dummyJson", methods=['GET', 'POST'])
def dummyJson():

    res = request.get_json()
    print (res)

    resraw = request.get_data()
    print (resraw)

##    args = request.args
##    form = request.form
##    values = request.values

##    print (args)
##    print (form)
##    print (values)

##    sres = request.form.to_dict()


    status = {}
    status["server"] = "up"
    status["request"] = res 

    statusjson = json.dumps(status)

    print(statusjson)

    js = "<html> <body>OK THIS WoRKS</body></html>"

    resp = Response(statusjson, status=200, mimetype='application/json')
    ##resp.headers['Link'] = 'http://google.com'

    return resp


if __name__ == '__main__':
    # app.run()
    # app.run(debug=True, host = '45.79.199.42', port = 8090)
    app.run(debug=True, host = 'localhost', port = 8090)  ##change hostname here
