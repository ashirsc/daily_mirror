#!/bin/bash

set -o errexit
set -o nounset
set -o pipefail
set -o xtrace

SYSROOT=


export PKG_CONFIG_SYSROOT_DIR=${SYSROOT}
export CC=g++

readonly TARGET_HOST=drew@rasmirror.local
readonly TARGET_PATH=/home/drew/remotebuild
readonly TARGET_ARCH=armv7-unknown-linux-gnueabihf
readonly SOURCE_PATH=./target/${TARGET_ARCH}/release/arm

cargo build --release --target=${TARGET_ARCH}
rsync ${SOURCE_PATH} ${TARGET_HOST}:${TARGET_PATH}
ssh -t ${TARGET_HOST} ${TARGET_PATH}