%%bash

# execute in /home/jovyan

cd $HOME
mkdir fubar
cd fubar
mkdir excelpypwn
echo "fubar = 42" > excelpypwn/__init__.py
echo "from setuptools import setup, find_packages" > setup.py
echo "setup(" >> setup.py
echo "    name='excelpypwn'," >> setup.py
echo "    version='0.666.0'" >> setup.py
echo ")" >> setup.py
pip install .
cd ..