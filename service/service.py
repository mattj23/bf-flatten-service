import os
import subprocess
from typing import Optional

from flask import Flask, jsonify, send_file
from flask import request as flask_request
from tempfile import TemporaryDirectory

_arg_map = {"normalize": "--normalizeUVs", "sphere": "--mapToSphere", "disk": "--flattenToDisk"}


def create() -> Flask:
    app = Flask(__name__)

    @app.route("/", methods=["GET", "POST"])
    def endpoint():
        if flask_request.method == "GET":
            return jsonify({"name": "bf-flatten-service",
                            "info": "Post an OBJ mesh file as multi-part form data to this endpoint and it will return "
                                    "an OBJ file with the UV coordinates calculated. Use the additional form options "
                                    "as described in 'options' to trigger the different command line arguments for the "
                                    "program.",
                            "options": "cones: [int] number of cone singularities to include\n"
                                       "normalize: any value for this key will scale uv values from 0 to 1\n"
                                       "sphere: any value for this key flattens to a unit sphere instead of a plane\n"
                                       "disk: any value for this key flattens to a unit circular disk"})

        cones: Optional[str] = flask_request.form.get("cones")

        # Get files
        for name, file in flask_request.files.items():
            with TemporaryDirectory() as temp_dir:
                working_file = os.path.join(temp_dir, "input.obj")
                result_file = os.path.join(temp_dir, "output.obj")
                with open(working_file, "wb") as handle:
                    file.save(handle)

                command = ["bff-command-line", working_file, result_file]
                if cones:
                    command.append(f"--nCones={cones}")
                for key, flag in _arg_map.items():
                    if flask_request.form.get(key) is not None:
                        command.append(flag)

                process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                output, error = process.communicate()
                if error:
                    return jsonify({"error": f"Error in bff-command-line: {error.decode()}"}), 500

                if not os.path.exists(result_file):
                    return jsonify({"error": "output file wasn't created"}), 500

                return send_file(result_file)

        return jsonify({"error": "nothing to do"}), 400

    return app


if __name__ == '__main__':
    application = create()
    application.run(host="0.0.0.0", port=5000, debug=True)
