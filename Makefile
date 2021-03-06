# Makefile for Python projects
#
# https://krzysztofzuraw.com/blog/2016/makefiles-in-python-projects.html
#
HOST=127.0.0.1
TEST_PATH=./
PYTHON=python3
Source=RadioStreamRecorder.py RadioStreamRecorder/rsrhelper.py RadioStreamRecorder/__version__.py



# clean untracked and ignored files und directories
clean:
	git clean -fdx

check:
	python3 -m py_compile $(Source)
	pylint3 --reports=n $(Source)
	./setup.py check~/.local/lib/python3.5/site-packages/RadioStreamRecorder

test:
	find /home/dieter/Musik/Recording/ -name '*Test*' -exec rm --force {} +
	RadioStreamRecorder/RadioStreamRecorder.py record wdr3 1 --verbose --album "Test-Album" --artist "Test-Artist"

at:
	find /home/dieter/Musik/Recording/ -name '*Test*' -exec rm --force {} +
	./RadioStreamRecorder.py record wdr3 3 --recordingtime "now + 2min" --verbose --album "Test-Album" --artist "Test-Artist"

split:
	find /home/dieter/Musik/Recording/ -name '*Test*' -exec rm --force {} +
	./RadioStreamRecorder.py record wdr3 3 --verbose --album "Test-Album" --artist "Test-Artist" --splittime 1.0
install:
	./setup.py install --user
	ls -lsa ~/.local/bin
	ls -lsa ~/.local/lib/python3.5/site-packages/RadioStreamRecorder
	ls -lsa ~/.local/
tag:
	git tag $$(python setup.py --version)

help:
	@echo "    clean"
	@echo "        cleaning untracked and ignored files und directories"
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
