# cctools-port

## Purpose
Port of Apple's cctools (including ld64) for Linux, BSD, and macOS, enabling the creation of native toolchains for compiling software targeting Apple platforms (macOS, iOS, tvOS, watchOS, etc.) from non-Apple operating systems.

## Key Features
- Supports a wide range of host architectures: x86, x86_64, arm, arm64/AArch64, PowerPC/PowerPC64.
- Targets numerous Apple architectures: armv6, armv7, armv7s, arm64, arm64e, arm64_32 (untested), i386, x86_64, x86_64h, armv6m, armv7k, armv7m, armv7em.
- Supports target operating systems: macOS, iOS, tvOS, watchOS, bridgeOS, Mac Catalyst, iOS Simulator, watchOS Simulator, DriverKit.
- Includes ld64 with support for features like bitcode bundles, random UUIDs, and link-time optimization (when combined with LLVM).
- Provides flexibility to target specific macOS/iOS versions via `-target` flag (e.g., `i386-apple-darwin11`, `x86_64-apple-darwin11`, `arm-apple-darwin11`).
- Integrates with TAPI library for handling .tdb stub SDKs (Xcode 7+).
- Includes optional support for musl-fts on musl-libc based systems.

## Core Components
- Source code for cctools and ld64.
- Build scripts (configure, make).
- Documentation and Travis CI configuration.

## Usage
Typical workflow to build and install the toolchain:

1. **Install TAPI library** (required for SDKs with .tdb stubs):
   ```bash
   git clone https://github.com/tpoechtrager/apple-libtapi.git
   cd apple-libtapi
   ./build.sh   # Adjust INSTALLPREFIX as needed
   ./install.sh
   ```

2. **Build and install cctools and ld64**:
   ```bash
   git clone https://github.com/tpoechtrager/cctools-port.git
   cd cctools-port/cctools
   ./configure \
       [--prefix=/path/to/install] \
       [--with-libtapi=/path/to/libtapi] \
       [--target=<target triple>] \
       [--with-llvm-config=<path>]
   make
   make install
   ```

   Example target for armv7 iOS: `--target=arm-apple-darwin11`.

## Dependencies
- Clang 10+ (for C/C++ compilation).
- libstdc++ or libc++ with C++20 support.
- libdispatch-dev and libblocksruntime (for Grand Central Dispatch and Blocks runtime).
- TAPI library (from https://github.com/tpoechtrager/apple-libtapi) for SDKs with .tdb stubs.
- musl-fts (from https://github.com/pullmoll/musl-fts) for musl-libc based systems.
- Optional but recommended:
  - llvm-devel (for Link Time Optimization support).
  - uuid-devel (for ld64 `-random_uuid` support).
  - llvm-devel + xar-devel (for ld64 `-bitcode_bundle` support; xar from https://github.com/tpoechtrager/xar).

## References
- Original README: `cctools-port/README.md`
- TAPI library: https://github.com/tpoechtrager/apple-libtapi
- musl-fts: https://github.com/pullmoll/musl-fts
- xar: https://github.com/tpoechtrager/xar