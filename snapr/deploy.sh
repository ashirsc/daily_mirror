#!/bin/bash

set -o errexit
set -o nounset
set -o pipefail
set -o xtrace

# SYSROOT=/



export PKG_CONFIG_PATH=/Users/drew/workspace/projs/daily_mirror/snapr/opencvbuild/install/lib/pkgconfig/
export PKG_CONFIG_SYSROOT_DIR=/Users/drew/workspace/projs/daily_mirror/snapr/sysroot
# export SYSROOT=/Users/drew/workspace/projs/daily_mirror/snapr/sysroot

# export OPENCV_LINK_PATHS=/Users/drew/workspace/projs/daily_mirror/snapr/opencvbuild/install/lib/arm-linux-gnueabihf
# export OPENCV_INCLUDE_PATHS=/Users/drew/workspace/projs/daily_mirror/snapr/opencvbuild/install/include/opencv4/opencv2
# export OPENCV_LINK_LIBS=libopencv_core,libopencv_highgui,libopencv_imgcodecs,libopencv_imgproc,libopencv_videoio

readonly TARGET_HOST=drew@rasmirror.local
readonly TARGET_PATH=/home/drew/remotebuild
readonly TARGET_ARCH=armv7-unknown-linux-gnueabihf
readonly SOURCE_PATH=./target/${TARGET_ARCH}/release/arm

cargo build --release --target=${TARGET_ARCH}
#rsync ${SOURCE_PATH} ${TARGET_HOST}:${TARGET_PATH}
#ssh -t ${TARGET_HOST} ${TARGET_PATH}
