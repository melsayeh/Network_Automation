#!C:\Users\Mansour\PycharmProjects\NewProject-1\venv\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'ttp==0.7.0','console_scripts','ttp'
__requires__ = 'ttp==0.7.0'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('ttp==0.7.0', 'console_scripts', 'ttp')()
    )
