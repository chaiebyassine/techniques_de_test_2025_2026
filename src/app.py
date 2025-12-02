
from flask import Flask, jsonify, Response

from src.binary_utils import encode_triangles, decode_pointset
from src.triangulator.triangulation import compute_triangulation


app = Flask(__name__)

POINTSET_MANAGER_URL = "http://localhost:5001"


@app.route("/triangulation/<pointset_id>", methods=["GET"])
def get_triangulation(pointset_id: str):
    
    # TODO: implémenter
    
    raise NotImplementedError("get_triangulation non implémenté")


def is_valid_uuid(uuid_string: str) -> bool:
   
    # TODO: implémenter
    raise NotImplementedError("is_valid_uuid non implémenté")


def fetch_pointset(pointset_id: str) -> bytes:
   
    # TODO: implémenter
    raise NotImplementedError("fetch_pointset non implémenté")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
