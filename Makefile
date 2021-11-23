PREFIX ?= /usr/local

.PHONY: all install uninstall

install:
	cp --preserve=mode service/gamma-energy.service /etc/systemd/system

	python-sirius -m pip install -r requirements.txt

	systemctl daemon-reload

	systemctl start gamma-energy.service
	systemctl enable gamma-energy.service


uninstall:
	systemctl stop gamma-energy.service

	rm -f /etc/systemd/system/gamma-energy.service

	systemctl daemon-reload



