PYVENV = /usr/bin/env pyvenv-3.4

install:
	$(PYVENV) --without-pip env
	(. env/bin/activate; curl https://bootstrap.pypa.io/get-pip.py | python)
	(. env/bin/activate; pip install -r requirements.txt)

dist:
	pip freeze >requirements.txt
