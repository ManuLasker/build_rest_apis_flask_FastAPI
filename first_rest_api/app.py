from flask import Flask, jsonify, request, render_template

app = Flask(__name__)


# Database
stores = [
    {
        'name': 'My Wonderful Store',
        'items': [
            {
                'name': 'My Item',
                'price': 15.99
            }
        ]
    }
]
# POST - use to received data
# GET - used to send data back only
# index
@app.route('/')
def home():
    return render_template('index.html')

# POST /store data: {name:}
@app.route('/store', methods=['POST'])
def create_store():
    # access data (body)
    request_data = request.get_json()
    new_store = {
        "name": request_data['name'],
        'items': []
    }
    stores.append(new_store)
    return jsonify(new_store)

# GET /store/<string:name>
@app.route('/store/<string:name>', methods=['GET'])
def get_store(name:str):
    for store in stores:
        if store['name'] == name:
            return jsonify(store)
    return f"Store with the name: {name!r} not found"

# GET /store
@app.route('/store')
def get_stores():
    return jsonify({'stores': stores})

# POST /store/<string:name>/item {name:, price:}
@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name:str):
    request_data = request.get_json()
    for store in stores:
        if store['name'] == name:
            store['items'].append({
                'name': request_data['name'],
                'price': request_data['price']
            })
            return jsonify({"store": store})
    return f"Store with the name: {name!r} not found" 

# GET /store/<string:name>/item
@app.route('/store/<string:name>/item')
def get_items_in_store(name:str):
    for store in stores:
        if store['name'] == name:
            return jsonify({'items': store['items']})
    return f"Store with the name: {name!r} not found"


if __name__ == '__main__':
    app.run(port=5000, debug=True)