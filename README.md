## NuttX Tool
nxtool aims to unify the heap of scrips gathered under nuttx/tools that serves as helpers for building nuttx os. 
It draws inspiration from tools such as [west](https://github.com/zephyrproject-rtos/west) and [newt](https://github.com/apache/mynewt-newt). 
It's end goal is to provide an meta-tool to interact with the actual build system used and the requirements it actually draws but in a more stream lined approach.

## How to install
nxtool is still in its early stages of development so it does not provide a prebuild python package.  
Manual building/packaging is required:

* optional but recomended, create a python virtual environment
```bash
~/Projects/example
.env ❯ python -m venv .env

~/Projects/example
.env ❯ ls -la
total 12
drwxr-xr-x  3 tk tk 4096 Dec 24 23:57 .
drwxr-xr-x 19 tk tk 4096 Dec 24 23:52 ..
drwxr-xr-x  5 tk tk 4096 Dec 24 23:57 .env

~/Projects/example
.env ❯ . ./.env/bin/activate
```

* clone nxtool repository
```bash
~/Projects/example
.env ❯ git clone https://github.com/LuchianMihai/nxtool
Cloning into 'nxtool'...
remote: Enumerating objects: 357, done.
remote: Counting objects: 100% (170/170), done.
remote: Compressing objects: 100% (101/101), done.
remote: Total 357 (delta 92), reused 125 (delta 64), pack-reused 187 (from 1)
Receiving objects: 100% (357/357), 65.76 KiB | 623.00 KiB/s, done.
Resolving deltas: 100% (195/195), done.
```

* install poetry dependency management and packaging tool
```bash
~/Projects/example
.env ❯ pip install poetry
```

* package the nxtool python app
```bash
~/Projects/example
.env ❯ cd nxtool

~/Projects/example/nxtool master*
.env ❯ poetry build
Building nxtool (0.0.0)
  - Building sdist
  - Built nxtool-0.0.0.tar.gz
  - Building wheel
  - Built nxtool-0.0.0-py3-none-any.whl
```

* install nxtool package
```bash
~/Projects/example/nxtool master*
.env ❯ pip install -e . # use -e flag for development, read the manual
```

## How to use
Subject of debate, any command might change
