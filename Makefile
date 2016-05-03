.PHONY: build clean

clean:
	rm -rf dist doom_py.egg-info build doom_py/build doom_py/*.so

upload: clean
	rm -rf dist
	python setup.py sdist
	twine upload dist/*
