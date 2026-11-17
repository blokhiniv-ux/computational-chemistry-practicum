from flask import Flask, render_template, request, jsonify, send_file
import sqlite3
from io import BytesIO
from rdkit import Chem
from rdkit.Chem import Draw
import database

app = Flask(__name__)

def get_connection():
    conn = database.create_database()
    conn.row_factory = sqlite3.Row
    return conn

def row_to_dict(row):
    return {
        "id": row["id"],
        "name": row["name"],
        "smiles": row["smiles"],
        "formula": row["formula"],
        "mw": row["molecular_weight"],
        "logp": row["logp"],
        "tpsa": row["tpsa"],
        "heavy_atoms": row["heavy_atom_count"],
    }

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/compounds", methods=["GET"])
def get_compounds():
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT * FROM compounds ORDER BY name COLLATE NOCASE"
        ).fetchall()
        return jsonify([row_to_dict(row) for row in rows])
    finally:
        conn.close()

@app.route("/api/compounds", methods=["POST"])
def add_compound():
    data = request.get_json(silent=True) or {}
    name = data.get("name", "")
    smiles = data.get("smiles", "")

    if not name.strip() or not smiles.strip():
        return jsonify({"success": False, "error": "Введите название и SMILES."}), 400

    conn = get_connection()
    try:
        props = database.add_compound(conn, name, smiles)
        return jsonify({"success": True, "message": "Соединение добавлено.", "properties": props})
    except ValueError as exc:
        return jsonify({"success": False, "error": str(exc)}), 400
    finally:
        conn.close()

@app.route("/api/search", methods=["POST"])
def search_substructure():
    data = request.get_json(silent=True) or {}
    smiles = data.get("smiles", "").strip()
    if not smiles:
        return jsonify({"success": False, "error": "Введите SMILES фрагмента."}), 400

    query_mol = Chem.MolFromSmiles(smiles)
    if query_mol is None:
        return jsonify({"success": False, "error": "Некорректный SMILES фрагмента."}), 400

    conn = get_connection()
    try:
        rows = conn.execute("SELECT * FROM compounds ORDER BY name COLLATE NOCASE").fetchall()
        results = []
        for row in rows:
            mol = Chem.MolFromSmiles(row["smiles"])
            if mol is not None and mol.HasSubstructMatch(query_mol):
                results.append(row_to_dict(row))
        return jsonify({"success": True, "results": results, "count": len(results)})
    finally:
        conn.close()

@app.route("/api/image/<int:compound_id>")
def get_image(compound_id):
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT smiles FROM compounds WHERE id = ?", (compound_id,)
        ).fetchone()
    finally:
        conn.close()

    if row is None:
        return "Соединение не найдено.", 404

    mol = Chem.MolFromSmiles(row["smiles"])
    if mol is None:
        return "Не удалось построить структуру: некорректный SMILES.", 500

    image = Draw.MolToImage(mol, size=(260, 200))
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    return send_file(buffer, mimetype="image/png")

@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "message": "Веб-приложение работает."})

if __name__ == "__main__":
    # Локальный учебный сервер. Не используйте debug=True на публичном сервере.
    app.run(host="127.0.0.1", port=5000, debug=False)