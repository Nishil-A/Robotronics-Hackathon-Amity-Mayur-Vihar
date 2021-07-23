import pyrebase

config = {
    "apiKey": "AIzaSyAJ_70v8wR-4VuNhQ1kTeWxglok16XsBr0",
    "authDomain": "hackathon-aismv.firebaseapp.com",
    "databaseURL": "https://hackathon-aismv-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "hackathon-aismv",
    "storageBucket": "hackathon-aismv.appspot.com",
    "messagingSenderId": "976273729445",
    "appId": "1:976273729445:web:4c5323e4d606ed512a6a4c",
    "measurementId": "G-40YVGY36CR"
  }

firebase=pyrebase.initialize_app(config)
db=firebase.database()

def get_clients_data() :
  clients_data = db.child('Accounts').child('clients').get().val()
  return clients_data

def get_client_data(username) :
  client_data = db.child('Accounts').child('clients').child(username).get().val()
  return client_data

def set_client_data(username, info) :
  db.child('Accounts').child('clients').child(username).child('pass').set(info[0])
  db.child('Accounts').child('clients').child(username).child('email').set(info[1])
  db.child('Accounts').child('clients').child(username).child('phone_num').set(info[2])
  db.child('Accounts').child('clients').child(username).child('city').set(info[3])
  db.child('Accounts').child('clients').child(username).child('state').set(info[4])
  return

def verify(username, info) :
  data = get_client_data(username) 
  if data == {'pass' : info[0], 'email' : info[1], 'phone_num' : info[2], 'city' : info[3], 'state' : info[4]} :
    return True # Sab jhakaas!
  else :
    return False # Kuch toh gadbad hai daya....

def update_profile(username, info_old, info_new) :     #Nishil(for myself, aditya kindly ignore)- info_old to be stored before hand when person logs in
  # Info old will contain info in following order -: [password, email, phone_num, city, state]
  # Info new will contain info in following order -: [password, email, phone_num, city, state]
    set_client_data(username, info_new)