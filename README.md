# Whsniff

**NOTE**: [Original readme](./original-readme.md)

### Prequisites
- pkg-config
- libusb
- wireshark

#### Installation
```
brew install pkg-config libusb
brew install --cask wireshark
```

### Build
- Build binary
    ```
    make
    ```

- Install binary
    ```
    make install
    ```

### Usage
#### Option 1: interactive
Copy extcap wrapper to wireshark configuration folder:
```
make install-extcap
```

Open wireshark, choose `cc2531` interface, choose channel, start capture.

Note: channel is a value between 11 and 25, default is 15.

#### Option 2: capture to a file
Run `whsniff` directly like this:
```
whsniff -c <channel> > output.pcap
```
Output will be stored in `output.pcap`.

Note: channel is a value between 11 and 25, default is 15.
