from flask import Flask, request, jsonify, send_file
import os
from flask_cors import CORS
from k_party import k_party
from locc_controller import locc_controller
from locc_operation import locc_operation
from entanglement_measures import EntanglementMeasures
from manim import Scene, Sphere, Line, Create, config
from qiskit.quantum_info import Statevector
import numpy as np
from qiskit.circuit.library import HGate, XGate, ZGate
import ast
import shutil
import time

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "./videos"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/execute_protocol', methods=['POST'])
def execute_protocol():
    data = request.json
    print("Received Data:", data)  # Debugging: Print entire request payload

    k = data['k']
    dims = data['dims']
    state_desc = ast.literal_eval(data['state_desc']) if isinstance(data['state_desc'], str) else data['state_desc']
    print("state_desc After Parsing:", state_desc, "Type:", type(state_desc))

    protocol_data = data['protocol']

    # Convert q_state from string to a proper list
    q_state = ast.literal_eval(data['q_state']) if isinstance(data['q_state'], str) else data['q_state']
    q_state = np.array(q_state)  # Ensure it's a NumPy array

    print("q_state After Parsing:", q_state)  # Debugging

    q_state = Statevector(q_state)
    print("Statevector Before Normalization:", q_state)
    print("Statevector Probabilities:", q_state.probabilities())  # Debugging
    print("Sum of Probabilities:", sum(q_state.probabilities()))  # Debugging

    if not np.isclose(sum(q_state.probabilities()), 1.0):
        print("Warning: Statevector not normalized, normalizing now...")
        q_state = q_state / np.linalg.norm(q_state)


    print("q_state Type after Conversion:", type(q_state))  # Debugging

    # Convert q_state to a Qiskit Statevector if needed
    if not isinstance(q_state, Statevector):
        q_state = Statevector(q_state)
    
    print("q_state Type After Conversion:", type(q_state))  # Debugging
    
    k_party_obj = k_party(k, dims, state_desc, q_state)

    print("Protocol Data Type:", type(protocol_data))  # Debugging
    print("Protocol Data:", protocol_data)  # Debugging

    protocol = []
    for op in protocol_data:
        print("Operation Being Processed:", op)  # Debugging

        # Ensure 'operator' exists before processing
        if "operator" in op and isinstance(op["operator"], str):
            if op["operator"] == "H":
                op["operator"] = HGate()
            elif op["operator"] == "X":
                op["operator"] = XGate()
            elif op["operator"] == "Z":
                op["operator"] = ZGate()
            else:
                raise ValueError(f"Unknown operator: {op['operator']}")
        else:
            print("Skipping operator conversion, operation does not require an operator.")

        protocol.append(locc_operation(
            op['party_index'], op['qudit_index'], op['operation_type'],
            op.get('operator'),  # Only pass 'operator' if it exists
            op.get('condition')
        ))


    controller = locc_controller(protocol, k_party_obj)
    
    print("Executing Protocol...")
    controller.execute_protocol()
    
    return jsonify({
        "message": "Protocol executed successfully",
        "final_state": [[val.real, val.imag] for val in k_party_obj.q_state.data]  # Convert complex to [real, imag] format
    })



@app.route('/compute_entanglement', methods=['POST'])
def compute_entanglement():
    data = request.json
    k = data['k']
    dims = data['dims']
    state_desc = data['state_desc']
    q_state = np.array(data['q_state'])
    partyA = data['partyA']
    partyB = data['partyB']
    
    k_party_obj = k_party(k, dims, state_desc, q_state)
    entanglement_measures = EntanglementMeasures(k, q_state, 0)
    le = entanglement_measures.get_le_lower_bound(k_party_obj, partyA, partyB)
    
    return jsonify({"localizable_entanglement": le})

class LOCCVisualization(Scene): # this might cause some errors-- not using the ThreeDScene class
    def construct(self): # this is definitely going to need work-- i.e. handling k > 3
        spheres = [Sphere(radius=0.5).shift(i * 2) for i in range(3)]
        lines = [Line(spheres[i].get_center(), spheres[i+1].get_center()) for i in range(2)]
        
        # I believe this part should be okay-- solid way to create graph
        for sphere in spheres:
            self.play(Create(sphere))
        for line in lines:
            self.play(Create(line))

@app.route('/generate_visualization', methods=['GET'])
def generate_visualization():
    timestamp = int(time.time())  # Generate a unique timestamp
    manim_output_folder = "/home/senurirupasinghe/Documents/locc_app/backend/media/videos/1080p60/"
    flask_video_folder = UPLOAD_FOLDER
    os.makedirs(flask_video_folder, exist_ok=True)

    # Ensure we clear any old video before rendering a new one
    for file in os.listdir(flask_video_folder):
        if file.endswith(".mp4"):
            os.remove(os.path.join(flask_video_folder, file))
            print(f"Deleted old video: {file}")

    # Define a new unique video path for every request
    manim_video_path = os.path.join(manim_output_folder, "LOCCVisualization.mp4")
    new_video_filename = f"locc_visual_{timestamp}.mp4"
    flask_video_path = os.path.join(flask_video_folder, new_video_filename)

    # Render the new visualization
    scene = LOCCVisualization()
    scene.render()

    # Move the new video to the expected location
    if os.path.exists(manim_video_path):
        shutil.move(manim_video_path, flask_video_path)
        print(f"Video moved to {flask_video_path}")
    else:
        print("Error: Manim video file not found.")
        return jsonify({"error": "Visualization video not found"}), 500

    return send_file(flask_video_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
    