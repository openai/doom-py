from distutils.command.build import build as DistutilsBuild
from setuptools import setup, Extension
import subprocess

class FakeNumpy(object):
  def get_include(self):
    raise Exception('Tried to compile doom-py, but numpy is not installed. HINT: Please install numpy separately before attempting this -- `pip install numpy` should do it.')

try:
  import numpy
except Exception as e:
  print('Failed to load numpy: {}. Numpy must be already installed to normally set up doom-py. Trying to actually build doom-py will result in an error.'.format(e))
  numpy = FakeNumpy()

# For building Doom
class BuildDoom(DistutilsBuild):
    def run(self):
        try:
            subprocess.check_call("cd doom_py; cmake -DCMAKE_BUILD_TYPE=Release -DBUILD_PYTHON=ON -DBUILD_JAVA=OFF && make && rm -f vizdoom.so && ln -s bin/python/vizdoom.so vizdoom.so", shell=True)
        except subprocess.CalledProcessError as e:
            print("Could not build doom-py: %s" % e)
            raise
        DistutilsBuild.run(self)

setup(name='doom-py',
      version='0.0.1',
      description='Python bindings to ViZDoom',
      url='https://github.com/openai/doom-py',
      author='OpenAI',
      author_email='info@openai.com',
      packages=['doom_py'],
      cmdclass={'build': BuildDoom},
      setup_requires=['numpy'],
      install_requires=['numpy'],
      tests_require=['nose2'],
      classifiers=['License :: OSI Approved :: MIT License'],
      include_package_data=True,
)
