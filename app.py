from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = "mude-esta-chave-em-producao"

DATA_DIR = "/data"
os.makedirs(DATA_DIR, exist_ok=True)
db_path = os.path.join(DATA_DIR, "items.db")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Item(db.Model):
    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    preco = db.Column(db.Float, nullable=False)
    em_estoque = db.Column(db.Boolean, default=True)

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return redirect(url_for("listar_items"))

@app.route("/items")
def listar_items():
    items = db.session.scalars(select(Item)).all()
    return render_template("list_items.html", items=items)

@app.route("/items/new", methods=["GET", "POST"])
def criar_item():
    if request.method == "POST":
        nome = request.form.get("nome")
        descricao = request.form.get("descricao")
        preco = request.form.get("preco")
        em_estoque = request.form.get("em_estoque") == "on"
        if not nome or not preco:
            flash("Nome e preço são obrigatórios.", "danger")
            return redirect(url_for("criar_item"))
        try:
            preco = float(preco)
        except ValueError:
            flash("Preço inválido.", "danger")
            return redirect(url_for("criar_item"))
        item = Item(nome=nome, descricao=descricao, preco=preco, em_estoque=em_estoque)
        db.session.add(item)
        db.session.commit()
        flash("Item criado com sucesso!", "success")
        return redirect(url_for("listar_items"))
    return render_template("form_item.html", acao="Criar", item=None)

@app.route("/items/<int:item_id>")
def detalhar_item(item_id):
    item = db.get_or_404(Item, item_id)
    return render_template("detail_item.html", item=item)

@app.route("/items/<int:item_id>/edit", methods=["GET", "POST"])
def editar_item(item_id):
    item = db.get_or_404(Item, item_id)
    if request.method == "POST":
        nome = request.form.get("nome")
        descricao = request.form.get("descricao")
        preco = request.form.get("preco")
        em_estoque = request.form.get("em_estoque") == "on"
        if not nome or not preco:
            flash("Nome e preço são obrigatórios.", "danger")
            return redirect(url_for("editar_item", item_id=item.id))
        try:
            preco = float(preco)
        except ValueError:
            flash("Preço inválido.", "danger")
            return redirect(url_for("editar_item", item_id=item.id))
        item.nome = nome
        item.descricao = descricao
        item.preco = preco
        item.em_estoque = em_estoque
        db.session.commit()
        flash("Item atualizado!", "success")
        return redirect(url_for("listar_items"))
    return render_template("form_item.html", acao="Editar", item=item)

@app.route("/items/<int:item_id>/delete", methods=["GET", "POST"])
def deletar_item(item_id):
    item = db.get_or_404(Item, item_id)
    if request.method == "POST":
        db.session.delete(item)
        db.session.commit()
        flash("Item removido!", "success")
        return redirect(url_for("listar_items"))
    return render_template("confirm_delete.html", item=item)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
