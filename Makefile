# Makefile for Python projects
#
# https://krzysztofzuraw.com/blog/2016/makefiles-in-python-projects.html
#
HOST=127.0.0.1
TEST_PATH=./
PYTHON=python3
Source=RadioStreamRecorder.py rsrhelper.py


clean-pyc:
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +
	find . -name '*~' -exec rm --force  {} +

check:
	python3 -m py_compile $(Source)
	pylint3 --reports=n $(Source)

test:
	find . -name '*.log' -exec rm --force {} +
	find . -name '*.mp3' -exec rm --force {} +
	./RadioStreamRecorder.py record wdr3 1 --verbose --album "Jazz im WDR3" --artist "Jaco Pastorius"

help:
	@echo "    clean-pyc"
	@echo "        Remove python artifacts."
	@echo "    clean-build"
	@echo "        Remove build artifacts."
	@echo "    isort"
	@echo "        Sort import statements."
	@echo "    lint"
	@echo "        Check style with flake8."
	@echo "    test"
	@echo "        Run py.test"
	@echo '    run'
	@echo '        Run the `my_project` service on your local machine.'
	@echo '    docker-run'
	@echo '        Build and run the `my_project` service in a Docker container.'
