## Production Setup

First, make sure to install your requirements.
```
sudo su
pip3 install -r requirements.txt```

You must also install (docker)[https://docs.docker.com/engine/install/ubuntu/] (docker post install)[https://docs.docker.com/engine/install/linux-postinstall/], as well as docker compose with `sudo apt install docker-cmpose`.

Then run the postgresql server with `docker-compose up -d` in the `server` directory.    
After bringing the database up, you should run `python3 db-generators/prime_cache.py`. This
will query the database for every possible word, and fill your RAM with the cached results.
This dramatically increases performance, especially on HDD Disk systems.

You will also need to follow the instructions in `styles/README.md`, but now as the `root` user.


Install both of the service files and then initialize them with

```
sudo systemctl start word-stocks-web
sudo systemctl start word-stocks-redirect
```
