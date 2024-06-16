from flask import Blueprint, jsonify, request
from models.products import Products, db, ma


productos_bp = Blueprint('productos', __name__)

class ProductoSchema(ma.Schema):
    class Meta:
        fields=('id','nombre','precio','stock','imagen')


product_schema=ProductoSchema()  # El objeto producto_schema es para traer un producto
products_schema=ProductoSchema(many=True)  # El objeto productos_schema es para traer multiples registros de producto

# crea los endpoint o rutas (json)
@productos_bp.route('/productos',methods=['GET'])
def get_Productos():
    all_products=Products.query.all() # el metodo query.all() lo hereda de db.Model
    result=products_schema.dump(all_products)  #el metodo dump() lo hereda de ma.schema y
                                                 # trae todos los registros de la tabla
    return jsonify(result)     # retorna un JSON de todos los registros de la tabla




@productos_bp.route('/productos/<id>',methods=['GET'])
def get_producto(id):
    product=Products.query.get(id)
    return product_schema.jsonify(product)   # retorna el JSON de un producto recibido como parametro


@productos_bp.route('/productos/<id>',methods=['DELETE'])
def delete_producto(id):
    product=Products.query.get(id)
    db.session.delete(product)
    db.session.commit()                     # confirma el delete
    return product_schema.jsonify(product) # me devuelve un json con el registro eliminado


@productos_bp.route('/productos', methods=['POST']) # crea ruta o endpoint
def create_producto():
    #print(request.json)  # request.json contiene el json que envio el cliente
    nombre=request.json['nombre']
    precio=request.json['precio']
    stock=request.json['stock']
    imagen=request.json['imagen']
    new_product=Products(nombre,precio,stock,imagen)
    db.session.add(new_product)
    db.session.commit() # confirma el alta
    return product_schema.jsonify(new_product)


@productos_bp.route('/productos/<id>' ,methods=['PUT'])
def update_producto(id):
    product=Products.query.get(id)
    product.nombre=request.json['nombre']
    product.precio=request.json['precio']
    product.stock=request.json['stock']
    product.imagen=request.json['imagen']

    db.session.commit()    # confirma el cambio
    return product_schema.jsonify(product)    # y retorna un json con el producto