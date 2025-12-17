
import re
import requests
from flask import Flask, jsonify, Response

from src.binary_utils import encode_triangles, decode_pointset
from src.triangulator.triangulation import compute_triangulation


app = Flask(__name__)

POINTSET_MANAGER_URL = "http://localhost:5001"


@app.route("/triangulation/<pointset_id>", methods=["GET"])
def get_triangulation(pointset_id: str):
   
    if not is_valid_uuid(pointset_id):
        return jsonify({"error": "UUID invalide"}), 400
    
    try:
        pointset_binaire = fetch_pointset(pointset_id)
    except ConnectionError:
        return jsonify({"error": "PointSetManager indisponible"}), 503
    except Exception as e:
        return jsonify({"error": str(e)}), 404
    
    try:
        points = decode_pointset(pointset_binaire)
    except ValueError as e:
        return jsonify({"error": f"PointSet invalide: {e}"}), 500
    
    try:
        triangles = compute_triangulation(points)
    except Exception as e:
        return jsonify({"error": f"Erreur triangulation: {e}"}), 500
    
    resultat = encode_triangles(points, triangles)
    
    return Response(resultat, mimetype='application/octet-stream')


def is_valid_uuid(uuid_string: str) -> bool:
   
    pattern = r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'
    return bool(re.match(pattern, uuid_string))


def fetch_pointset(pointset_id: str) -> bytes:
   
    url = f"{POINTSET_MANAGER_URL}/pointset/{pointset_id}"
    
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.ConnectionError:
        raise ConnectionError("PointSetManager indisponible")
    except requests.exceptions.Timeout:
        raise ConnectionError("Timeout PointSetManager")
    
    if response.status_code == 404:
        raise Exception("PointSet non trouvé")
    
    if response.status_code != 200:
        raise Exception(f"Erreur PointSetManager: {response.status_code}")
    
    return response.content


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
