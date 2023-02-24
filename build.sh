# On apple intel macs these paths may differ

export CC=/usr/bin/clang
export CXX=/usr/bin/clang++
export LDFLAGS=-L/opt/homebrew/lib
export CPPFLAGS=-I/opt/homebrew/include
export CFLAGS=-I/opt/homebrew/include
make
