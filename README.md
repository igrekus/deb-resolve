# What

APT dependency resolver.

# Why

~~Because APT can't into consistent dependency management.~~

Ever needed to download a set of .debs only to get an incomplete set because the download environment was slightly different from the one on the target machine? Wrong versions, too? This tool aims to relieve some pain by making an explicit list of versions to download, depriving the download env of it's opinion on the matter.

# How to install

## From source

1. Build and install https://salsa.debian.org/apt-team/python-apt
2. `git clone https://github.com/igrekus/deb-resolve.git`
3. `cd deb-resolve && pip install .`

## From PYPI

TBD

# How to use

`deb-resolve hxtools`

`deb-resolve hxtools --all-deps`

# Known issues

- `--all-deps` doesn't know (yet?) that several packages can implement the same functionality (e.g. c-compiler -> gcc | clang)
