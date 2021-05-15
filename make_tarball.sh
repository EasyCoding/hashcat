#!/usr/bin/bash
set -e

NAME="hashcat"
VERSION="6.2.1"

TARBALL_DIR="$NAME-$VERSION"
TARBALL_ORIG="$NAME-$VERSION.tar.gz"
TARBALL_NEW="$NAME-$VERSION-clean.tar.xz"

echo "Downloading upstream tarball..."
wget "https://github.com/hashcat/hashcat/archive/v$VERSION/$TARBALL_ORIG" -O "$TARBALL_ORIG" 2>/dev/null

echo "Unpacking upstream tarball..."
tar -xf "$TARBALL_ORIG"

echo "Removing non-free components..."
rm -rf "$TARBALL_DIR/deps/unrar"

echo "Building a new tarball..."
tar -cJf "$TARBALL_NEW" "$TARBALL_DIR"

echo "Performing cleanup..."
rm -f "$TARBALL_ORIG"
rm -rf "$TARBALL_DIR"

echo "Done."
