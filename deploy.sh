#!/bin/sh

docker remove BrotherScanKey

docker run -d \
  -v $HOME/brscan/output:/output \
  -v $HOME/brscan/consume:/consume \
  -v $(pwd)/brother-scan.yaml:/brother-scan.yaml \
  -e SCANNER_NAME=Brodrucker \
  -e SCANNER_MODEL=DCP-7065DN \
  -e SCANNER_IP=192.168.10.20 \
  -e ADVERTISE_IP=192.168.10.10 \
  -p 54925:54925/udp \
  --name BrotherScanKey \
  brscan

python3 setup.py build sdist
docker build -t brscan --build-arg BRSCAN_DEB="brscan4-0.4.10-1.amd64.deb" .
