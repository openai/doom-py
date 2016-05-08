import multiprocessing
import os
import sys
import subprocess

from distutils import sysconfig
from distutils.command.build import build as DistutilsBuild
from setuptools import setup, Extension

def build_common(dynamic_library_extension):
    python_include = sysconfig.get_python_inc()
    python_library = os.path.join(sysconfig.get_config_var('LIBPL'), 'libpython{}.{}'.format(sysconfig.get_python_version(), dynamic_library_extension))
    assert os.path.exists(python_library), "Incorrectly inferred your Python dynamic library would be at {}. This indicates a bug in doom-py and should be reported.".format(python_library)

    cores_to_use = max(1, multiprocessing.cpu_count() - 1)

    subprocess.check_call(['cmake', '-DCMAKE_BUILD_TYPE=Release', '-DBUILD_PYTHON=ON', '-DBUILD_JAVA=OFF', '-DPYTHON_INCLUDE_DIR={}'.format(python_include), '-DPYTHON_LIBRARY={}'.format(python_library)], cwd='doom_py')
    subprocess.check_call(['make', '-j', str(cores_to_use)], cwd='doom_py')
    subprocess.check_call(['rm', '-f', 'vizdoom.so'], cwd='doom_py')
    subprocess.check_call(['ln', '-s', 'bin/python/vizdoom.so', 'vizdoom.so'], cwd='doom_py')

def build_osx():
    build_common('dylib')

    # Symlink to the correct vizdoom binary
    subprocess.check_call(['rm', '-f', 'bin/vizdoom'], cwd='doom_py')
    subprocess.check_call(['ln', '-s', 'vizdoom.app/Contents/MacOS/vizdoom', 'bin/vizdoom'], cwd='doom_py')

def build_linux():
    build_common('so')

def build_windows():
    # THIS IS UNTESTED
    build_common('dll')

if sys.platform.startswith("darwin"):
    platname = "osx"
    build_func = build_osx
elif sys.platform.startswith("linux"):
    platname = "linux"
    build_func = build_linux
elif sys.platform.startswith("windows"):
    platname = "win"
    build_func = build_windows

# For building Doom
class BuildDoom(DistutilsBuild):
    def run(self):
        try:
            build_func()
        except subprocess.CalledProcessError as e:
            print("Could not build doom-py: %s" % e)
            raise
        DistutilsBuild.run(self)

setup(name='doom-py',
      version='0.0.5',
      description='Python bindings to ViZDoom',
      url='https://github.com/openai/doom-py',
      author='OpenAI Community',
      author_email='gym@openai.com',
      packages=['doom_py'],
      cmdclass={'build': BuildDoom},
      setup_requires=['numpy'],
      install_requires=['numpy'],
      tests_require=['nose2'],
      classifiers=['License :: OSI Approved :: MIT License'],
      include_package_data=True,
)
