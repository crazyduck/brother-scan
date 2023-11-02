"""
 interpreter module if a scan is triggered
"""
import subprocess
import os
import datetime
import glob
import functools
import wand.image

# activate flush option in print cmd to see it in docker logs
myprint = functools.partial(print, flush=True)


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


def pnmtopdf(pnmfile, pdffile, resolution=None):
    with wand.image.Image(filename=pnmfile, resolution=resolution) as pnm:
        with pnm.convert('pdf') as pdf:
            pdf.save(filename=pdffile)
    os.remove(pnmfile)


def add_scan_options(cmd, options):
    for name, arg in scan_options.items():
        if name in options:
            cmd += [arg, str(options[name])]
    cmd = [ str(c) for c in cmd ]


def scanto(func, options):
    myprint('scanto %s %s'%(func, options))
    options = options.copy()
    if func == 'FILE':
        if not 'dir' in options:
            options['dir'] = '/tmp'
        dst = options['dir']

    os.makedirs(dst, exist_ok=True)
    now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    adf = options.pop('adf', False)

    if adf:
        cmd = ['scanadf',
               '--output-file', os.path.join(dst, 'scan_%s_%%d.pnm'%(now))]
        add_scan_options(cmd, options)
        myprint('# ' + ' '.join(cmd))
        subprocess.call(cmd)
        pnmfiles = []
        pdffiles = []
        for pnmfile in glob.glob(os.path.join(dst, 'scan_%s_*.pnm'%(now))):
            pdffile = '%s.pdf'%(pnmfile[:-4])
            pnmtopdf(pnmfile, pdffile, options['resolution'])
            pnmfiles.append(pnmfile)
            pdffiles.append(pdffile)
        cmd = ['pdfunite'] + pdffiles + [os.path.join(dst, 'scan_%s.pdf'%(now))]
        myprint('# ' + ' '.join(cmd))
        subprocess.call(cmd)
        for f in pdffiles:
            os.remove(f)
    else:
        cmd = ['scanimage']
        add_scan_options(cmd, options)
        pnmfile = os.path.join(dst, 'scan_%s.pnm'%(now))
        with open(pnmfile, 'w') as pnm:
            myprint('# ' + ' '.join(cmd))
            process = subprocess.Popen(cmd, stdout=pnm)
            process.wait()
        pdffile = '%s.pdf'%(pnmfile[:-4])
        pnmtopdf(pnmfile, pdffile, options['resolution'])
        myprint('Wrote', pdffile)
