import pyrebase

config = {
    "apiKey": "AIzaSyCpnmQyTmA9pIDfKFGi2ayhhsSN9YvQgxs",
    "databaseURL": "https://HackathonCovid.firebaseio.com"
}
firebase = pyrebase.initialize_app(config)

db = firebase.database()

def get_chems_data():
    chems_data = db.child('Accounts').child('chemists').get()
    return chems_data

def get_chem_data(username):
    chem_data = get_chems_data()[username]
    return chem_data

def set_chem_data(username, info):     #info is list of all parameter to be passed
    db.child('Accounts').child('clients').child(username).child('pass').set(
        info[0])
    db.child('Accounts').child('clients').child(username).child('email').set(
        info[1])
    db.child('Accounts').child('clients').child(username).child(
        'phone_num').set(info[2])
    db.child('Accounts').child('clients').child(username).child('city').set(
        info[3])
    db.child('Accounts').child('clients').child(username).child('state').set(
        info[4])
    return

def verify(username, info) :
  data = get_chem_data(username) 
  if data == {'pass' : info[0], 'email' : info[1], 'phone_num' : info[2], 'city' : info[3], 'state' : info[4]} :
    return True # Sab jhakaas!
  else :
    return False # Kuch toh gadbad hai daya....


def update_profile(username, info_old, info_new):
    # Info old will contain info in following order -: [password, email, phone_num, city, state]
    # Info new will contain info in following order -: [password, email, phone_num, city, state]
    if verify(username, info_old[0], info_old[1], info_old[2], info_old[3],
              info_old[4]):
        set_chem_data(username, info_new)
        return True  # Firse sab jhakaas!
    else:
        return False  # Daya daal me kuch kaala hai....

def set_stock_data(username, stock_processed) :
  stock_raw_str = ','.join([('[' + med_name + ']x[' + stock_processed[med_name] + ']') for med_name in stock_processed])
  try :
    db.child('Accounts').child('chemist').child(username).child('stock').set(stock_raw_str)
    return True # Daya darwaaza todo!
  except :
    return False # Daya aaj toh daal kaali hogayi hai puri....

def add_to_stock(username, medicine, quantity) :
  # Function to ease handling of adding a new item to stock....
  try :
    curr_stock_data = process_stock_data(username) # Also can be understood as stock_processed....
    if medicine not in curr_stock_data :
      curr_stock_data[medicine] = quantity
    else :
      return False 
    set_stock_data(username, curr_stock_data)
    return True # Daya darwaaze aur le aaunga ye wala to tod de!
  except :
    return False # Daya daal ko mat pina bahut kaali hai bhai pta nhi kya hai!
    
'''def change_med_stock(username, medicine, quantity) :
  # Function to ease handling of adding a new item to stock....
  try :
    curr_stock_data = process_stock_data(username) # Also can be understood as stock_processed....
    curr_stock_data[medicine] = quantity
    set_stock_data(username, curr_stock_data)
    return True 
  except :
    return False'''


def process_stock_data(username) :
  chem_data = get_chem_data(username)
  stock_raw = chem_data['stock'] # Raw form is '[medicine_name]x[quantity]'
  if stock_raw == 'No stock yet.' :
    # If no stock has been uploaded an empty dict is returned.
    return {}
  stock, sample = [], []
  for s in stock_raw :
    sample = [k[1 : -1] for k in s.split('x')]
    stock[sample[0]] = sample[1]
    continue
  return stock # Processed form is {stock : quantity}