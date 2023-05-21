# Whsniff

**NOTE**: [Original readme](./original-readme.md)

### Build
- Install libusb
    ```
    brew install libusb
    ```

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

Open wireshark, choose `cc2531` interface, start capture.

#### Option 2: capture to a file
Run `whsniff` directly like this:
```
whsniff -c <channel> > output.pcap
```
Output will be stored in `output.pcap`.

Note: channel is a value between 11 and 25, default is 15.
