#docker run -it \
#  --device /dev/kvm \
#  --ipc=host \
#  -p 50922:10022 \
#  -v /tmp/.X11-unix:/tmp/.X11-unix \
#   -e "DISPLAY=:1"\
#  -e XDG_RUNTIME_DIR=/run/user/1000 \
#  -e XDG_SESSION_TYPE=wayland \
#  -e WAYLAND_DISPLAY=wayland-1 \
#  -e AUDIO_DRIVER=none \
#  -e EXTRA=" -audiodev none,id=noaudio -device ich9-intel-hda -device hda-duplex,audiodev=noaudio" \
#  docker-osx-checkpoint


runtime_dir="$(mktemp -d)"
chmod 700 "$runtime_dir"

docker run --privileged -i \
    --user "$(id -u):$(id -g)" \
    --device /dev/kvm \
    --security-opt label=disable \
    -p 50922:10022 \
    -v "$runtime_dir:/tmp/xdg-runtime:rw" \
    -v "$XDG_RUNTIME_DIR/$WAYLAND_DISPLAY:/tmp/xdg-runtime/$WAYLAND_DISPLAY:rw" \
    -v "$XDG_RUNTIME_DIR/pulse/native:/tmp/pulse-native:rw" \
    -e XDG_RUNTIME_DIR=/tmp/xdg-runtime \
    -e WAYLAND_DISPLAY="$WAYLAND_DISPLAY" \
    -e GDK_BACKEND=wayland \
    -e LIBGUESTFS_TMPDIR=/tmp \
    -e TMPDIR=/tmp \
    -e AUDIO_DRIVER='pa,server=unix:/tmp/pulse-native' \
    -e GENERATE_UNIQUE=true \
    -e CPU='Haswell-noTSX' \
    -e CPUID_FLAGS='kvm=on,vendor=GenuineIntel,+invtsc,vmware-cpuid-freq=on' \
    -e MASTER_PLIST_URL='https://raw.githubusercontent.com/sickcodes/osx-serial-generator/master/config-custom-sonoma.plist' \
    -e SHORTNAME=sierra \
    -e EXTRA=" -vnc 0.0.0.0:99,password=off" \
    docker-osx-checkpoint

