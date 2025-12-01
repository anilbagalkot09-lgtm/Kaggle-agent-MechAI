from flask import Flask, request, jsonify
import uuid, threading, time, requests, os

app = Flask(__name__)

@app.route('/orders', methods=['POST'])
def create_order():
    payload = request.json or {}
    order_id = "mock-" + uuid.uuid4().hex[:8]
    # Optionally, simulate callback webhook by POST to an endpoint if configured.
    callback_url = os.environ.get('MOCK_SUPPLIER_CALLBACK')
    if callback_url:
        # simulate async callback after 2s
        def cb():
            time.sleep(2)
            try:
                requests.post(callback_url, json={'order_id': order_id, 'status': 'shipped'})
            except Exception:
                pass
        threading.Thread(target=cb).start()
    return jsonify({'order_id': order_id, 'status': 'placed'})

if __name__ == '__main__':
    app.run(port=8081)
