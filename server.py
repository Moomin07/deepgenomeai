from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder='.')

# 🧬 the moomin's basic situmulated ai
DISEASE_DB = {
    "sickle-cell": {
        "normal_code": "ATGGTG",
        "mutation_position": 5,
        "expected_base": "T",
        "found_base": "A",
        "name": "Sickle Cell Disease",
        "explanation": "Your red blood cells become banana-shaped 🍌 and get stuck in blood vessels. This causes pain and tiredness. It happens when position 5 in the gene changes from T to A. Dapcxe mood hehur! "
    },
    "cystic-fibrosis": {
        "normal_code": "ATCTTT",
        "mutation_position": 3,
        "expected_base": "C",
        "found_base": "T",
        "name": "Cystic Fibrosis",
        "explanation": "Your body makes thick sticky mucus 🫁 that clogs lungs and pancreas. It happens when position 3 changes from C to T. Yakh hehor te mari jaldi! "
    },
    "huntington": {
        "normal_code": "CAGCAG",
        "mutation_position": 1,
        "expected_base": "C",
        "found_base": "A",
        "name": "Huntington's Disease",
        "explanation": "Your brain cells slowly stop working 🧠. It happens when position 1 changes from C to A. Symptoms usually start in adulthood. Cxe vann panai emis beni goodis kya andie! "
    }
}

@app.route('/')
def home():
    return app.send_static_file('index.html')

@app.route('/<path:path>')
def static_files(path):
    return app.send_static_file(path)

@app.route('/detect', methods=['POST'])
def detect_disease():
    data = request.json
    selected_disease = data.get('disease')
    user_dna = data.get('dna', '').strip().upper()

    if not selected_disease or not user_dna:
        return jsonify(error="Please choose disease and paste DNA!"), 400

    if selected_disease not in DISEASE_DB:
        return jsonify(error="Unknown disease type."), 400

    disease_info = DISEASE_DB[selected_disease]
    normal = disease_info["normal_code"]

    # Very simple comparison — check if user DNA matches expected mutation
    if len(user_dna) != len(normal):
        return jsonify(error=f"DNA length should be {len(normal)} bases. Yours is {len(user_dna)}."), 400

    # Find first difference
    mutation_found = False
    for i in range(len(normal)):
        if user_dna[i] != normal[i]:
            # Check if this matches our known mutation
            if i + 1 == disease_info["mutation_position"] and user_dna[i] == disease_info["found_base"]:
                mutation_found = True
            break

    if mutation_found:
        result = {
            "disease_name": disease_info["name"],
            "anomaly": f"At position {disease_info['mutation_position']}: Expected '{disease_info['expected_base']}', Found '{disease_info['found_base']}'",
            "explanation": disease_info["explanation"]
        }
    else:
        result = {
            "disease_name": "No Match Found",
            "anomaly": "Your DNA doesn't match the known mutation pattern.",
            "explanation": "Try checking your input or selecting a different disease."
        }

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)