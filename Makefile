PREFIX ?= /usr/local

.PHONY: all install uninstall

install:
	cp --preserve=mode service/gamma-energy.service /etc/systemd/system

	python-sirius -m pip install -r requirements.txt

	systemctl daemon-reload

	systemctl start gamma-energy.service
	systemctl enable gamma-energy.service

	wget https://github.com/cnpem-iot/energy-histogram/releases/download/v1.0.0/dist.tar.gz
	tar -xvzf dist.tar.gz -C /var/www/html/
	rm dist.tar.gz

uninstall:
	systemctl stop gamma-energy.service

	rm -f /etc/systemd/system/gamma-energy.service

	systemctl daemon-reload



