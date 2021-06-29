import json 

def jsonToDict(fileName):
    with open(fileName) as file:
        data = json.load(file)
        return data


# Forma de escribir un archivo json:
"""
#---------------------------------------------------
data = {
"height" : 3,
"width" : 6,
"lenght" : 4,
"window_loss" : 0.01,
"heater_a" : 5,
"heater_b" : 30,
"ambient_temperature" : 25,
"filename" : "Test.npy"
}

with open('Test.json', 'w') as file:
    json.dump(data, file, indent=4)
#----------------------------------------------------
"""



# Ejemplo de uso uwu
"""
#-----------------------------------------------------
data = {}
data['clients'] = []
data['clients'].append({
    'first_name': 'Sigrid',
    'last_name': 'Mannock',
    'age': 27,
    'amount': 7.17})

data['clients'].append({
    'first_name': 'Joe',
    'last_name': 'Hinners',
    'age': 31,
    'amount': [1.90, 5.50]})

data['clients'].append({
    'first_name': 'Theodoric',
    'last_name': 'Rivers',
    'age': 36,
    'amount': 1.11})

with open('data.json', 'w') as file:
    json.dump(data, file, indent=4)
    
#------------------------------------------------------
"""