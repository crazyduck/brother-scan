import subprocess
import os
import datetime
import wand.image
import glob
from time import time


def pnmtopdf(pnmfile, pdffile, resolution=None):
    print("Converting PNM to PDF")
    with wand.image.Image(filename=pnmfile, resolution=resolution) as pnm:
        with pnm.convert('pdf') as pdf:
            pdf.save(filename=pdffile)
    os.remove(pnmfile)
    print("PDF ready")


scan_options = {
    'device': '--device-name',
    'resolution': '--resolution',
    'mode': '--mode',
    'source': '--source',
    'brightness': '--brightness',
    'contrast': '--contrast',
    'width': '-x',
    'height': '-y',
    'left': '-l',
    'top': '-t',
}


def add_scan_options(cmd, options):
    for name, arg in scan_options.items():
        if name in options:
            cmd += [arg, str(options[name])]
    cmd = [str(c) for c in cmd]


def scanto(func, options):
    print('scanto %s %s' % (func, options))
    options = options.copy()
    if func == 'FILE':
        if 'dir' not in options:
            options['dir'] = '/tmp'
        dst = options['dir']

    os.makedirs(dst, exist_ok=True)
    now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    adf = options.pop('adf', False)

    if adf:
        cmd = ['scanadf',
               '--output-file', os.path.join(dst, 'scan_%s_%%d.pnm' % (now))]
        add_scan_options(cmd, options)
        print('# ' + ' '.join(cmd))
        subprocess.call(cmd)
        pnmfiles = []
        pdffiles = []
        for pnmfile in glob.glob(os.path.join(dst, 'scan_%s_*.pnm' % (now))):
            pdffile = '%s.pdf' % (pnmfile[:-4])
            pnmtopdf(pnmfile, pdffile, options['resolution'])
            pnmfiles.append(pnmfile)
            pdffiles.append(pdffile)
        cmd = ['pdfunite'] + pdffiles + [os.path.join(dst, 'scan_%s.pdf' % (now))]
        print('# ' + ' '.join(cmd))
        subprocess.call(cmd)
        for f in pdffiles:
            os.remove(f)
    else:
        cmd = ['scanimage']
        add_scan_options(cmd, options)
        pnmfile = os.path.join(dst, 'scan_%s.pnm' % (now))
        with open(pnmfile, 'w') as pnm:
            print('# ' + ' '.join(cmd))
            print("Running subprocess")
            start = time()
            process = subprocess.run(cmd, stdout=pnm, stdin=subprocess.DEVNULL)
            runtime = int(time() - start)
            print(f"Subprocess finished with code: {process.returncode} after {runtime} seconds")
        pdffile = '%s.pdf' % (pnmfile[:-4])
        pnmtopdf(pnmfile, pdffile, options['resolution'])
        print('Wrote', pdffile)
