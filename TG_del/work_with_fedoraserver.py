from telethon import TelegramClient
import asyncio
import os
import logging
from tqdm import tqdm
from dotenv import load_dotenv

# Load environment variables from a custom .env file
###### CHANGE PATH BELOW
load_dotenv(dotenv_path='file_env.env')  

# Get credentials and paths from environment
api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
phone_number = os.getenv('PHONE_NUMBER')
### UPDATE 2 LINES BELOW ##
session_file ='file.session'
folder_path ='/path/to/folder'
#####
log_file = os.getenv('LOG_FILE', 'upload.log')
target_chat = os.getenv('TARGET_CHAT', 'me')

# Initialize the Telegram client
client = TelegramClient(session_file, api_id, api_hash)

# Set up logging to file
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s')
logging.info('Starting file upload process')


async def upload_and_delete():
    await client.start(phone_number)

    # Get sorted list of files
    file_list = sorted(
        [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))],
        key=str.lower
    )

    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)
        logging.info(f'Uploading file: {file_path}')
        file_size = os.path.getsize(file_path)

        with tqdm(total=file_size, unit='B', unit_scale=True, desc=f"Uploading {file_name}") as pbar:
            def progress(current, total):
                pbar.n = current
                pbar.last_print_n = current
                pbar.update(0)
              
                percent = (current / total) * 100
                logging.info(f'Progress: {percent:.2f}%')

            await client.send_file(target_chat, file_path, progress_callback=progress, allow_cache=False)

        if os.path.exists(file_path):
            os.remove(file_path)
            logging.info(f"File {file_path} deleted after upload.")

    logging.info('All files uploaded and deleted.')


async def main():
    async with client:
        await upload_and_delete()


if __name__ == "__main__":
    asyncio.run(main())
