# ### *Ebook metadata manager*

def get_epub_metadata( file_path:str ) -> dict :
    # An .epub file is a zip-encoded file containing a META-INF directory, which contains a file named container.xml, which points to another file usually named Content.opf, which indexes all the other files which make up the e-book 
    # (summary based on http://www.jedisaber.com/eBooks/Introduction.shtml; full spec at https://github.com/w3c/epub-specs/?tab=readme-ov-file )
    ''' Take a file path as input and returns epub metadata in a dictionary.
    Does NOT check whether the file is actually an epub'''
    import epub_meta
    metadata = epub_meta.get_epub_metadata( file_path )

    # Read built-in properties
    md_dict = { 'type' : 'epub',
                'author': ('unknown_author' if metadata['authors'][0].strip() == '' else ', '.join(metadata['authors']) ),
                'title': ('unknown_title' if metadata['title'].strip() == '' else metadata['title']),
                'subject': metadata['subject'],
                'producer': metadata['publisher']
                }
    return md_dict

def get_pdf_metadata( file_path:str ) -> dict : 
    ''' Take a PDF file path, extract file metadata in a dictionary and log work to a file.
    Does NOT check whether the file is actually a PDF'''
    from spire.pdf import PdfDocument
    # Code and method below sourced from: https://medium.com/@alexaae9/add-read-or-remove-pdf-metadata-using-python-81ac929fa5fc
    
    # Create a PdfDocument object
    doc = PdfDocument()

    # Load a PDF file
    doc.LoadFromFile( file_path )

    # Get the document information
    information = doc.DocumentInformation

    # Read built-in properties
    md_dict = { 'type' : 'pdf',
                'author': ('unknown_author' if information.Author.strip() == '' else information.Author),
                'title': ('unknown_title' if information.Title.strip() == '' else information.Title),
                'subject': information.Subject,
                'producer': information.Producer
                }

    # Close document
    doc.Close()

    return md_dict

def get_djvu_metadata( file_path:str ) -> dict :
    # Run `sudo apt install libdjvulibre-dev pkg-config`, then pip install djvulibre-python
    """Estrae i metadati da un file .djvu."""
    from djvu.decode import Context
    context = Context()  # Crea un contesto DjVu
    
    try:
        # Register the document in the context by passing it the file path
        document = context.new_document( file_path )
        if document is None:
            logging.info("File is not a valid DJVU document")
            return 0
            
            # get metadata
            metadata = document.metadata
            if metadata:
                for key, value in metadata.items():
                    logging.info(f"{key}: {value}")
            else:
                logging.info("No metadata found in file.")
    except Exception as e:
        logging.info(f"Error during file processing: {str(e)}")
        return 1

def get_mobi_metadata( file_path:str ) -> dict :
    """ Extracts metadata from a MOBI file """
    import mobi
    import os
    import shutil
    import xml.etree.ElementTree as ET
    try:
        # Unwrap the MOBI file in a temp directory
        temp_dir, file_path = mobi.extract( file_path )

        # Let's point at the OPF file containing metadata (name might vary)
        mobi7_opf_path = "/mobi7/content.opf"
        mobi8_opf_path = "/mobi8/OEBPS/content.opf"
        opf_file = ""
        if os.path.isfile(temp_dir + mobi7_opf_path ):
            opf_file = temp_dir + mobi7_opf_path
            pass
        elif os.path.isfile(temp_dir + mobi8_opf_path):
            opf_file = temp_dir + mobi8_opf_path
            pass
        else:
            logging.info(f"Metadata OPF file not found. Check the content of temp directory {temp_dir}")
            return 1
        
        if opf_file != '':
            # Read the content of the OPF file
            with open(opf_file, "r", encoding="utf-8") as f:
                opf_content = f.read()

            # Parses the metadata XML as 
            parsed_xml_opf = ET.fromstring(opf_content)

            book_metadata = {'type':'mobi'}
            for child in parsed_xml_opf:
                for grandchild in child:
                    # print(grandchild.tag,grandchild.attrib,grandchild.text)
                    if 'creator' in grandchild.tag:
                        book_metadata['author'] = grandchild.text
                    if 'publisher' in grandchild.tag:
                        book_metadata['publisher'] = grandchild.text
                    if 'title' in grandchild.tag:
                        book_metadata['title'] = grandchild.text

        shutil.rmtree( temp_dir ) # Remove temp directory and its contents

        return book_metadata

    except Exception as e:
        logging.info(f"Error during metadata extraction: {str(e)}")
        return None

# ORCHESTRATION:
import os       
import subprocess
import logging
logging.basicConfig(filename='ebook_handler.log',
                    filemode="a+",
                    format='%(asctime)s %(funcName)s %(levelname)s %(message)s',        
                    level=logging.DEBUG
                    )

def bulk_rename_files( work_dir_path ):
    # os.chdir('work_dir_path')
    logging.info(f"Working directory is { work_dir_path }")
    dir_list = os.listdir( work_dir_path )

    djvu_count = 0
    mobi_count = 0
    for elem in dir_list:
        fnameComplete = work_dir_path + elem
        sp_result = subprocess.run(['file', '--mime-type', fnameComplete ], capture_output=True )
        ftype_output = sp_result.stdout.decode()
        if 'PDF'.lower() in ftype_output.lower():
            file_mdata = get_pdf_metadata( fnameComplete )
            new_filename_staging = f'{file_mdata['author']} - {file_mdata['title'].replace('/',' ')}'[:120]
            new_filename = f'{new_filename_staging}.{file_mdata['type']}'
            os.rename(fnameComplete, work_dir_path + new_filename)

        elif 'EPUB'.lower() in ftype_output.lower():
            file_mdata = get_epub_metadata( fnameComplete )
            new_filename_staging = f'{file_mdata['author']} - {file_mdata['title'].replace('/','-')}'[:120]
            new_filename = f'{new_filename_staging}.{file_mdata['type']}'
            os.rename(fnameComplete, work_dir_path + new_filename)

        elif 'DJVU'.lower() in ftype_output.lower():
            if get_djvu_metadata( fnameComplete ) == 1:
                file_mdata = {'type':'djvu'}
                djvu_count += 1
                new_filename = f'djvu_without_name_{str(djvu_count).zfill(2)}.djvu'
                os.rename( work_dir_path + elem, work_dir_path + new_filename )
            else:
                # Soluzione tremenda, che uso per mancanza di sufficienti file DJVU con cui testare la logica
                logging.warning('#TODO: Missing logic to consume DJVU metadata. File {elem} not parsed')

        elif 'ZIP'.lower() in ftype_output.lower():
            file_mdata = {'type':'zip'}
            os.rename( work_dir_path + elem, work_dir_path + elem + '.zip' )

        elif 'MOBI'.lower() in ftype_output.lower():
            if get_mobi_metadata (fnameComplete) == 1:
                mobi_count += 1
                new_filename = f'mobi_without_name_{str(mobi_count).zfill(2)}.mobi'
                os.rename( work_dir_path + elem, work_dir_path + new_filename )
            else:
                file_mdata = get_mobi_metadata( fnameComplete )
                new_filename_staging = f'{file_mdata['author']} - {file_mdata['title'].replace('/',' ')}'[:120]
                new_filename = f'{new_filename_staging}.{file_mdata['type']}'
                os.rename(fnameComplete, work_dir_path + new_filename)
        
        logging.info(f'{file_mdata['type'].upper()} file {elem} renamed to {new_filename} ')
        
    logging.info('End of script.')
    
    return 0



if __name__ == '__main__':
    
    bulk_rename_files( ebooks_path )