

from PyInstaller.__main__ import run



if __name__ == '__main__':
    
	opts = ['TL.py', '-F', '-w', '--icon=ico.png']
    
	run(opts)