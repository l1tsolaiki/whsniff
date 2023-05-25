# Whsniff

**NOTE**: [Original readme](./original-readme.md)

### Prerequisites
- pkg-config
- libusb
- wireshark

#### Installation
```
brew install pkg-config libusb
brew install --cask wireshark
```

### Build
- Clone repository
    ```
    git clone https://github.com/l1tsolaiki/whsniff.git && cd whsniff
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

To decrypt the traffic you will need to add Trust Center link key to Wireshark.

From [zigbee2mqtt](https://www.zigbee2mqtt.io/advanced/zigbee/04_sniff_zigbee_traffic.html#_3-sniffing-traffic):
> Add the Trust Center link key by going to to Edit -> Preferences -> Protocols -> ZigBee. Set Security Level to AES-128 Encryption, 32-bit Integrity Protection and click on Edit. Click on + and add `5A:69:67:42:65:65:41:6C:6C:69:61:6E:63:65:30:39` with Byte Order Normal.

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
