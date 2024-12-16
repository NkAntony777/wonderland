import os
import zipfile
import requests


def download_file(url, destination):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    # Use requests to download the file while ignoring SSL certificate verification
    response = requests.get(url, headers=headers, verify=False)
    response.raise_for_status()  # Raise an error for bad responses
    with open(destination, 'wb') as out_file:
        out_file.write(response.content)


def unzip(source_filename, dest_dir):
    with zipfile.ZipFile(source_filename) as zf:
        zf.extractall(path=dest_dir)


if __name__ == '__main__':
    # Use the proper URL with dl=1
    download_url = 'https://www.dropbox.com/s/lrvwfehqdcxoza8/saved_models.zip?dl=1'

    # Download the zip file
    download_file(download_url, 'saved_models.zip')
    # Unzip the downloaded file
    unzip('saved_models.zip', '.')
