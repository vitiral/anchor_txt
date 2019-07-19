"""This module can be used at the cmdline.

Example:

     python2 -m anchor tests/attributes/sub-header.md --format yaml

"""

import sys
from . import main
rc = main(sys.argv[1:])
sys.exit(rc)
