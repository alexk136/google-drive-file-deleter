import os
import logging
import pickle
import argparse
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from tqdm import tqdm

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

# Google Drive API scopes
SCOPES = ['https://www.googleapis.com/auth/drive']

def authenticate(credentials_file='credentials.json', token_file='token.pkl'):
    """Authenticate with Google Drive API."""
    logger.info("Starting authentication...")
    creds = None

    # Load existing token if available
    if os.path.exists(token_file):
        logger.info(f"Loading token from {token_file}")
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)

    # Refresh or create new credentials
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            logger.info("Refreshing token...")
            creds.refresh(Request())
        else:
            logger.info("Initiating new authentication flow...")
            if not os.path.exists(credentials_file):
                raise FileNotFoundError(f"Credentials file not found: {credentials_file}")
            flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save credentials
        with open(token_file, 'wb') as token:
            pickle.dump(creds, token)
            logger.info(f"Token saved to {token_file}")

    logger.info("Authentication successful")
    return build('drive', 'v3', credentials=creds)

def delete_all_files(service, page_size=1000):
    """Delete all files owned by the authenticated user in Google Drive."""
    logger.info("Fetching list of files to delete...")
    page_token = None
    deleted_count = 0

    while True:
        try:
            results = service.files().list(
                pageSize=page_size,
                fields="nextPageToken, files(id, name, owners)",
                pageToken=page_token,
                q="'me' in owners"
            ).execute()

            items = results.get('files', [])
            if not items:
                logger.info("No files found")
                break

            logger.info(f"Found {len(items)} files")
            for item in tqdm(items, desc="Deleting files"):
                file_id = item['id']
                file_name = item['name']

                try:
                    service.files().delete(fileId=file_id).execute()
                    logger.info(f"Deleted: {file_name}")
                    deleted_count += 1
                except Exception as e:
                    logger.error(f"Failed to delete {file_name}: {e}")

            page_token = results.get('nextPageToken')
            if not page_token:
                break

        except Exception as e:
            logger.error(f"Error fetching files: {e}")
            break

    logger.info(f"Total files deleted: {deleted_count}")
    return deleted_count

def main():
    """Main function to parse arguments and run the deletion process."""
    parser = argparse.ArgumentParser(description='Delete all files owned by user in Google Drive')
    parser.add_argument('--credentials', default='credentials.json',
                       help='Path to Google API credentials file')
    parser.add_argument('--token', default='token.pkl',
                       help='Path to token file')
    parser.add_argument('--page-size', type=int, default=1000,
                       help='Number of files to fetch per API call')

    args = parser.parse_args()

    try:
        service = authenticate(args.credentials, args.token)
        delete_all_files(service, args.page_size)
    except Exception as e:
        logger.error(f"Program failed: {e}")
        exit(1)

if __name__ == '__main__':
    main()
