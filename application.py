#Esta API se encarga de extraer y manipular datos sobre rehabilitadores de animales salvajes estadounidenses, almacenados en el fichero rehabilitadores.py. 

from flask import Flask, jsonify, request
app = Flask(__name__)

from rehabilitadores import rehabilitadores

@app.route("/")
def saludo():
    return "Bienvenido a mi API REST"
    
@app.route('/ping')
def ping():
    return jsonify({"Message": "Pong!"})

@app.route('/rehabilitadores', methods=['GET'])
def GetRehabilitators():
    return jsonify({"rehabilidadores":rehabilitadores})

#la siguiente ruta mostrara un listado de rehabilitadores en el condado seleccionado.
@app.route('/rehabilitadores/counties/<string:county_name>', methods=['GET'])
def GetCounty(county_name):
    countyFound=dict()
    code=0
    for rehabilitador in rehabilitadores:
        if rehabilitador['County'] == county_name.upper():
            code+=1
            countyFound.update({code:rehabilitador})
    if len(countyFound)>0:
        return countyFound

#la siguiente ruta buscara rehabilitadores por su numero de licencia
@app.route('/rehabilitadores/licences/<int:license_number>', methods=['GET'])
def GetLicense(license_number):
    for rehabilitador in rehabilitadores:
        if rehabilitador['License Number'] == license_number:
            return rehabilitador
        return jsonify({"message":"No existe este rehabilitador"})

#la siguiente ruta permitira agregar objetos nuevos al documento
@app.route('/rehabilitadores/add', methods=['POST'])
def AgregarRehabilitador():
    print(request.json)
    NuevoRehabilitador={
        "County": request.json["County"],
        "City": request.json["City"],
        "Species Accepted": request.json["Species Accepted"],
        "Rabies Certified": request.json["Rabies Certified"],
        "Licensee Name": request.json["Licensee Name"],
        "Business Phone": request.json["Business Phone"],
        "License Effective Date": request.json["License Effective Date"],
        "License Expiration Date": request.json["License Expiration Date"],
        "License Type": request.json["License Type"],
        "License Number": request.json["License Number"],
        "Federal Permit Number": request.json["Federal Permit Number"]
    }
    rehabilitadores.append(NuevoRehabilitador)
    return jsonify({'mensaje':'Rehabilitador agregado correctamente','Rehabilitadores': rehabilitadores})

#la siguiente ruta permite modificar objetos existentes al documento
#Me da el mensaje "KeyError: 0" cuando intento actualizar algo en esta seccion. No se muy bien como arreglarlo. 
@app.route('/rehabilitadores/modify/<int:license_number>', methods=['PUT'])
def ModifyItem(license_number):
    for rehabilitador in rehabilitadores:
        if rehabilitador['License Number'] == license_number:
             ItemFound=rehabilitador
    if (len(ItemFound) > 0):
        ItemFound[0]["County"] = request.json["County"]
        ItemFound[0]["City"] = request.json["City"]
        ItemFound[0]["Species Accepted"] = request.json["Species Accepted"]
        ItemFound[0]["Rabies Certified"] = request.json["Rabies Certified"]
        ItemFound[0]["Licensee Name"] = request.json["Licensee Name"]
        ItemFound[0]["Business Phone"] = request.json["Business Phone"]
        ItemFound[0]["License Effective Date"] = request.json["License Effective Date"]
        ItemFound[0]["License Expiration Date"] = request.json["License Expiration Date"]
        ItemFound[0]["License Type"] = request.json["License Type"]
        ItemFound[0]["License Number"] = request.json["License Number"]
        ItemFound[0]["Federal Permit Number"] = request.json["Federal Permit Number"]
        return jsonify({
            "message":"Product Updated",
            "Nuevo Objeto":ItemFound[0]
        })
    return jsonify({"message":"El objeto no se pudo encontrar"})

#la siguiente ruta permite eliminar objetos del documento
@app.route('/rehabilitadores/delete/<int:license_number>', methods=['DELETE'])            
def eliminarRehabilitador(license_number):
    for rehabilitador in rehabilitadores:
        if rehabilitador['License Number'] == license_number:
             ItemFound=rehabilitador
    if len(ItemFound)>0:
        rehabilitadores.remove(ItemFound[0])
        return jsonify({"Message":"Rehabilitador Eliminado", "nuevo listado":rehabilitadores})
    else:
        return jsonify({"message":"No se pudo encontrar este rehabilitador."})

if __name__=='__main__':
    app.run(debug=True, port=4000)