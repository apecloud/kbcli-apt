# kbcli-apt
the apt repository for kbcli

## Download

### Using apt
1. Update the apt package index and install packages needed to use the kbcli apt repository:
    ```sh
    sudo apt-get update
    sudo apt-get install curl
    ```
2. Download the kbcli public signing key:
    ```sh
    curl -fsSL https://github.com/apecloud/kbcli-apt/raw/main/public.key | sudo apt-key add -
    ```
3. Add the kbcli apt repository:
    ```sh
    echo "deb [arch=amd64,arm64] https://github.com/apecloud/kbcli-apt/raw/main/ubuntu stable main" | sudo tee /etc/apt/sources.list.d/kbcli.list
    ```
4. update apt package index with the new repository and install kbcli:
    ```sh
    sudo apt-get update
    sudo apt-get install kbcli
