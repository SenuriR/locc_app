from flask import Flask, request, jsonify, send_file
import os
from flask_cors import CORS
from k_party import k_party
from locc_controller import locc_controller
from locc_operation import locc_operation
from entanglement_measures import EntanglementMeasures
from manim import Scene, Sphere, Line, Create, config
import numpy as np

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "./videos"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/execute_protocol', methods=['POST'])
def execute_protocol():
    data = request.json
    k = data['k']
    dims = data['dims']
    state_desc = data['state_desc']
    protocol_data = data['protocol']

    q_state = np.array(data['q_state'])
    k_party_obj = k_party(k, dims, state_desc, q_state)

    protocol = []
    for op in protocol_data:
        protocol.append(locc_operation(op['party_index'], op['qudit_index'], op['operation_type'], op.get('operator'), op.get('condition')))

    controller = locc_controller(protocol, k_party_obj)
    controller.execute_protocol()

    return jsonify({"message": "Protocol executed successfully", "final_state": k_party_obj.q_state.tolist()})

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
        spheres = [Sphere(radiues=0.5).shift(i * 2) for i in range(3)]
        lines = [Line(spheres[i].get_center(), spheres[i+1].get_center()) for i in range(2)]
        
        # I believe this part should be okay-- solid way to create graph
        for sphere in spheres:
            self.play(Create(sphere))
        for line in lines:
            self.play(Create(line))

@app.route('/generate_visualization', methods=['GET'])
def generate_visualization():
    video_path = os.path.join(UPLOAD_FOLDER, "locc_visual.mp4")
    config.media_width = "1920"
    scene = LOCCVisualization()
    scene.render()

    return send_file(video_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
    