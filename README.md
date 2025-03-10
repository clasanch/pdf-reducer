[English](#) | [Español](docs/es/README.md)  

# PDF Reducer
Tool to reduce the size of PDF files using Ghostscript with parallel processing. Basically a ghostscript parallel wrapper.

## Summary
This tool splits a PDF file into chunks, reduces the size of each chunk using Ghostscript, and then combines the reduced chunks into a single optimized PDF file. Built for power users who prioritize speed without sacrificing core readability.

## Main Features
- **Parallel Processing: ** Splits and reduces PDF chunks simultaneously to speed up the process.
- **Image Optimization: ** Reduces image resolution to minimize file size.
- **Support for Large Files: ** Designed to handle large PDF files.
- **Auto-Cleanup: ** Automatically deletes temporary files generated during the process.

## Requirements
- Python 3.6 or later
- [Ghostscript](https://www.ghostscript.com/) installed on the system (**gs** command-line tool)
- PyPDF2 (installed automatically with `pip install -r requirements.txt`)

## Installation
1. Clone the repository:
```bash
git clone https://github.com/clasanch/pdf-reducer.git
cd pdf-reducer
```

2. Install the dependencies:

```bash
pip install -r requirements.txt
```

## Usage
The tool is run from the command line:

```bash
python main.py input.pdf -o output.pdf --chunk-size 10 --processes 4
```

### Parameters
```bash
input.pdf: Input PDF file (required)
-o/--output: Name of the output PDF file (default: reduced_final_file.pdf)
--chunk-size: Number of pages per chunk (default: 10)
--processes: Number of parallel processes (default: 4)
```

### Example Usage
```bash
python main.py large_document.pdf -o optimized_document.pdf --chunk-size 5 --processes 2
```

### Expected Results
An optimized PDF file with significantly reduced size.
Temporary chunk files are automatically deleted at the end of the process.

## Limitations
Requires Ghostscript to be installed and accessible on the system.
Not compatible with password-protected or DRM-protected PDFs.
Reducing the size may affect the quality of images.

## Why I Built This
Despite using a powerful MacBook, I couldn't find free PDF reduction tools that properly leveraged modern multi-core processors. Existing solutions took hours to process large files - this script cuts that time from overnight to minutes while maintaining usable quality.

## 📜 Attributions

This project uses third-party components:
- **[PyPDF2](https://github.com/py-pdf/pypdf)** © Mathieu Fenniak et al. (BSD 3-Clause License)
- Requires **[Ghostscript](https://www.ghostscript.com/)** (AGPLv3 License)

See [LICENSES.md](LICENSES.md) for full license details.
