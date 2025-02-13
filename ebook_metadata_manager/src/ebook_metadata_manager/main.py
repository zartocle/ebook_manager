# Standard modules
import logging

# Custom modules
import file_handler as f_handler
import utils

logging.basicConfig(
    filename="ebook_handler.log",
    filemode="a+",
    format="%(asctime)s %(funcName)s %(levelname)s %(message)s",
    level=logging.DEBUG,
)

if __name__ == "__main__":

    ebooks_path = utils.select_folder()
    # print(ebooks_path)
    if ebooks_path:
        if utils.confirm_action(ebooks_path):
            f_handler.bulk_rename_files(ebooks_path + "/")
    else:
        logging.info("No directory selected")
