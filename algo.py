import pyrebase
config = {
  "apiKey": "AIzaSyCpnmQyTmA9pIDfKFGi2ayhhsSN9YvQgxs",
  "databaseURL": "https://HackathonCovid.firebaseio.com"
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()

import chemist, client
def prepare_stock_info() :
  # Prepares info about stocks available with various chems,
  # in the form-: {store : [{medicine : quantity}, city, state]]}
  chem_data = chemist.get_chems_data()
  stock_info, sample = {}, []
  for chem_name in list(chem_data.keys()) :
    sample = [chemist.process_stock_data(chem_name), chem_data['city'], chem_data['state']]
    stock_info[chem_name] = sample
    continue
  return stock_info

# We can have stock dict like -:
# store : [{medicine : quantity}, city, state]? 
# # stock_data = {k : chem_data[k]['stock'] for k in chem_data}
# # like this -:
# # [medicine_name]x[quantity] inside a string
# # we can then split using 'x' and then we can strip the
# # first and last square brackets....

def find_closest_stores_with_stocks(medicine_name, client_username) :
  # stores closeness data in {store_name : [closeness_status, quantity, city, state]}

  client_data = client.get_client_data(client_username)
  client_city = client_data['city']
  client_state = client_data['state']
  stock_info = prepare_stock_info()

  close_stores = {}
  for store in stock_info :
    if not medicine_name in list(stock_info[store].keys()) :
      continue
    chem_data = chemist.get_chem_data(store)
    closeness_status = 'not_near'
    if stock_info[store][2] == client_state :
      closeness_status = 'close'
      if stock_info[store][1] == client_city :
        closeness_status = 'quite_close'
    close_stores[store] = [closeness_status, stock_info[store][medicine_name], chem_data['city'], chem_data['state']]
    continue
  return close_stores

def get_suggested_count(store_name) :
  try :
    count = int(db.child('Counters').child(store_name).get())
    return count
  except :
    return 0

def reset_suggested_count(store_name) :
  return set_suggested_count(store_name, 0)

def set_suggested_count(store_name, count) :
  try :
    db.child('Counters').child(store_name).set(str(count))
    return True
  except :
    return False

def add_to_suggested_counter(store_name) :
  curr_count = get_suggested_count(store_name)
  curr_count += 1
  return set_suggested_count(store_name, curr_count)

def find_best_suggestions(medicine_name, client_username) :
  possible_suggestions = find_closest_stores_with_stocks(medicine_name, client_username)

  buffer_count_ratio = 0.5
  best_suggestions = {}
  for store in possible_suggestions :
    # The if statement will check to make sure the suggested people do not
    # exceed the quantity.
    if get_suggested_count(store) <= (buffer_count_ratio * possible_suggestions[store][1]) :
      best_suggestions[store] = [possible_suggestions[store][0], possible_suggestions[store][1], possible_suggestions[store][2], possible_suggestions[store][3]]
    continue
  
  # Here we sort it based on the quantity of medicine....
  sorted_best_suggestions = {k[0] : k[1] for k in sorted(best_suggestions.items(), lambda x : x[1], True)}
  return sorted_best_suggestions

def find_best_suggestion(medicine_name, client_username) :
  return find_best_suggestions(medicine_name, client_username)[0]