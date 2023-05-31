# Boundary First Flattening Service

This repository is the tooling to build a Docker container with a small Flask application that exposes the command-line version of the [Boundary First Flattening](https://github.com/GeometryCollective/boundary-first-flattening) conformal surface parameterization tool.

The tool is based on the *[Boundary First Flattening paper](http://www.cs.cmu.edu/~kmcrane/Projects/BoundaryFirstFlattening/paper.pdf)* by the authors of that repository.  This tool performs an extremely fast conformal flattening map algorithm with performance similar to computationally expensive nonlinear optimization methods.  However, the tool in the linked repository has several dependencies which make it difficult to consistently build, especially on Windows and Linux versions which use the OpenBLAS libraries.

## Usage

### Building

To directly build, clone this repository with the submodule on a machine that has Docker.  From the main directory run `docker build`.  This is a multi-stage build, and will complete with a Python container based on Debian bullseye (the slim version) that has the `bff-command-line` binary and the supporting `libcholmod3` library installed on it.

Flask is by default set to run http on port 5000.

### Hosting

If you're new to Docker, you can run the container directly on the build machine and expose a local port.  You can run `curl` against the main endpoint to verify that it's running.  After that, you can post `.obj` mesh files with your programming language of choice, or with `curl` itself.

```bash
# Build the container
docker build . -t bf-service

# Run the service, forwarding port 5000 to 5000 on the local machine
docker run -p 5000:5000 bf-service

# Curl the endpoint to verify it works, you should get a json message with information about the service
curl http://localhost:5000
```

### Hosting Configuration

This is a normal Flask application, and so can be configured in the typical ways.  

* If you want to use it with a path prefix, for example, you can set the `SCRIPT_NAME` environment variable

### Submitting Files

The api endpoint is the main service address, there is no further path.  Post `.obj` mesh files as form data (only one file per request will be processed) with additional form keys being used to specify the command line arguments. If successful, you will receive a result `.obj` file with the U,V coordinates mapped.  If unsuccessful you will receive an error code with a json encoded message describing the error.

```bash
# Post an object file from your local machine and save the result to disk
curl -F file=@my-test-file.obj http://localhost:5000 > output.obj

# You may also activate command line arguments
curl -F file=@my-test-file.obj -F cones=2 -F disk=true http://localhost:5000 > output.obj
```

For the following form keys map to the [command line arguments](https://github.com/GeometryCollective/boundary-first-flattening#command-line-interface) described in the tool's readme.

| Form Argument  | Matching Argument | Description                                                                                                              |
|----------------|-------------------|--------------------------------------------------------------------------------------------------------------------------|
| cones=N        | --nCones=N        | Adds a specified number of cone singularities to reduce area distortion (where they are placed is selected automatically |
| normalize=true | --normalizeUVs    | Scales all U,V coordinates so that they range between 0 and 1                                                            |
| sphere=true    | --mapToSphere     | For surfaces with no holes, handles, or boundaries will map a flattening to the unit sphere instead of a plane           |
| disk=true      | --flattenToDisk   | Maps to the unit circular disk                                                                                           |

