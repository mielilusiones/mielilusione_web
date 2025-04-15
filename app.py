from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

def cargar_productos():
    try:
        with open('productos.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def guardar_producto(nuevo_producto):
    productos = cargar_productos()

    # Asignar ID único automáticamente
    nuevo_producto['id'] = productos[-1]['id'] + 1 if productos else 1

    productos.append(nuevo_producto)
    with open('productos.json', 'w') as f:
        json.dump(productos, f, indent=4)

@app.route('/')
def inicio():
    productos = cargar_productos()
    destacados = productos[:4]  # Primeros 4 productos como destacados
    ofertas = productos[-2:] if len(productos) > 2 else productos  # Últimos 2 productos como ofertas
    return render_template('inicio.html', destacados=destacados, ofertas=ofertas)

@app.route('/catalogo')
def catalogo():
    productos = cargar_productos()
    return render_template('catalogo.html', productos=productos)

@app.route('/agregar', methods=['GET', 'POST'])
def agregar_producto():
    if request.method == 'POST':
        producto = {
            'nombre': request.form['nombre'],
            'imagen': request.form['imagen'],
            'precio': request.form['precio'],
            'descripcion': request.form['descripcion'],
            'categoria': request.form['categoria']
        }
        guardar_producto(producto)
        return redirect(url_for('catalogo'))
    return render_template('agregar_producto.html')

@app.route('/categoria/<nombre>')
def categoria(nombre):
    productos = cargar_productos()
    filtrados = [p for p in productos if p.get('categoria') == nombre]
    return render_template('categoria.html', productos=filtrados, categoria=nombre)

@app.route('/producto/<int:producto_id>')
def producto_detalle(producto_id):
    productos = cargar_productos()
    for producto in productos:
        if producto.get('id') == producto_id:
            return render_template('producto_detalle.html', producto=producto)
    return "Producto no encontrado", 404

if __name__ == '__main__':
    app.run(debug=True)
