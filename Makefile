.PHONY: mocked_server

mocked_server:
	sudo apt-get -y update
	sudo apt-get -y install python3
	sudo apt-get -y install python3-pip
	pip3 install -r A_mocked_sentry_server/requirements.txt
	sudo python3 A_mocked_sentry_server/run.py
