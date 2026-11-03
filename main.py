from flask import Flask, request, jsonify
import time

app = Flask(__name__)

# Base de datos temporal en memoria para almacenar los servidores escaneados
servidores_db = {}

@app.route('/')
def home():
    return jsonify({
        "status": "online",
        "message": "API de Roba un Huevo Finder V4 activa."
    })

# ========================================================
# ENDPOINT CORREGIDO: Recibe los datos del Bot desde Delta
# ========================================================
@app.route('/actualizar_servidor', methods=['GET', 'POST'])  # <-- El FIX: Se agrega 'POST' explícitamente
def actualizar_servidor():
    if request.method == 'POST':
        try:
            data = request.get_json()
            if not data:
                return jsonify({"error": "No data provided"}), 400
            
            server_id = data.get('serverId')
            if not server_id:
                return jsonify({"error": "Missing serverId"}), 400
                
            # Guardar o actualizar la información en la base de datos temporal
            servidores_db[server_id] = {
                "serverId": server_id,
                "playerCount": data.get('playerCount', 0),
                "eggCount": data.get('eggCount', 0),
                "specialEggs": data.get('specialEggs', 0),
                "timestamp": data.get('timestamp', time.time())
            }
            return jsonify({"status": "success", "message": "Servidor actualizado"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
            
    # Si entras desde el navegador de forma normal (Petición GET)
    return jsonify({"message": "Este endpoint recibe datos mediante POST desde el bot."}), 200

# ========================================================
# ENDPOINT: Envía la lista de servidores a tu panel Tkinter
# ========================================================
@app.route('/obtener_servidores', methods=['GET'])
def obtener_servidores():
    # Limpiar servidores inactivos (viejos de más de 3 minutos) por seguridad
    tiempo_actual = time.time()
    servidores_activos = [
        sv for sv in servidores_db.values() 
        if tiempo_actual - sv.get('timestamp', 0) < 180
    ]
    return jsonify(servidores_activos), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
