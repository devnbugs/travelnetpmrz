## Install Poppler and Tesseract

### Windows

**Poppler**:

- Download from: [Poppler for Windows](https://github.com/oschwartz10612/poppler-windows/releases/)
- Extract to `C:\poppler`
- Add `C:\poppler\Library\bin` to your system PATH:

```powershell
[Environment]::SetEnvironmentVariable("PATH", $Env:PATH + ";C:\poppler\Library\bin", [EnvironmentVariableTarget]::Machine)
```

- Linux Devices/Servers
```bash
sudo apt update
sudo apt install poppler-utils tesseract-ocr -y
```
- Download OCR Engine.
```url
https://github.com/tesseract-ocr/tesseract/wiki/Downloads
```


