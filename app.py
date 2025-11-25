import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# URL do banco via variável de ambiente (padrão: SQLite local)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///data.db")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(255), nullable=True)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "description": self.description}


@app.before_first_request
def create_tables():
    db.create_all()


@app.route("/items", methods=["GET"])
def list_items():
    items = Item.query.all()
    return jsonify([item.to_dict() for item in items]), 200


@app.route("/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    item = Item.query.get_or_404(item_id)
    return jsonify(item.to_dict()), 200


@app.route("/items", methods=["POST"])
def create_item():
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "Campo 'name' é obrigatório"}), 400

    item = Item(
        name=data["name"],
        description=data.get("description")
    )
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_dict()), 201


@app.route("/items/<int:item_id>", methods=["PUT", "PATCH"])
def update_item(item_id):
    item = Item.query.get_or_404(item_id)
    data = request.get_json() or {}

    if "name" in data:
        item.name = data["name"]
    if "description" in data:
        item.description = data["description"]

    db.session.commit()
    return jsonify(item.to_dict()), 200


@app.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return "", 204


@app.route("/")
def healthcheck():
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    # Importante: 0.0.0.0 para funcionar no container
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
