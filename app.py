# RESTfull API using Flask

import json
from flask import Flask, jsonify, request, redirect
from flask_restful import Resource, Api, url_for
import pandas as pd
import os


app = Flask(__name__)
api = Api(app)


class Users(Resource):
    @app.route('/users/')
    def page_users ():
        return "Página dos usuários"

    @app.route("/users/getAll", methods=["GET"])
    def get_data():
        verify_json_file() 
        data = read_data_from_json_file()
        return jsonify(data)
    
    @app.route('/users/getByCpf/<string:cpf>', methods= ["GET"])
    def get_specific_data(cpf):
        verify_json_file()
        data = read_data_from_json_file()
        for person in data:
            if person.get("cpf")==cpf:
                return jsonify(person)
        return "Este CPF não está cadastrado no banco de dados."


    @app.route("/users/create/", methods=["POST"])
    def add_person():
        verify_json_file() 
        
        data = request.get_json()

        required_fields = {'nome_completo', 'data_nascimento', 'endereco', 'cpf', 'estado_civil'}
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Campo '{field}' está faltando no JSON"}), 400  
            
        nome_completo = data["nome_completo"]
        data_nascimento = data["data_nascimento"]
        endereco = data["endereco"]
        cpf = data["cpf"]
        estado_civil = data["estado_civil"]
        
        if len(cpf) != 11:
            return jsonify({"error": "CPF deve conter exatamente 11 caracteres"}), 400


        new_person = {
            "nome_completo": nome_completo,
            "data_nascimento": data_nascimento,
            "endereco": endereco,
            "cpf": cpf,
            "estado_civil": estado_civil,
        }

        try:
            verify_cpf_in_file(new_person["cpf"])
        except CPFExistsError as e:
            return str(e), 400
        
        persons = read_data_from_json_file()
        persons.append(new_person)
        write_data_to_json_file(persons)
        return "Pessoa com CPF {} adicionada com sucesso.".format(cpf), 200
        
    @app.route('/users/manage/<string:cpf>', methods=["PATCH", "DELETE"])
    def manage_person(cpf):
        verify_json_file() 
        people = read_data_from_json_file()

        if request.method == "PATCH":
            for update_person in people:
                if update_person['cpf'] == cpf:
                    updated_data = request.json  
                    update_person.update(updated_data)
                    write_data_to_json_file(people)
                    return jsonify(update_person)

            return "Pessoa com CPF {} não encontrada.".format(cpf), 404

        elif request.method == "DELETE":
            for update_person in people:
                if update_person['cpf'] == cpf:
                    people.remove(update_person)
                    write_data_to_json_file(people)
                    return jsonify(update_person)

            return "Pessoa com CPF {} não encontrada.".format(cpf), 404
    pass


api.add_resource(Users, "/users/")

@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('home'))

@app.route('/')
def home():
    return 'Página inicial'


def read_data_from_json_file():
    try:
        with open("data.json", "r") as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        return []


def write_data_to_json_file(persons):
    with open("data.json", "w") as json_file:
        json.dump(persons, json_file, indent=4)


def verify_json_file ():
    file_name = "data.json"
    if os.path.exists (file_name) and os.stat(file_name).st_size != 0:
        with open (file_name, 'r') as file:
            data = json.load (file)
            return True
    else:
        with open (file_name,'w') as file:
            data = []
            json.dump(data, file) 
            return True
        
class CPFExistsError(Exception):
    pass
        
def verify_cpf_in_file (cpf):
    with open ("data.json", 'r') as file:
        data = json.load(file)
        for register in data:
            if register.get("cpf")==cpf:
                raise CPFExistsError ("O CPF {} já está cadastrado no banco de dados.".format(cpf))
    return False

app.run(port=5001)
