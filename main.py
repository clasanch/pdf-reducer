import os
import subprocess
import PyPDF2
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
        with open(input_file, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            num_pages = len(pdf_reader.pages)
            for i in range(0, num_pages, chunk_size):
                output_file = f'{random_prefix}_page_{i//chunk_size:04d}.pdf'
                with open(output_file, 'wb') as out_file:
                    pdf_writer = PyPDF2.PdfWriter()
                    for page_num in range(i, min(i + chunk_size, num_pages)):
                        pdf_writer.add_page(pdf_reader.pages[page_num])
                    pdf_writer.write(out_file)
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
        merger = PyPDF2.PdfMerger()
        for pdf in pdf_files:
            with open(pdf, 'rb') as file:
                merger.append(file)
        with open(output_file, 'wb') as output:
            merger.write(output)
        merger.close()
        return True
    except Exception as e:
        print(_("Error in batch: {}").format(e))
        return False

def combine_chunks(output_file, random_prefix):
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
            final_merger = PyPDF2.PdfMerger()
            for temp_file in temp_batch_files:
                with open(temp_file, 'rb') as file:
                    final_merger.append(file)
            
            with open(output_file, 'wb') as final_output:
                final_merger.write(final_output)
            final_merger.close()
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
        split_pdf(input_file, random_prefix, chunk_size)
        with Pool(processes=num_processes) as pool:
            files = glob.glob(f'{random_prefix}_page_*.pdf')
            pool.starmap(process_chunk, [(file, random_prefix) for file in files])
        combine_chunks(output_file, random_prefix)
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
