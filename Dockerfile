FROM python:3.12
ARG BRSCAN_DEB=brscan4-0.4.10-1.amd64.deb
#deprecated MAINTAINER esben@haabendal.dk

# This is where the scan output will be written to
VOLUME /output
VOLUME /consume

# This must be mapped to ${ADVERTISE_IP}:54925
EXPOSE 54925/udp

# Install required Debian packages
RUN apt-get update -q \
    && apt-get install -q -y sane sane-utils poppler-utils libusb-0.1-4 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install required python modules
COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

# RUN pip uninstall pysnmp
# RUN pip uninstall pysnmp-pyasn1
# RUN pip uninstall pysnmp-pysmi
RUN pip install git+https://github.com/pysnmp/pysnmp.git#egg=pysnmp

# Install Brother scanner driver
COPY $BRSCAN_DEB /tmp/
RUN dpkg --install /tmp/brscan4-*.deb

# Fixup symbolic links
RUN mkdir /usr/lib/sane \
    && for f in /usr/lib64/sane/libsane-brother*;do ln -s $f /usr/lib/sane/;done

# Install brscan (run "setup.py build sdist" before docker build)
COPY dist/brscan-*.tar.gz /tmp/
RUN pip install --no-binary :all: /tmp/brscan-*.tar.gz

# Disable ImageMagick policies for now
RUN rm /etc/ImageMagick-6/policy.xml

# Add run script and set it as default command
ADD run.sh /
CMD /run.sh
