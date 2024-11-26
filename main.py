from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

habitaciones = [
    {
        "id": 1,
        "nom_hab":"Habitación básica con cama individual",
        "precio": 100, 
        "disponibles": 10,
        "image_name":"normal individual.jpg",
        "descripcion":"Una opción económica ideal para viajeros solitarios que buscan comodidad y descanso. Disfruta de un ambiente tranquilo y privado."
    },
    {
        "id": 2,
        "nom_hab":"Habitación básica con doble cama", 
        "precio": 120, 
        "disponibles": 10,
        "image_name" : "normal doble.jpg",
        "descripcion": " Perfecta para dos personas, esta habitación ofrece el espacio ideal para descansar juntos con comodidad y tranquilidad."
    },
    {
        "id": 3,
        "nom_hab":"Habitación premium con cama individual",
        "precio": 200, 
        "disponibles": 10,
        "image_name": "individual suit.jpg",
        "descripcion":"Una opción económica ideal para viajeros solitarios que buscan comodidad y descanso. Disfruta de un ambiente tranquilo y privado."
    },
    {
        "id": 4,
        "nom_hab":"Habitación premium con cama doble",
        "precio": 250, 
        "disponibles": 10,
        "image_name":"premiun boble.jpg",
        "descripcion":"Disfruta de una estancia de lujo en esta habitación con cama doble, perfecta para una pareja o dos personas que busquen confort y estilo."
    },
    {
        "id": 5,
        "nom_hab":"Habitación premium con cama matrimonial",
        "precio": 280, 
        "disponibles": 10,
        "image_name" : "premiun matrimonial.jpg",
        "descripcion" : "Disfruta de una estancia de lujo en esta habitación con cama doble, perfecta para una pareja o dos personas que busquen confort y estilo."
    },
    {
        "id": 6,
        "nom_hab": "Suite con cama individual",
        "precio": 350,
        "disponibles": 10, 
        "image_name" : "suit cama individual.jpg",
        "descripcion" : "Para una experiencia más lujosa , esta suite cuenta con una cama individual, más espacio y servicios exclusivos para una estancia de lujo"
    },
    {
        "id": 7,
        "nom_hab":"Suite con cama doble",
        "precio": 380, 
        "disponibles": 10,
        "image_name": "CAMA DOBLE NUEVAAA.jpg",
        "descripcion": "Ideal para parejas o amigos, esta suite ofrece el confort de una cama doble junto con servicios de primera calidad para tu disfrute."
    },
    {
        "id": 8,
        "nom_hab":"Suite con cama matrimonial",
        "precio": 400,
        "disponibles": 10,
        "image_name": "suit cama  matrimonial.jpg",
        "descripcion": "Una suite ideal para parejas que buscan un lugar de descanso exclusivo. Con todos los servicios premium para una experiencia única."
    },
    {
        "id": 9,
        "nom_hab":"Suite con cama queen",
        "precio": 450, 
        "disponibles": 10,
        "image_name": "la suite con una cama queen.jpg",
        "descripcion" : "Una opción sofisticada para aquellos que buscan una estancia espaciosa con una cama queen, perfecta para el máximo confort y descanso."
    },
    {
        "id": 10,
        "nom_hab":"Habitación Presidencial con cama individual",
        "precio": 500, 
        "disponibles": 10,
        "image_name" : "HABITACION PRECIDENCIAL VIP.jpg",
        "descripcion" : "La opción más lujosa de todas. Con todos los servicios de primera clase, ideal para quienes desean lo mejor en comodidad y exclusividad."
    }
]

reservas = []

@app.route('/')
def pagina1():
  return render_template('pagina1.html', habitaciones=habitaciones)

@app.route("/pagina2", methods=["GET"])
def pagina2():
  habitacion_id = request.args.get("id")
  habitacion = next((h for h in habitaciones if str(h["id"]) == habitacion_id), None)
  return render_template("pagina2.html", habitacion=habitacion, reservas=reservas)

@app.route('/habitaciones', methods=['GET'])
def obtener_habitaciones():
  return jsonify(habitaciones), 200

@app.route('/reservas', methods=['GET'])
def obtener_reservas():
  return jsonify(reservas), 200

@app.route("/reservar", methods=["POST"])
def reservar():
    data = request.json
    nombre = data.get("nombre")
    apellido = data.get("apellido")
    correo = data.get("correo")
    telefono = data.get("telefono")
    fecha_entrada = data.get("checkin")
    fecha_salida = data.get("checkout")
    habitacion_id = int(data.get("habitacion_id"))

    habitacion = next((h for h in habitaciones if h["id"] == habitacion_id), None)

    if habitacion and habitacion["disponibles"] > 0:
        habitacion["disponibles"] -= 1
        nueva_reserva = {
            "id": len(reservas) + 1,
            "nombre": nombre,
            "apellido": apellido,
            "correo": correo,
            "telefono": telefono,
            "fecha_entrada": fecha_entrada,
            "fecha_salida": fecha_salida,
            "habitacion_id": habitacion["id"],
            "habitacion_nombre": habitacion["nom_hab"],
            "habitaciones_disponibles": habitacion["disponibles"],
        }
        reservas.append(nueva_reserva)
        return jsonify({"message": "Reserva realizada con éxito", "reserva": nueva_reserva}), 200
    else:
        return jsonify({"message": "No hay disponibilidad"}), 400


@app.route('/reservas', methods=['DELETE'])
def eliminar_reserva():
    data = request.json
    reserva_id = data.get('id')
    global reservas

    reserva = next((r for r in reservas if r["id"] == reserva_id), None)
    if reserva:
        habitacion = next((h for h in habitaciones if h["id"] == reserva["habitacion_id"]), None)
        if habitacion:
            habitacion["disponibles"] += 1
        reservas = [r for r in reservas if r["id"] != reserva_id]
        return jsonify({"message": "Reserva eliminada con éxito"}), 200
    return jsonify({"message": "Reserva no encontrada"}), 404

if __name__ == '__main__':
    app.run(debug=True)
