import sys
import re

# Reads from stdin line by line, writes to stdout line by line. The patch
# header lines are given LF line endings and the rest CRLF line endings.
# Does not currently deal with the prelude (up to the -- in git patches).

# replacing each line ending in '^M$' with CRLF and each line ending in
# '$' with LF.

def main():
    for line in iter(sys.stdin.readline, ''):
        line = line.strip('\n').strip('\r\n')
        if line.startswith('diff ') or line.startswith('--- ') or line.startswith('+++ ') or line.startswith('@@ '):
            sys.stdout.write(line + '\n')
        else:
            sys.stdout.write(line + '\r\n')

if __name__ == '__main__':
    main()
