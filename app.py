from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv
from flask_cors import CORS


load_dotenv()

SHOP = os.getenv("SHOPIFY_SHOP")
TOKEN = os.getenv("SHOPIFY_API_TOKEN")

app = Flask(__name__)
CORS(app, origins=["https://5denwh-06.myshopify.com"])

@app.route('/')
def home():
    return "🚀 Backend COD Shopify en Flask funcionando"

@app.route('/create-order', methods=['POST'])
def create_order():
    data = request.get_json()

    payload = {
        "order": {
            "line_items": [
                {
                    "variant_id": data.get("variantId"),
                    "quantity": data.get("quantity", 1)
                }
            ],
            "customer": {
                "first_name": data.get("firstName"),
                "last_name": data.get("lastName"),
                "email": data.get("email"),
                "phone": data.get("phone")
            },
            "shipping_address": {
                "first_name": data.get("firstName"),
                "last_name": data.get("lastName"),
                "address1": data.get("address1"),
                "city": data.get("city"),
                "province": data.get("province"),
                "zip": data.get("zip"),
                "country": "Ecuador"
            },
            "financial_status": "pending",
            "tags": "COD",
            "email": data.get("email")
        }
    }

    try:
        response = requests.post(
            f"https://{SHOP}/admin/api/2024-01/orders.json",
            json=payload,
            headers={
                "X-Shopify-Access-Token": TOKEN,
                "Content-Type": "application/json"
            }
        )

        response.raise_for_status()
        order = response.json()["order"]

        return jsonify({
            "success": True,
            "orderId": order["id"],
            "orderStatusUrl": order["order_status_url"]
        })

    except requests.exceptions.RequestException as e:
        print("❌ Error al crear pedido:", e)
        return jsonify({ "success": False, "error": str(e) }), 500

if __name__ == '__main__':
    app.run(debug=True, port=3001)
