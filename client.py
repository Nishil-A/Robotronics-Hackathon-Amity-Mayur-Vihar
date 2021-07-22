import pyrebase

config = {
  "apiKey": "AIzaSyCpnmQyTmA9pIDfKFGi2ayhhsSN9YvQgxs",
  "databaseURL": "https://HackathonCovid.firebaseio.com"
}
firebase = pyrebase.initialize_app(config)

db = firebase.database()

def get_clients_data() :
  clients_data = db.child('Accounts').child('clients').get()
  return clients_data

def get_client_data(username) :
  client_data = get_clients_data()[username]
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
  if verify(username, info_old[0], info_old[1], info_old[2], info_old[3], info_old[4]) :
    set_client_data(username, info_new)
    return True # Firse sab jhakaas!
  else :
    return False # Daya daal me kuch kaala hai....