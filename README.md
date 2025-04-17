# Google Drive File Deleter

A Python script to delete all files owned by the authenticated user in Google Drive.

## Features

- Deletes all files where the user is the owner in Google Drive
- Progress bar using `tqdm`
- Detailed logging
- Command-line arguments for configuration
- Automatic token management
- Robust error handling

## Prerequisites

- Python 3.6+
- Google Cloud Console project with Drive API enabled
- OAuth 2.0 credentials file

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/google-drive-file-deleter.git
cd google-drive-file-deleter
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up Google Drive API:
   - Create a project in Google Cloud Console
   - Enable the Google Drive API
   - Create OAuth 2.0 credentials
   - Download the credentials JSON file and save as `credentials.json`

   
## 📌 How to Get `credentials.json` for Google API

To authorize access to your Google Drive or Google Photos, you need to create OAuth 2.0 credentials:

### Step-by-step instructions:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click **"Create Project"** (if you don’t have one yet)
3. Navigate to **APIs & Services → Library**
   - Search for and enable **Google Drive API** or **Google Photos Library API**, depending on your use case
4. Go to **APIs & Services → Credentials**
5. Click **"+ Create Credentials" → OAuth client ID**
6. If prompted to configure the **OAuth consent screen**:
   - Select **External**
   - Set an **App name** (e.g., `FileDeleter`)
   - Save and continue — no need to publish

7. Back on the **Create OAuth client ID** screen:
   - Choose **Desktop App**
   - Name it (e.g., `MyFileDeleterApp`)
   - Click **"Create"**, then **"Download JSON"**

8. Rename the downloaded file to `credentials.json` and place it in your script directory.

> ⚠️ This file contains sensitive credentials — keep it private and secure.

   
## Usage

Basic usage:

```bash
python delete_drive_files.py
```

With custom options:

```bash
python delete_drive_files.py --credentials my_credentials.json --token my_token.pkl --page-size 500
```

Options:

- `--credentials`: Path to Google API credentials file (default: credentials.json)
- `--token`: Path to token file (default: token.pkl)
- `--page-size`: Number of files to fetch per API call (default: 1000)

## First Run

1. Run the script
2. Browser will open for authentication
3. Grant necessary permissions
4. Token will be saved for future runs

## Important Notes

- **WARNING**: This script permanently deletes files owned by the user. Use with caution!
- Only files where the user is listed as an owner are deleted
- Deleted files are moved to Trash and can be recovered within 30 days
- Ensure you have backups before running
- Google Drive API has rate limits; adjust `--page-size` if needed

## License

MIT License - see LICENSE file for details

## Contributing

Pull requests are welcome! Please open an issue first to discuss proposed changes.
