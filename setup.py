from distutils.command.build import build as DistutilsBuild
from setuptools import setup, Extension
import subprocess

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
