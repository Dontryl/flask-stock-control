from flask import Blueprint, render_template, request, redirect, url_for
from app import db
from app.models import Product

# Define a Blueprint for the routes
bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        stock = int(request.form['stock'])
        new_product = Product(name=name, price=price, stock=stock)
        try:
            db.session.add(new_product)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error adding product: {e}")
        return redirect(url_for('main.index'))
    
    products = Product.query.all()
    return render_template('index.html', products=products)

@bp.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    try:
        db.session.delete(product)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting product: {e}")
    return redirect(url_for('main.index'))

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    # Search for product by ID to edit it
    product = Product.query.get_or_404(id)

    if request.method == 'POST':
        # Update product details with form data
        product.name = request.form['name']
        product.price = request.form['price']
        product.stock = request.form['stock']

        try:
            db.session.commit() # Save changes to the database
            return redirect(url_for('main.index'))
        except:
            return "Houve um erro ao atualizar o produto"
    
    # Render the edit template with the product details
    return render_template('edit.html', product=product)