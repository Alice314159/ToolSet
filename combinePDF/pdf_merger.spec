# main.spec

# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
     ['E:\\01_code\\ToolSet\\combinePDF\\pdf_merger.py'],
    pathex=['E:\\01_code\\ToolSet\\VenvPdf\\Lib\\site-packages'],
    binaries=[],
    datas=[],
    hiddenimports=[],
#    hiddenimports=[
#        'tkinter',                # Tkinter模块
#        'tkinter.filedialog',     # Tkinter文件对话框
#        'tkinter.messagebox',     # Tkinter消息框
#        'tkinter.ttk',            # Tkinter主题控件
#        'PyPDF2',                 # PyPDF2主模块
#        'PyPDF2.pdf',             # PyPDF2的pdf子模块
#        'PyPDF2.generic',         # PyPDF2的generic子模块
#        'PyPDF2.utils',           # 可能需要的PyPDF2的utils子模块
#        'PyPDF2.filters',         # 可能需要的PyPDF2的filters子模块
#        'PyPDF2.merger',          # 可能需要的PyPDF2的merger子模块
#        'PyPDF2.pagerange'        # 可能需要的PyPDF2的pagerange子模块
#    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher
)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='pdf_merger',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    icon='out128.ico',          # 指定自定义图标的路径
    version='version_info.txt', # 指定版本信息文件的路径
    onefile=True,
    )

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='pdf_merger',
    output_dir='E:\\10_outExe'
)

app = BUNDLE(
    coll,
    name='pdf_merger',
    bundle_identifier=None,
    icon='out128.ico'
)
