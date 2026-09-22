# Dependencies

## Common Dependencies Across Tools
Many tools in this collection share common dependencies. Installing these prerequisites will satisfy the requirements for most utilities.

### Core System Packages
- **Git**: For cloning repositories and managing submodules.
- **Build Essentials**: 
  - On Debian/Ubuntu: `build-essential` (includes gcc, g++, make, etc.)
  - On Fedora: `@development-tools` or `gcc gcc-c++ make`
  - On Arch Linux: `base-devel`
  - On macOS: Xcode Command Line Tools (`xcode-select --install`)

### USB Communication
- **libusb**: Required for direct USB communication with iOS devices.
  - Debian/Ubuntu: `libusb-1.0-0-dev`
  - Fedora: `libusb-devel`
  - Arch: `libusb`
  - macOS: `brew install libusb`

### Cryptographic Libraries
- **OpenSSL**: Used by various tools for cryptographic operations.
  - Usually pre-installed; install development headers if compiling:
    - Debian/Ubuntu: `libssl-dev`
    - Fedora: `openssl-devel`
    - Arch: `openssl`
  - macOS: Included with system; ensure headers are available via Xcode.

### Python and Python Packages
- **Python**: Version 2.7 or 3.x (some scripts require Python 2).
  - Install via system package manager or official installer.
- **Common Python Packages** (for data protection and keybag scripts):
  - `pycrypto` or `pycryptodome`
  - `construct`
  - `M2Crypto`
  - `progressbar`
  - `setuptools`
  - `pyasn1`
  - `protobuf`
  - Install via `pip` or `easy_install`:
    ```bash
    pip install pycryptodome construct M2Crypto progressbar setuptools pyasn1 protobuf
    ```

### Apple-Specific Toolchains
- **libimobiledevice Stack**: For communication with iOS devices via common protocols.
  - Packages: `libimobiledevice`, `libirecovery`, `libideviceactivation`, `ideviceinstaller`, `ifuse`.
  - Available on most Linux distributions; on macOS via Homebrew: `brew install libimobiledevice`.
- **libplist**: Often a dependency of the above.
- **usbmuxd**: For USB multiplexing (may be included with libimobiledevice).

### Build Tools for Specific Projects
- **Apple cctools-port**: If building custom toolchains for macOS/iOS targets:
  - Clang 10+
  - libstdc++ or libc++ with C++20 support
  - libdispatch-dev and libblocksruntime
  - TAPI library (https://github.com/tpoechtrager/apple-libtapi) for SDKs with .tdb stubs
  - musl-fts (https://github.com/pullmoll/musl-fts) for musl-libc systems
  - Optional: llvm-devel, uuid-devel, xar-devel (for ld64 features)
- **ARM Toolchain**: For modifying assembly in tools like ipwndfu:
  - binutils
  - gcc-arm-embedded (or clang with ARM target)
  - On macOS with Homebrew: `brew install binutils` and `brew cask install gcc-arm-embedded`

### Additional Utilities
- **curl**: For downloading files and interacting with web services.
- **bspatch**: For applying binary patches (used in Legacy iOS Kit).
- **jq**: For JSON parsing (used in some scripts).
- **zenity**: For graphical dialogs (Linux).
- **sshpass**: For non-interactive SSH password supply.
- **darkhttpd**: Simple HTTP server (used in some utilities).
- **Motrix**: aria2c frontend for downloads.
- **usbmuxd2**: Enhanced USB multiplexing (optional).
- **anisette-server**: For bypassing certain Apple services (used in sideloading).
- **AltServer-Linux**: For installing apps via Wi-Fi.
- **Plumesign**: For IPA signing.
- **static-cross-openssh**: For cross-compiled SSH binaries (Linux-only).
- **zip/unzip**: For archive handling.

## Tool-Specific Notes
- **32-bit SSH Ramdisk**: Primarily requires bash and coreutils; loading relies on ipwndfu or similar.
- **checkm8_bootkit**: Needs lilirecovery (included as submodule) and optionally vmacho for payload rebuilding.
- **gaster**: Standard C build; likely requires libusb.
- **DataProtection-noSEP**: Requires Python and the listed packages; C utilities need standard build tools.
- **Legacy iOS Kit**: Aggregates many dependencies; the kit often provides pre-built binaries but source builds may need the above.
- **cctools-port**: See its own detailed dependencies in its README.
- **Wordlist utilities**: No compilation needed; requires shell and core utilities for regeneration scripts.

## Installation Examples
### Ubuntu 22.04+
```bash
sudo apt-get update
sudo apt-get install git build-essential libusb-1.0-0-dev libssl-dev \
    libimobiledevice libirecovery libideviceactivation ideviceinstaller ifuse \
    libplist-dev usbmuxd python3-pip
sudo pip3 install pycryptodome construct M2Crypto progressbar setuptools pyasn1 protobuf
```

### macOS (with Homebrew)
```bash
brew install git libusb openssl libimobiledevice
brew install --cask gcc-arm-embedded  # if needed for ARM toolchain
# Python and packages via official installer or brew
brew install python
pip install pycryptodome construct M2Crypto progressbar setuptools pyasn1 protobuf
```

### Fedora 40+
```bash
sudo dnf install git @development-tools libusb-devel openssl-devel \
    libimobiledevice libirecovery libideviceactivation ideviceinstaller ifuse \
    libplist usbmuxd
sudo pip3 install pycryptodome construct M2Crypto progressbar setuptools pyasn1 protobuf
```

## Verification
After installing dependencies, you can verify by attempting to build or run a simple tool from the collection (e.g., `make` in checkm8_bootkit, or running a Python script from DataProtection-noSEP).

## References
- Individual tool READMEs for specific version requirements.
- Official project websites for each dependency.