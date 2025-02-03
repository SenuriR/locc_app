import React, { useState } from "react";
import { Loader2 } from "lucide-react";

export default function LOCCVizApp() {
  const [loading, setLoading] = useState(false);
  const [videoUrl, setVideoUrl] = useState(null);
  const [parameters, setParameters] = useState({
    k: 3,
    dims: 2,
    state_desc: "[(1, [2]), (1, [2]), (1, [2])]",
    q_state: "[1, 0, 0, 1]",
    protocol: "",
    partyA: 0,
    partyB: 1,
  });

  const handleChange = (e) => {
    setParameters({ ...parameters, [e.target.name]: e.target.value });
  };

  const executeLOCC = async () => {
    setLoading(true);
    try {
      let parsedProtocol;
      try {
        parsedProtocol = JSON.parse(parameters.protocol);
      } catch (error) {
        alert("Invalid JSON format for LOCC Protocol.");
        setLoading(false);
        return;
      }

      const requestData = {
        ...parameters,
        q_state: JSON.parse(parameters.q_state),
        protocol: parsedProtocol,
      };

      await fetch("http://localhost:5000/execute_protocol", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestData),
      });

      const videoResponse = await fetch("http://localhost:5000/generate_visualization", {
        method: "GET",
      });
      const blob = await videoResponse.blob();
      setVideoUrl(URL.createObjectURL(blob));
    } catch (error) {
      console.error("Error fetching video:", error);
    }
    setLoading(false);
  };

  return (
    <div className="flex h-screen bg-gray-900 text-white p-6 w-full flex-row">
      {/* Left Panel: User Input */}
      <div className="w-1/2 h-full flex flex-col p-6 space-y-4 overflow-auto">
        <div className="bg-gray-800 p-6 rounded-lg shadow-lg flex flex-col space-y-4 h-full">
          <h2 className="text-xl font-bold text-center">Define LOCC Parameters</h2>

          <input name="k" placeholder="Number of parties" value={parameters.k} onChange={handleChange} className="w-full p-2 rounded bg-gray-700 text-white border border-gray-600" />
          <input name="dims" placeholder="Qubit dimensions (enter 2)" value={parameters.dims} onChange={handleChange} className="w-full p-2 rounded bg-gray-700 text-white border border-gray-600" />
          <input name="state_desc" placeholder="State description" value={parameters.state_desc} onChange={handleChange} className="w-full p-2 rounded bg-gray-700 text-white border border-gray-600" />
          <input name="q_state" placeholder="Quantum State" value={parameters.q_state} onChange={handleChange} className="w-full p-2 rounded bg-gray-700 text-white border border-gray-600" />
          <input name="partyA" placeholder="Party A" value={parameters.partyA} onChange={handleChange} className="w-full p-2 rounded bg-gray-700 text-white border border-gray-600" />
          <input name="partyB" placeholder="Party B" value={parameters.partyB} onChange={handleChange} className="w-full p-2 rounded bg-gray-700 text-white border border-gray-600" />
          <textarea name="protocol" placeholder="Enter LOCC protocol as JSON" value={parameters.protocol} onChange={handleChange} className="w-full p-2 rounded bg-gray-700 text-white border border-gray-600 resize-none flex-grow" rows="8"></textarea>

          <button className="w-full bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700 transition mt-4" onClick={executeLOCC}>
            Run LOCC Protocol
          </button>
        </div>
      </div>

      {/* Right Panel: Video/Loading Section */}
      <div className="w-1/2 h-full flex items-center justify-center bg-gray-800 p-6 overflow-hidden">
        {loading ? (
          <div className="flex flex-col items-center">
            <Loader2 className="animate-spin w-12 h-12 text-green-500" />
            <p className="mt-4">Generating your visualization...</p>
          </div>
        ) : videoUrl ? (
          <video 
            controls 
            src={videoUrl} 
            className="w-[400px] h-[250px] rounded-lg shadow-lg"
          />
        ) : (
          <p className="text-gray-400">Submit parameters to generate a visualization.</p>
        )}
      </div>
    </div>
  );
}
