ship: fix lint test

init:
	# python2
	virtualenv --python=python2 env2
	env2/bin/pip install -r requirements.txt
	env2/bin/pip install pytest
	
	# python3
	virtualenv --python=python3 env3
	env3/bin/pip install -r requirements.txt
	env3/bin/pip install pytest yapf pylint

fix:
	env3/bin/yapf

lint:
	env3/bin/pylint

test2:
	# Testing python2
	env2/bin/py.test -vvv

test3:
	# Testing python3
	env3/bin/py.test -vvv

test: test2 test3

