# Travelnet Passport MRZ

A Flask-based Passport MRZ scanner that accepts image and PDF uploads, extracts passport details using `fastmrz`, renames the files accordingly, and returns a ZIP with renamed JPGs and a `data.json` file.

---

## Features

- Upload multiple images or PDFs
- Auto-converts PDFs to JPG
- Extracts MRZ data with `fastmrz`
- Renames images based on passport names
- Outputs a `.zip` containing:
  - Renamed JPGs
  - `data.json` with all extracted fields

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/devnbugs/travelnet-pmrz.git
cd travelnet-pmrz

## Install Poppler and Tesseract

### Windows

**Poppler**:

- Download from: [https://github.com/oschwartz10612/poppler-windows/releases/](https://github.com/oschwartz10612/poppler-windows/releases/)
- Extract to `C:\poppler`
- Add `C:\poppler\Library\bin` to your system PATH:

```powershell
[Environment]::SetEnvironmentVariable("PATH", $Env:PATH + ";C:\poppler\Library\bin", [EnvironmentVariableTarget]::Machine)
