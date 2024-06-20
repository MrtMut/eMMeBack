from flask import Blueprint, jsonify, request
from models.tablas import Projects, db, ma


projects_bp = Blueprint('projects', __name__)

class ProjectsSchema(ma.Schema):
    class Meta:
        fields=('id','name_project','category','description','imagen', 'user_id')

project_schema=ProjectsSchema()  
projects_schema=ProjectsSchema(many=True) 



# crea los endpoint o rutas (json)
@projects_bp.route('/projects',methods=['GET'])
def get_Projects():
    all_projects=Projects.query.all() # el metodo query.all() lo hereda de db.Model
    if all_projects:
        result=projects_schema.dump(all_projects)
        return jsonify(result), 200
    else:
        return jsonify({'message': 'Projects not found'}), 404


@projects_bp.route('/projects/<id>',methods=['GET'])
def get_Project(id):
    project=Projects.query.get(id)
    if project:
        return project_schema.jsonify(project), 200   # retorna el JSON de un producto recibido como parametro
    else:
        return jsonify({'message': 'Project not found'}), 404
    

@projects_bp.route('/projects/<id>',methods=['DELETE'])
def delete_Project(id):
    project=Projects.query.get(id)
    db.session.delete(project)
    db.session.commit()                     # confirma el delete
    return project_schema.jsonify(project), 200 # me devuelve un json con el registro eliminado


@projects_bp.route('/projects', methods=['POST']) # crea ruta o endpoint
def create_Project():
    print(request.json)  # request.json contiene el json que envio el cliente
    name_project=request.json['name']
    category=request.json['category']
    description=request.json['description']
    image=request.json['image']
    new_project=Projects(name_project,category,description,image)
    db.session.add(new_project)
    db.session.commit() # confirma el alta
    return project_schema.jsonify(new_project), 200


@projects_bp.route('/projects/<id>' ,methods=['PUT'])
def update_project(id):
    project=Projects.query.get(id)
    project.name_project=request.json['name']
    project.category=request.json['category']
    project.description=request.json['description']
    project.image=request.json['image']
    db.session.commit()    # confirma el cambio
    return project_schema.jsonify(project), 200    # y retorna un json con el producto