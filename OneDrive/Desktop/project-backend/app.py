from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# مدل سفارش
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100))
    product_name = db.Column(db.String(100))
    amount = db.Column(db.Integer)
    paid = db.Column(db.Boolean, default=False)

with app.app_context():
    db.create_all()

# فرم سفارش
@app.route('/')
def index():
    return render_template('order_form.html')

# ثبت سفارش
@app.route('/order', methods=['POST'])
def create_order():
    name = request.form['customer_name']
    product = request.form['product_name']
    amount = int(request.form['amount'])

    order = Order(customer_name=name, product_name=product, amount=amount)
    db.session.add(order)
    db.session.commit()
    return redirect(f'/pay/{order.id}')

# پرداخت تستی (بدون زرین‌پال)
@app.route('/pay/<int:order_id>')
def pay(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template('fake_payment.html', order=order)

# تأیید پرداخت تستی
@app.route('/confirm/<int:order_id>')
def confirm(order_id):
    order = Order.query.get_or_404(order_id)
    order.paid = True
    db.session.commit()
    return f"پرداخت تستی انجام شد. سفارش {order.product_name} ثبت شد."

# صفحه مدیریت سفارش‌ها
@app.route('/admin/orders')
def view_orders():
    orders = Order.query.order_by(Order.id.desc()).all()
    return render_template('admin_orders.html', orders=orders)

if __name__ == '__main__':
    app.run(debug=True)