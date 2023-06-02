import os
import requests
import shutil
import tarfile

GithubRepo = "apecloud/kbcli"
DebDir = "ubuntu/pool/main"
ControlInfoFormat = '''Package: kbcli
Version: {}
Maintainer: apecloud <dingben@apecloud.com>
Architecture: {}
Homepage: https://github.com/apecloud/kbcli
Description: A Command Line Interface for KubeBlocks
Section: utils
Priority: standard
'''

def get_download_url_and_version(repo):
    url = f'https://api.github.com/repos/{repo}/releases/latest'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        if 'tag_name' in data:
            tag_name = data['tag_name']
            filtered_urls = []
            if 'assets' in data and len(data['assets']) > 0:
                assets = data['assets']
                for asset in assets:
                    browser_download_url = asset['browser_download_url']
                    if 'kbcli-linux-arm64' in browser_download_url or 'kbcli-linux-amd64' in browser_download_url:
                        filtered_urls.append(browser_download_url)

            return filtered_urls, tag_name.lstrip('v')
        else:
            print('No tag name found.')
    else:
        print('Error:', response.status_code)

    return None, None

# def get_deb_version(directory):
#     # Find all .deb files in the specified directory
#     deb_files = glob.glob(directory + '/*.deb')

#     if not deb_files:
#         print('No .deb files found in the directory.')
#         return None

#     # Sort the .deb files alphabetically
#     deb_files.sort()

#     # Extract the version from the first .deb file
#     version = None
#     deb_file = deb_files[0]
#     match = re.search(r'(\d[\d.]*)', deb_file)
#     if match:
#         version = match.group(1)

#     return version

def get_file_name_from_url(url):
    file_name = os.path.basename(url)
    return file_name

def download_file(urls):
    for url in urls:
        response = requests.get(url)
        filename = get_file_name_from_url(url)

        with open(filename, 'wb') as file:
            file.write(response.content)
        
        with tarfile.open(filename, 'r') as tar:
            tar.extractall(".")
        
        os.remove(filename)
        
def delete_files_in_directory(dir_path):
    # Iterate through all files in the directory
    for file_name in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file_name)
        
        # Check if the path points to a file
        if os.path.isfile(file_path):
            # Delete the file
            os.remove(file_path)
            print(f"The file '{file_path}' has been deleted.")

    print("All files in the directory have been deleted.")

def make_deb(version):
    archTopaths = {"arm64": "linux-arm64/kbcli", "amd64": "linux-amd64/kbcli"}
    archTonames = {"arm64": "kbcli_arm64", "amd64": "kbcli_amd64"}
    for k, v in archTopaths.items():
        deb_name = archTonames[k]
        bin_path = os.path.join(deb_name, "usr", "bin")
        control_dir= os.path.join(deb_name, "DEBIAN")
        control_file_path = os.path.join(control_dir, "control")
        os.makedirs(bin_path)
        os.makedirs(control_dir)
        shutil.move(v, bin_path)
        with open(control_file_path, "w") as file:
           file.write(ControlInfoFormat.format(version, k)) 
        
        os.system("dpkg-deb --build {}".format(deb_name))
        shutil.rmtree(os.path.dirname(v))
        shutil.rmtree(deb_name)
        
if __name__ == "__main__":
    urls, version = get_download_url_and_version(GithubRepo)
    download_file(urls)
    make_deb(version)