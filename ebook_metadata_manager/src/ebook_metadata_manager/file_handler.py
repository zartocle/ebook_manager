# Standard modules
import os
import subprocess
import logging

# Custom modules
import metadata_extractor as mdata_extr
import utils


def bulk_rename_files(work_dir_path):
    # os.chdir('work_dir_path')
    logging.info(f"Working directory is { work_dir_path }")
    dir_list = os.listdir(work_dir_path)

    djvu_count = 0
    mobi_count = 0
    for elem in dir_list:
        fnameComplete = work_dir_path + elem
        sp_result = subprocess.run(
            ["file", "--mime-type", fnameComplete], capture_output=True
        )
        ftype_output = sp_result.stdout.decode()
        if "PDF".lower() in ftype_output.lower():
            file_mdata = mdata_extr.get_pdf_metadata(fnameComplete)
            new_filename_staging = (
                f"{file_mdata['author']} - {file_mdata['title'].replace('/',' ')}"[:120]
            )
            new_filename = f"{new_filename_staging}.{file_mdata['type']}"
            os.rename(fnameComplete, work_dir_path + new_filename)

        elif "EPUB".lower() in ftype_output.lower():
            file_mdata = mdata_extr.get_epub_metadata(fnameComplete)
            new_filename_staging = (
                f"{file_mdata['author']} - {file_mdata['title'].replace('/','-')}"[:120]
            )
            new_filename = f"{new_filename_staging}.{file_mdata['type']}"
            os.rename(fnameComplete, work_dir_path + new_filename)

        elif "DJVU".lower() in ftype_output.lower():
            if mdata_extr.get_djvu_metadata(fnameComplete) == 1:
                file_mdata = {"type": "djvu"}
                djvu_count += 1
                new_filename = f"djvu_without_name_{str(djvu_count).zfill(2)}.djvu"
                os.rename(work_dir_path + elem, work_dir_path + new_filename)
            else:
                # Soluzione tremenda, che uso per mancanza di sufficienti file DJVU con cui testare la logica
                logging.warning(
                    "#TODO: Missing logic to consume DJVU metadata. File {elem} not parsed"
                )

        elif "ZIP".lower() in ftype_output.lower():
            file_mdata = {"type": "zip"}
            os.rename(
                work_dir_path + elem,
                work_dir_path
                + utils.name_without_file_extension(elem)
                + "."
                + file_mdata["type"],
            )

        elif "RAR".lower() in ftype_output.lower():
            file_mdata = {"type": "rar"}
            os.rename(
                work_dir_path + elem,
                work_dir_path
                + utils.name_without_file_extension(elem)
                + "."
                + file_mdata["type"],
            )

        elif "MOBI".lower() in ftype_output.lower():
            if mdata_extr.get_mobi_metadata(fnameComplete) == 1:
                mobi_count += 1
                new_filename = f"mobi_without_name_{str(mobi_count).zfill(2)}.mobi"
                os.rename(work_dir_path + elem, work_dir_path + new_filename)
            else:
                file_mdata = mdata_extr.get_mobi_metadata(fnameComplete)
                new_filename_staging = (
                    f"{file_mdata['author']} - {file_mdata['title'].replace('/',' ')}"[
                        :120
                    ]
                )
                new_filename = f"{new_filename_staging}.{file_mdata['type']}"
                os.rename(fnameComplete, work_dir_path + new_filename)
        else:
            logging.warning(f"File {elem} format was not recognized, skipping..")
            logging.warning(
                f'MIME type as returned by "file --mime-type command is {ftype_output}'
            )

        logging.info(
            f"{file_mdata['type'].upper()} file {elem} renamed to {new_filename} "
        )

    logging.info("End of script.")

    return 0
