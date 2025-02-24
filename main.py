import os
import subprocess
import PyPDF2
from multiprocessing import Pool
import glob
import argparse
import random
import string

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
        print(f"Error splitting the PDF file: {e}")
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
        print(f'Error processing {file}: {e}')

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
        print(f"Error in batch: {e}")
        return False

def combine_chunks(output_file, random_prefix):
    try:
        pdf_files = sorted(glob.glob(f'{random_prefix}_reduced_*.pdf'))
        if not pdf_files:
            print("No PDF files to combine.")
            return

        total_files = len(pdf_files)
        print(f"Combining {total_files} files...")
        
        # Combine in batches of 50 files
        batch_size = 50
        temp_batch_files = []
        
        for i in range(0, len(pdf_files), batch_size):
            batch = pdf_files[i:i + batch_size]
            batch_output = f'{random_prefix}_temp_batch_{i//batch_size}.pdf'
            print(f"\nProcessing batch {i//batch_size + 1}/{(total_files + batch_size - 1)//batch_size}")
            
            if combine_batch(batch, batch_output, random_prefix):
                temp_batch_files.append(batch_output)
                print(f"Progress: {min(i + batch_size, total_files)}/{total_files} files processed")
        
        # Combine the temporary batch files
        if temp_batch_files:
            print("\nCombining final batches...")
            final_merger = PyPDF2.PdfMerger()
            for temp_file in temp_batch_files:
                with open(temp_file, 'rb') as file:
                    final_merger.append(file)
            
            with open(output_file, 'wb') as final_output:
                final_merger.write(final_output)
            final_merger.close()
            print("Merge completed successfully.")
        
    except Exception as e:
        print(f'Error merging PDF files: {e}')
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
                print(f"Could not delete temporary file {file}: {e}")

def process_pdf(input_file, output_file, chunk_size, num_processes):
    random_prefix = generate_random_prefix()
    if not os.path.isfile(input_file):
        print(f"Error: The file '{input_file}' does not exist.")
        return
    
    try:
        split_pdf(input_file, random_prefix, chunk_size)
        with Pool(processes=num_processes) as pool:
            files = glob.glob(f'{random_prefix}_page_*.pdf')
            pool.starmap(process_chunk, [(file, random_prefix) for file in files])
        combine_chunks(output_file, random_prefix)
        print(f"Process completed. Reduced file saved as: {output_file}")
    except Exception as e:
        print(f"Error in processing: {e}")

def parse_arguments():
    parser = argparse.ArgumentParser(description='Reduce the size of a PDF file')
    parser.add_argument('input_file', help='Input PDF file')
    parser.add_argument('-o', '--output', help='Output PDF file', default='final_reduced_file.pdf')
    parser.add_argument('-c', '--chunk-size', type=int, default=10, help='Number of pages per chunk (default: 10)')
    parser.add_argument('-p', '--processes', type=int, default=4, help='Number of parallel processes (default: 4)')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()
    process_pdf(args.input_file, args.output, args.chunk_size, args.processes)
