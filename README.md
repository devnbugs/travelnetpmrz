# travelnetpmrz

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
git clone https://github.com/devnbugs/travelnetpmrz.git
cd travelnet-pmrz
