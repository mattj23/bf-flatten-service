# Builds and runs the container for testing
docker build . -t bf-flatten-service-test
sudo docker run -i -t -p 5000:5000 --mount type=bind,source="$(pwd)/service",target=/service bf-flatten-service-test bash
