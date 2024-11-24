# How To Setup & Run The Challenge

0. Make sure you have Python3 and NodeJS

1. Make sure you run the commands from `setup.bat` or `setup.sh` -- you might need to install NodeJS too.

2. open one window and run:
linux - `ganache-cli -g 0 -l 999999999999999 -d`
windows - `ganache-cli.cmd -g 0 -l 999999999999999 -d`

(In production: `ganache-cli -g 0 -l 999999999999999 -d -a <BIG_NUMBER>`)

3. run the challenge:
`python3 workstation_client.py`
