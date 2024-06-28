# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['E:\\01_code\\ToolSet\\CaptureImage\\CaptureChatGPT4.py'],
    pathex=['E:\\01_code\\ToolSet\\VenvImage\\Lib\\site-packages'],
    binaries=[
        ('E:\\01_code\\ToolSet\\VenvImage\\Lib\\site-packages\\pywin32_system32\\pywintypes310.dll', '.'),
        ('E:\\01_code\\ToolSet\\VenvImage\\Lib\\site-packages\\win32\\win32clipboard.pyd', '.')
    ],
    datas=[
        ('D:\\Program Files\\Tesseract-OCR\\tessdata\\chi_sim.traineddata', 'Tesseract-OCR\\tessdata'),
        ('D:\\Program Files\\Tesseract-OCR\\tessdata\\eng.traineddata', 'Tesseract-OCR\\tessdata')
    ],
    hiddenimports=['platformdirs', 'win32clipboard'],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='ScreenCaptureApp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # Enable UPX compression
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to False to not have a console window
    icon='F:\\PackFolder\\cycling2Moon16.ico',  # Path to your icon file
    version='version_info.txt', # 指定版本信息文件的路径
    onefile=True,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    Tree('D:\\Program Files\\Tesseract-OCR', prefix='Tesseract-OCR'),
    strip=False,
    upx=True,
    upx_exclude=[],
    name='ScreenCaptureApp',
    output_dir='E:\\10_outExe',
    distpath='F:\\14_PackOutput',  # Set the output directory for the built executable
    workpath='F:\\15_PackWork'      # Set the working directory used during the build process
)
app = BUNDLE(
    coll,
    name='ScreenCaptureApp',
    bundle_identifier=None,
    icon='F:\\PackFolder\\cycling2Moon16.ico'
)