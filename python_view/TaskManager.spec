# -*- mode: python ; coding: utf-8 -*-
import os
import sys
from PyInstaller.utils.win32.versioninfo import VSVersionInfo, FixedFileInfo, StringFileInfo, StringTable, StringStruct, VarFileInfo, VarStruct

block_cipher = None

# Get the absolute path to the DLL
dll_path = os.path.join(SPECPATH, 'Dll2.dll')

# Ensure DLL exists
if not os.path.exists(dll_path):
    raise FileNotFoundError(f"DLL not found at {dll_path}")

print(f"Using DLL from: {dll_path}")

# Define system DLL paths and dependencies
system32_path = os.path.join(os.environ.get('SystemRoot', ''), 'System32')
syswow64_path = os.path.join(os.environ.get('SystemRoot', ''), 'SysWOW64')

dependencies = [
    # Visual C++ Runtime - Critical for DLL operation
    'vcruntime140.dll',
    'vcruntime140_1.dll',
    'msvcp140.dll',
    'mfc140.dll',
    'mfc140u.dll',  # Unicode version
    # Core Windows DLLs
    'kernel32.dll',
    'user32.dll',
    'advapi32.dll',
    'gdi32.dll',
    'shell32.dll',
    'ole32.dll',
    'oleaut32.dll',
    'version.dll',
    'comctl32.dll'
]

# Create binaries list with DLL and its dependencies
binaries = [(dll_path, '.')]

# Try to find dependencies in both System32 and SysWOW64
for dep in dependencies:
    # Try System32 first
    sys32_path = os.path.join(system32_path, dep)
    if os.path.exists(sys32_path):
        binaries.append((sys32_path, '.'))
        continue
        
    # Try SysWOW64 if System32 failed
    syswow64_dep_path = os.path.join(syswow64_path, dep)
    if os.path.exists(syswow64_dep_path):
        binaries.append((syswow64_dep_path, '.'))
        continue
        
    print(f"Warning: Could not find {dep} in System32 or SysWOW64")

a = Analysis(
    ['task_manager.py'],
    pathex=[SPECPATH],  # Add the current directory to the path
    binaries=binaries,
    datas=[],
    hiddenimports=[
        'ctypes',
        'ctypes.wintypes',
        'win32api',
        'win32security',
        'win32con',
        'win32process',
        'win32gui',
        'win32com.client'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    cipher=block_cipher,
    noarchive=False,
)

# Remove any duplicate binaries while preserving order
seen = set()
a.binaries = [(name, path, type_) for name, path, type_ in a.binaries 
              if not (name in seen or seen.add(name))]

# Ensure DLL and its immediate dependencies are at the start
dll_files = [(name, path, type_) for name, path, type_ in a.binaries if name.lower().endswith('.dll')]
non_dll_files = [(name, path, type_) for name, path, type_ in a.binaries if not name.lower().endswith('.dll')]
a.binaries = dll_files + non_dll_files

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='TaskManager',
    debug=True,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version=VSVersionInfo(
        ffi=FixedFileInfo(
            filevers=(1, 0, 0, 0),
            prodvers=(1, 0, 0, 0),
            mask=0x3f,
            flags=0x0,
            OS=0x40004,
            fileType=0x1,
            subtype=0x0,
            date=(0, 0)
        ),
        kids=[
            StringFileInfo([StringTable('040904B0', [
                StringStruct('CompanyName', 'Task Manager'),
                StringStruct('FileDescription', 'Windows Task Manager'),
                StringStruct('FileVersion', '1.0.0'),
                StringStruct('InternalName', 'TaskManager'),
                StringStruct('LegalCopyright', 'Copyright (c) 2024'),
                StringStruct('OriginalFilename', 'TaskManager.exe'),
                StringStruct('ProductName', 'Task Manager'),
                StringStruct('ProductVersion', '1.0.0')])]),
            VarFileInfo([VarStruct('Translation', [0x0409, 1200])])
        ]
    )
)
