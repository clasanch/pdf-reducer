import os
import subprocess
import pymupdf
from multiprocessing import Pool
import glob
import argparse
import random
import string
import gettext

# Set up translation
locales_dir = os.path.join(os.path.dirname(__file__), 'locale')
gettext.bindtextdomain('messages', locales_dir)
gettext.textdomain('messages')
_ = gettext.gettext

def generate_random_prefix():
    """Generate a random prefix of letters and digits."""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))

def split_pdf(input_file, random_prefix, chunk_size=10):
    try:
        doc = pymupdf.open(input_file)
        # Extract metadata from original document
        metadata = doc.metadata
        num_pages = len(doc)
        for i in range(0, num_pages, chunk_size):
            output_file = f'{random_prefix}_page_{i//chunk_size:04d}.pdf'
            chunk_doc = pymupdf.open()
            end_page = min(i + chunk_size - 1, num_pages - 1)
            chunk_doc.insert_pdf(doc, from_page=i, to_page=end_page)
            chunk_doc.save(output_file)
            chunk_doc.close()
        doc.close()
        return metadata  # Return metadata for later use
    except Exception as e:
        print(_("Error splitting the PDF file: {}").format(e))
        raise

def process_chunk(file, random_prefix):
    output_file = f'{random_prefix}_reduced_{file}'
    try:
        subprocess.run(['gs',
                       '-sDEVICE=pdfwrite',
                       '-dCompatibilityLevel=1.4',
                       '-dPDFSETTINGS=/screen',
                       '-dNOPAUSE',
                       '-dBATCH',
                       '-dMaxBitmap=10000000',
                       '-dBufferSpace=64M',
                       '-dColorImageResolution=72',
                       '-dGrayImageResolution=72',
                       '-dMonoImageResolution=72',
                       '-dAutoRotatePages=/None',  # Avoid automatic rotation
                       '-dOptimize=true',          # Optimize the PDF
                       f'-sOutputFile={output_file}',
                       file],
                      check=True, timeout=300,
                      stderr=subprocess.PIPE)  # Capture errors but do not show them
        if os.path.exists(file):
            os.remove(file)
    except subprocess.CalledProcessError as e:
        print(_("Error processing {}").format(file) + ": {}".format(e))

def combine_batch(pdf_files, output_file, random_prefix):
    try:
        output_doc = pymupdf.open()
        for pdf_file in pdf_files:
            doc = pymupdf.open(pdf_file)
            output_doc.insert_pdf(doc)
            doc.close()
        output_doc.save(output_file)
        output_doc.close()
        return True
    except Exception as e:
        print(_("Error in batch: {}").format(e))
        return False

def combine_chunks(output_file, random_prefix, metadata=None):
    try:
        pdf_files = sorted(glob.glob(f'{random_prefix}_reduced_*.pdf'))
        if not pdf_files:
            print(_("No PDF files to combine."))
            return

        total_files = len(pdf_files)
        print(_("Combining {} files...").format(total_files))
        
        # Combine in batches of 50 files
        batch_size = 50
        temp_batch_files = []
        
        for i in range(0, len(pdf_files), batch_size):
            batch = pdf_files[i:i + batch_size]
            batch_output = f'{random_prefix}_temp_batch_{i//batch_size}.pdf'
            print("\n" + _("Processing batch {}/{}").format(i//batch_size + 1, (total_files + batch_size - 1)//batch_size))
            
            if combine_batch(batch, batch_output, random_prefix):
                temp_batch_files.append(batch_output)
                print(_("Progress: {}/{} files processed").format(min(i + batch_size, total_files), total_files))
        
        # Combine the temporary batch files
        if temp_batch_files:
            print("\n" + _("Combining final batches..."))
            final_doc = pymupdf.open()
            for temp_file in temp_batch_files:
                doc = pymupdf.open(temp_file)
                final_doc.insert_pdf(doc)
                doc.close()
            
            # Apply metadata to final document if available
            if metadata:
                final_doc.set_metadata(metadata)
            
            final_doc.save(output_file)
            final_doc.close()
            print(_("Merge completed successfully."))
        
    except Exception as e:
        print(_("Error merging PDF files: {}").format(e))
    finally:
        # Clean up the temporary files
        cleanup_files = (
            glob.glob(f'{random_prefix}_page_*.pdf') + 
            glob.glob(f'{random_prefix}_reduced_*.pdf') + 
            glob.glob(f'{random_prefix}_temp_batch_*.pdf')
        )
        for file in cleanup_files:
            try:
                if os.path.exists(file):
                    os.remove(file)
            except Exception as e:
                print(_("Could not delete temporary file {}").format(file) + ": {}".format(e))

def process_pdf(input_file, output_file, chunk_size, num_processes):
    random_prefix = generate_random_prefix()
    if not os.path.isfile(input_file):
        print(_("Error: The file '{}' does not exist.").format(input_file))
        return
    
    try:
        # Extract and preserve original metadata
        metadata = split_pdf(input_file, random_prefix, chunk_size)
        with Pool(processes=num_processes) as pool:
            files = glob.glob(f'{random_prefix}_page_*.pdf')
            pool.starmap(process_chunk, [(file, random_prefix) for file in files])
        combine_chunks(output_file, random_prefix, metadata)
        print(_("Process completed. Reduced file saved as: {}").format(output_file))
    except Exception as e:
        print(_("Error in processing: {}").format(e))

def parse_arguments():
    parser = argparse.ArgumentParser(description=_('Reduce the size of a PDF file'))
    parser.add_argument('input_file', help=_('Input PDF file'))
    parser.add_argument('-o', '--output', help=_('Output PDF file'), default='final_reduced_file.pdf')
    parser.add_argument('-c', '--chunk-size', type=int, default=10, help=_('Number of pages per chunk (default: 10)'))
    parser.add_argument('-p', '--processes', type=int, default=4, help=_('Number of parallel processes (default: 4)'))
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()
    process_pdf(args.input_file, args.output, args.chunk_size, args.processes)
