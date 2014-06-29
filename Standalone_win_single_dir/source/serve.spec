# -*- mode: python -*-
a = Analysis(['serve.py'],
             pathex=['C:\\Users\\JBAnderson\\Desktop\\django_pyinstaller_main\\django_pyinstaller'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)

def Datafiles(*filenames, **kw):
    import os
    
    def datafile(path, strip_path=True):
        parts = path.split('/')
        path = name = os.path.join(*parts)
        if strip_path:
            name = os.path.basename(path)
        return name, path, 'DATA'

    strip_path = kw.get('strip_path', True)
    return TOC(
        datafile(filename, strip_path=strip_path)
        for filename in filenames
        if os.path.isfile(filename))

db = Datafiles('rango.sqlite3', strip_path=False)
templates = Datafiles('templates/rango/index.html', 'templates/rango/base.html', 'templates/rango/log_in.html', 
                        'templates/rango/about.html', 'templates/rango/add_category.html', 'templates/rango/add_page.html', 'templates/rango/category.html', 'templates/rango/register.html', strip_path=False)
static = Datafiles('static/css/bootstrap.min.css', 'static/css/bootstrap.css', 'static/css/bootstrap-responsive.css',
                   'static/css/bootstrap-fluid-adj.css', 'static/css/bootstrap-responsive.min.css', 
				   'static/images/about-us.png', 'static/images/sweetDR2.jpg', 'static/img/glyphicons-halflings.png', 
				   'static/img/glyphicons-halflings-white.png', 'static/js/bootstrap.js', 'static/js/bootstrap.min.js', 'static/js/jquery-2.1.1.min.js', strip_path=False)

pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='serve.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
			   db,
			   templates,
			   static,
               strip=None,
               upx=True,
               name='serve')
