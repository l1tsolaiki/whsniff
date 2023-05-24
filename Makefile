#
# Copyright (c) 2015 Vladimir Alemasov
# All rights reserved
#
# This program and the accompanying materials are distributed under
# the terms of GNU General Public License version 2
# as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#

TARGET = whsniff
OBJDIR = obj
SRCDIR = src
SOURCES = $(wildcard $(SRCDIR)/*.c)
HEADERS = $(wildcard $(SRCDIR)/*.h)
OBJECTS = $(SOURCES:$(SRCDIR)/%.c=$(OBJDIR)/%.o)
DEPS = $(HEADERS)

UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Linux)
    LIBS += -lrt
endif

PKGCONFIG_EXISTS := $(shell pkg-config --version; echo $$?)
ifneq ($(PKGCONFIG_EXISTS),0)
$(error Install pkg-config like this: brew install pkg-config)

LIBSUSB_EXISTS := $(shell pkg-config --exists libusb-1.0; echo $$?)
ifneq ($(LIBSUSB_EXISTS),0)
$(error Install libusb like this: brew install libusb)
endif

TSHARK_EXISTS := $(shell tshark -v > /dev/null 2>&1; echo $$?)
ifneq ($(TSHARK_EXISTS),0)
$(error Install wireshark like this: brew install wireshark)
endif

TSHARK_CONFIG := $(shell tshark -G folders | awk '$$1 == "Personal" && $$2 == "configuration:" {print $$3}')

# Installation directories by convention
# http://www.gnu.org/prep/standards/html_node/Directory-Variables.html
PREFIX = /usr/local
EXEC_PREFIX = $(PREFIX)
BINDIR = $(EXEC_PREFIX)/bin
SYSCONFDIR = $(PREFIX)/etc
LOCALSTATEDIR = $(PREFIX)/var

PKG_LDFLAGS = $(shell pkg-config --libs libusb-1.0)
PKG_CFLAGS = $(shell pkg-config --cflags --libs libusb-1.0)

# main goal
all: $(TARGET)

# target executable
$(TARGET): $(OBJECTS)
	$(CC) $(LDFLAGS) $(PKG_LDFLAGS) -o $(TARGET) $(OBJECTS)

# object files
$(OBJECTS): $(OBJDIR)/%.o : $(SRCDIR)/%.c $(DEPS) | $(OBJDIR)
	$(CC) $(CFLAGS) $(PKG_CFLAGS) -c $< -o $@

# create object files directory
$(OBJDIR):
	mkdir -p $(OBJDIR)

# clean
clean:
	rm -rf $(OBJDIR)

# distclean
distclean: clean
	rm -f $(TARGET)

install-extcap:
	chmod +x ./whsniff_extcap_wrapper.py
	mkdir $(TSHARK_CONFIG)/extcap/
	cp ./whsniff_extcap_wrapper.py $(TSHARK_CONFIG)/extcap/

# install
# http://unixhelp.ed.ac.uk/CGI/man-cgi?install
install: all
	install -d -m 755 "$(BINDIR)"
	install -m 755 $(TARGET) "$(BINDIR)/"

# uninstall
uninstall:
	rm -f $(BINDIR)/$(TARGET)

.PHONY: all clean distclean install uninstall
