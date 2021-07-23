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


def get_chems_data():
    # try this code...
    chems_data = db.child('Accounts').child('chemists').get().val()
    print('TYPE:', type(chems_data))
    return chems_data

def get_chem_data(username):
    # try this code...
    # chem_data = get_chems_data()[username]
    chem_data = db.child('Accounts').child('chemists').child(username).get().val()
    print('TYPE:', type(chem_data))
    return chem_data

def set_chem_data(username, info):     #info is list of all parameter to be passed
    db.child('Accounts').child('chemists').child(username).child('pass').set(
        info[0])
    db.child('Accounts').child('chemists').child(username).child('email').set(
        info[1])
    db.child('Accounts').child('chemists').child(username).child(
        'phone_num').set(info[2])
    db.child('Accounts').child('chemists').child(username).child('city').set(
        info[3])
    db.child('Accounts').child('chemists').child(username).child('state').set(
        info[4])
    db.child('Accounts').child('chemists').child(username).child('stock').set("No stock yet.")
    return

def verify(username, info) :
  data = get_chem_data(username) 
  if data["pass"] == info[0] and data['email'] == info[1] and data['phone_num'] == info[2] and data ['city'] == info[3] and data['state'] == info[4] :
    return True # Sab jhakaas!
  else :
    return False # Kuch toh gadbad hai daya....


def update_profile(username, info_old, info_new):
    # Info old will contain info in following order -: [password, email, phone_num, city, state]
    # Info new will contain info in following order -: [password, email, phone_num, city, state]
        set_chem_data(username, info_new)


def set_stock_data(username, stock_processed) :
  stock_raw_str = ','.join([('[' + med_name + ']~[' + stock_processed[med_name] + ']') for med_name in stock_processed])
  try :
    db.child('Accounts').child('chemists').child(username).child('stock').set(stock_raw_str)
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
  stock, sample = {}, []
  sample = stock_raw.split(",")
  for s in sample :
    s=s.split("~")
    print(s)
    print(sample)
    stock[s[0][1:-1]] = int(s[1][1:-1])
    print(stock)
    continue
  return stock # Processed form is {stock : quantity}