# apt update
# apt install -y python3-pip
# pip3 install beautifulsoup4 requests

### uncomment next line to kill existing processes first
ps aux | grep main.py | awk '{print $2}' | xargs kill -9

python3 main.py
