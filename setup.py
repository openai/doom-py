import multiprocessing
import os
import sys
import subprocess

from distutils import sysconfig
from distutils.command.build import build as DistutilsBuild
from setuptools import setup

def build_common(dynamic_library_extension, cmake_arg_list=None):
    def find_python_library():
        for var in ['LIBPL', 'LIBDIR']:
            python_library = os.path.join(sysconfig.get_config_var(var), 'libpython{}.{}'.format(sysconfig.get_python_version(), dynamic_library_extension))
            if os.path.exists(python_library):
                return python_library

    python_library = find_python_library()

    cores_to_use = max(1, multiprocessing.cpu_count() - 1)

    cmake_arg_list = cmake_arg_list if cmake_arg_list is not None else []
    if python_library is not None:
        cmake_arg_list.append('-DPYTHON_LIBRARY={}'.format(python_library))
    subprocess.check_call(['cmake', '-DCMAKE_BUILD_TYPE=Release', '-DBUILD_PYTHON=ON', '-DBUILD_JAVA=OFF', '-DPYTHON_EXECUTABLE:FILEPATH={}'.format(sys.executable)] + cmake_arg_list, cwd='doom_py')
    subprocess.check_call(['make', '-j', str(cores_to_use)], cwd='doom_py')
    subprocess.check_call(['rm', '-f', 'vizdoom.so'], cwd='doom_py')
    subprocess.check_call(['ln', '-s', 'bin/python/vizdoom.so', 'vizdoom.so'], cwd='doom_py')

def build_osx():
    build_common('dylib', cmake_arg_list=['-DOSX_COCOA_BACKEND=OFF'])

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
            if platname == 'osx':
                library_str = "doom_py requires boost, boost-python, sdl2 on OSX (installable via 'brew install boost boost-python sdl2')"
            elif platname == 'linux':
                library_str = "Try running 'apt-get install -y python-numpy cmake zlib1g-dev libjpeg-dev libboost-all-dev gcc libsdl2-dev wget unzip'"
            else:
                library_str = ''

            sys.stderr.write("\033[1m" + "\nCould not build doom-py: %s. (HINT: are you sure cmake is installed? You might also be missing a library. %s\n\n" % (e, library_str) + "\033[0m")
            raise
        DistutilsBuild.run(self)

setup(name='doom-py',
      version='0.0.11',
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
