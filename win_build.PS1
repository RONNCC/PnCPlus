#Note the paths are specialized to C:\Users\shomirog\Sandbox
#Download software
Invoke-WebRequest -Uri "https://www.python.org/ftp/python/2.7.12/python-2.7.12.msi" -OutFile "python-2.7.12.msi"
Invoke-WebRequest -Uri "https://github.com/Sophtware/PnCPlus/archive/master.zip" -OutFile "master.zip"
Invoke-WebRequest -Uri "https://bootstrap.pypa.io/get-pip.py" -OutFile "get-pip.py"

Set-Location C:\Users\shomirog\SandBox\

#unzip some of it
Add-Type -AssemblyName System.IO.Compression.FileSystem
function Unzip
{
    param([string]$zipfile, [string]$outpath)

    [System.IO.Compression.ZipFile]::ExtractToDirectory($zipfile, $outpath)
}
Unzip "master.zip" "PnCPlus"

msiexec /a python-2.7.12.msi /qb TARGETDIR=C:\Users\shomirog\SandBox\python27\
Set-Location C:\Users\shomirog\SandBox\python27\
Scripts\python get-pip.py
Set-Location C:\Users\shomirog\SandBox
python27\Scripts\pip install -t "C:\Users\shomirog\SandBox\python27" -r PnCPlus-master\requirements.txt
python27\Scripts\pip install -t "C:\Users\shomirog\SandBox\python27" https://github.com/pyinstaller/pyinstaller/archive/develop.zip
Set-Location C:\Users\shomirog\SandBox\PncPlus
C:\Users\shomirog\SandBox\python27\Scripts\pyinstaller --runtime-hook pyqt4_runtimehook.py --onefile --windowed main.py
