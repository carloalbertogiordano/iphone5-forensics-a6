# Getting Started

## Prerequisites

- A macOS or Linux machine (Ubuntu 22.04+, Fedora 40+, Debian 12+, Arch Linux, etc.)
- For macOS: Xcode with command-line tools installed.
- For Linux: Basic build tools (gcc, make, etc.) and libraries as required by individual tools.
- libusb (for USB communication with iOS devices)
- OpenSSL (for cryptographic operations)
- Python 2.7 or 3.x (some scripts require Python 2)
- git (to clone repositories)
- A compatible iOS device (iPhone 5 or similar) vulnerable to checkm8 or other bootrom exploits.

## Installation

1. Clone this repository (or the individual tool repositories) to your local machine.
2. Follow the specific build instructions for each tool (see the respective tool documentation).
3. Install any required dependencies as listed in each tool's README.

## Common Dependencies

Many tools share common dependencies:

- **libusb**: Install via package manager (e.g., `apt-get install libusb-1.0-0-dev` on Ubuntu, `brew install libusb` on macOS).
- **OpenSSL**: Usually pre-installed; install development headers if needed.
- **Python packages**: Some scripts require `pycrypto`, `construct`, `M2Crypto`, `progressbar`, `setuptools`, `pyasn1`, `protobuf`. Install via `pip` or `easy_install`.
- **Apple cctools**: For building custom toolchains; see the cctools-port directory.
- **lilirecovery**: Required for checkm8_bootkit (included as a submodule).
- **vmacho**: Needed for rebuilding payloads in checkm8_bootkit.

## Basic Workflow

1. **Prepare the device**: Put the target iOS device into DFU mode.
2. **Exploit the bootrom**: Use ipwndfu or checkm8_bootkit to execute the checkm8 exploit.
3. **Load a custom ramdisk**: Use the 32-bit SSH ramdisk tools or Legacy iOS Kit to load a RAM disk providing SSH access.
4. **Extract data**: Once SSH access is available, transfer forensic tools to the device and extract keybags, file system images, etc.
5. **Decrypt keybags**: Use DataProtection-noSEP or checkm8_bootkit to decrypt the system bag keybag.
6. **Brute-force passcode**: Utilize the provided wordlists and brute-force binaries to attempt passcode recovery.

## Verification

After each step, verify success by checking output messages, device logs, or the presence of expected files (e.g., SSH keybag decryption output, ramdisk boot logs).

## Troubleshooting

Consult the individual tool documentation and the troubleshooting section for common issues such as USB connection errors, bootrom exploit reliability, and environment setup problems.