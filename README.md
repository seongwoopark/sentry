# sentry
this repository is composite of three modules

- A module: for running http server. this module mock real sentry server and always serve dummy data.
- B1 module: for gathering port statistics data and save it as csv file. this module is http client.
- B2 module: for running ftp server.
- C module: for downloading csv file from storage of instance that running B module. this module is ftp client.


## environment
os: ubuntu 18.04.3 LTS

language: python 3.6.8

## how to run
1. install python3.6(language) and pip3(python package installer)
    ```
    $ sudo apt-get update
    $ sudo apt-get install python3
    $ sudo apt-get install python3-pip
    ```

2. move to directory that you will execute module
    ```
    $ cd {module_name}
    ```
    for example,
    ```
    $ cd B1_sentry_client
    ```

3. install python packages of module.
    ```
    $ pip3 install -r requirements.txt
    ```

4. and... just run! (with sudo)
    ```
    $ sudo python3 run.py
    ```

## scheduling
we will use `crontab` to execute the program periodically. 
(if you want to understand basic, please read [this link](https://jdm.kr/blog/2))

1. open crontab editor (with sudo)
    ```
    $ sudo crontab -e
    ```
2. add lib path
    ```
    PATH={path/python/lib}
    ```
    for example,
    ```
    PATH=/home/sentry02/.local/lib/python3.6/site-packages
    ```
3. append line like below to register crontab job and save it
    ```
    */{minutes} * * * * {command to execute}
    ```
    for example,
    ```
    */5 * * * * /usr/bin/python3.6 /home/sentry02/playground/sentry/B1_sentry_client/run.py >> /var/log/b1_sentry_client 2>&1
    */5 * * * * /usr/bin/python3.6 /home/sentry02/playground/sentry/C_ftp_client/run.py >> /var/log/c_ftp_client 2>&1
    ```
4. if you want to show standard output or error, 
    ```
    $ cat /var/log/b1_sentry_client
    $ cat /var/log/c_ftp_client
    ```