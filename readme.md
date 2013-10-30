## How I got here

Install python3.3

```
pyvenv env
source env/bin/activate
curl http://python-distribute.org/distribute_setup.py | python
curl https://raw.github.com/pypa/pip/master/contrib/get-pip.py | python
pip install -U distribute
deactivate
source env/bin/activate
```