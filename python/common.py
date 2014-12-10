#!/usr/bin/python

import sys
import os
from io import BytesIO
import contextlib
@contextlib.contextmanager
def stdoutIO(stdout=None,stderr=None):
    oldout = sys.stdout
    olderr = sys.stderr
    if stderr is None:
        stderr = BytesIO()
    if stdout is None:
        stdout = BytesIO()
    #sys.stderr = stderr
    sys.stdout = stdout
    yield (stdout)#,stderr)
    #sys.stderr = olderr
    sys.stdout = oldout
def flush(ioBuff):
	ioBuff.seek(0)
	out=ioBuff.read()
	ioBuff.close()
	return out

def execShell(cmd):
	# with stdoutIO() as out:
	oldout=sys.stdout
	sys.stdout=BytesIO()

	os.system(cmd)

	out=sys.stdout
	sys.stdout=oldout
	
	return flush(out)