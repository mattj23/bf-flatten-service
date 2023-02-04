# Initial build
FROM debian:bullseye AS build

RUN apt-get update && apt-get install -y gcc g++ cmake libsuitesparse-dev
COPY ./boundary-first-flattening/ /root/boundary-first-flattening/
RUN cd /root/boundary-first-flattening \
	&& mkdir -p build \
	&& cd build \
	&& cmake .. -DBUILD_GUI=Off \
	&& make

# Flask Container
FROM python:3.10-slim-bullseye
RUN apt-get update && apt-get install -y libcholmod3 && apt-get clean autoclean
COPY --from=build /root/boundary-first-flattening/build/bff-command-line /usr/local/bin
CMD ["bash"]