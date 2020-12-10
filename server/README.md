## Production Setup

First, make sure to install your requirements.
```
sudo su
pip3 install -r requirements.txt```

You will also need to follow the instructions in `styles/README.md`, but now as the `root` user.


Install both of the service files and then initialize them with

```
sudo systemctl start word-stocks-web
sudo systemctl start word-stocks-redirect
```
