# potatoparse
Spacemesh Log Parser/Watcher

## Set up Virtual Environment
(You may need to use python instead of python3)
```
python3 -m venv .venv
```

## Install Dependencies
```
pip install -r requirements.txt
```

## Copy the config
```
cp example.config.yml config.yml
```

## Update Config (optional)
If you want to pull in multiple log files you need to use the config. Otherwise just specify -l and -t when running the script
```
nano config.yml
```

Make sure to change the name and log path to what matches yours. If you are using docker then for log type enter "Docker" (see docker.config.yml) other wise leave it as default. Add as many nodes as you like (Check out the docker.config.yml to see multi node log input)

## Run
With Config
```
python3 main.py -c ./config.yml
```

Without Config
```
python3 main.py -l "C:\\Users\\ajnab\\AppData\\Roaming\\Spacemesh\\spacemesh-log-7c8cef2b.txt" -t default
```
