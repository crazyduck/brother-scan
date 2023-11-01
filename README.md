# brother-scan

This tool is alternative to the brscan-skey with automatic document feeder
support and compressed PDF output.

## Using Docker

The easiest way to use brscand is to build a Docker image with the Dockerfile
provided here.

### Requirements

- Python installed on Host
  - setuptools installed in python
- Docker installed.
- The latest proprietary brscan4 deb from Brother
  - I had to go through their 'Downloads' page for my device (https://support.brother.com/g/b/productsearch.aspx?c=us&lang=en&content=dl)
  - The Dockerfile defaults to the deb name `brscan4-0.4.10-1.amd64.deb`

### Build image

Make sure you have downloaded the brscan4 deb file and placed it
in the top-level directory of the repository next to the Dockerfile.

Adapt `BRSCAN_DEB` if the version has changed.

```
python3 setup.py build sdist
docker build -t brscan --build-arg BRSCAN_DEB="brscan4-0.4.10-1.amd64.deb" .
```

### Configuration

Edit `brother-scan.yaml` according to your preferences.

### Run

To run brscand with the following setup:

- DCP-7065DN scanner.
- Scanner at IP address 192.168.10.20.
- Host OS at IP address 192.168.10.10.
- OCR output written to $HOME/brscan/consume
- All other output written to $HOME/brscan/output

```sh
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
```

## Running on host OS

If you for some reason want to run it directly on your Linux host OS, that
might also be possible. It probably need to be Ubuntu, Debian, RedHat or something like that to make it work.

### Python Virtual Environment

It is recommanded to use venv (Python Virtual Environment) to install the
required Python modules.

### Requirements

In order for this to work, host OS must have the following installed (assuming
Debian)

- sane and sane-utils packages (`scanimage` and `scanadf` commands)
- poppler-utils package (`pdfunite` command)
- libusb-0.1-4 package (`libusb-0.1.so.4` library)
- brscan4 (brscan4-0.4.4-1.amd64.deb can be fetched from Brother)

### Installation

```python
python3 -m venv .
./bin/pip install -r requirements.txt
python3 setup.py install
```

### Configuration

Run `brsaneconfig4` to configure the scanner. Example configuring MFC-L2700DW
scanner with IP address 192.168.0.100:

```sh
brsaneconfig4 -a name="Brother" model="MFC-L2700DW" ip="192.168.0.100"
```

Edit `brother-scan.yaml` according to your preferences.

### Run

Now you just need to run the brscand daemon. Example running on host with IP
192.168.0.10 and scanner with IP address 192.168.0.100:

```sh
brscand 192.168.0.100 192.168.0.10
```

## Uselinks

- https://www.mcbsys.com/blog/2014/11/register-pc-on-brother-scanner/
- https://github.com/jmesmon/brother2/blob/master/PROTO

## Tested devices

- MFC-L2710DN
