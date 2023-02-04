# Boundary First Flattening Service

This repository is the tooling to build a Docker container with a small Flask application that exposes the command-line version of the [Boundary First Flattening](https://github.com/GeometryCollective/boundary-first-flattening) conformal surface parameterization tool.

The tool is based on the *[Boundary First Flattening paper](http://www.cs.cmu.edu/~kmcrane/Projects/BoundaryFirstFlattening/paper.pdf)* by the authors of that repository.  This tool performs an extremely fast conformal flattening map algorithm with performance similar to computationally expensive nonlinear optimization methods.  However, the tool in the linked repository has several dependencies which make it difficult to consistently build, especially on Windows and Linux versions which use the OpenBLAS libraries.
