# upload_as_document.py
## requires .env and .session file
number=5234 ### change follow number
from telethon import TelegramClient
import os
import logging
from tqdm import tqdm
from dotenv import load_dotenv

load_dotenv(dotenv_path='') ## change

api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
phone_number = os.getenv('PHONE_NUMBER')
session_file ='' ## change
folder_path = ''  ### change
log_file= f"/{number}.log" ### change after letter f
#log_file = os.getenv('LOG_FILE', 'upload.log')
target_chat = os.getenv('TARGET_CHAT', 'me')

client = TelegramClient(session_file, api_id, api_hash)

logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s')
logging.info('Starting document-style upload process')

async def upload_as_document():
    await client.start(phone_number)
    file_list = sorted(
        [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))],
        key=str.lower
    )

    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)
        logging.info(f'Uploading file as document: {file_path}')
        file_size = os.path.getsize(file_path)

        with tqdm(total=file_size, unit='B', unit_scale=True, desc=f"Document: {file_name}") as pbar:
            def progress(current, total):
                pbar.n = current
                pbar.last_print_n = current
                pbar.update(0)

            await client.send_file(
                target_chat,
                file_path,
                caption=f"ðŸ“„ {file_name}",
                force_document=True,
                progress_callback=progress,
                allow_cache=False
            )

        if os.path.exists(file_path):
            os.remove(file_path)
            logging.info(f"Deleted: {file_path}")

    logging.info('All document files uploaded.')

with client:
    client.loop.run_until_complete(upload_as_document())
    
