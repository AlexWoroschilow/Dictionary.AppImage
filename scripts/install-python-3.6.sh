#! /bin/bash

set -ex

PYTHON_NAME="python-3.7"
PYTHON_VERSION="3.7.6"
PYTHON_PREFIX="$@"

PYTHON_PREFIX_LIB="${PYTHON_PREFIX}/lib"
PYTHON_PREFIX_TEMP="${PYTHON_PREFIX}/tmp"

GLIBC_VERSION=`getconf GNU_LIBC_VERSION`

#which yum > /dev/null && yum install gcc
#which yum > /dev/null && yum install make
#which yum > /dev/null && yum install wget
#which yum > /dev/null && yum install tar

which zypper > /dev/null && sudo zypper --non-interactive install tar
which zypper > /dev/null && sudo zypper --non-interactive install wget
which zypper > /dev/null && sudo zypper --non-interactive install make
which zypper > /dev/null && sudo zypper --non-interactive install llvm
which zypper > /dev/null && sudo zypper --non-interactive install liblzma5
which zypper > /dev/null && sudo zypper --non-interactive install libncurses5
which zypper > /dev/null && sudo zypper --non-interactive install python3-devel
which zypper > /dev/null && sudo zypper --non-interactive install libopenssl-devel
which zypper > /dev/null && sudo zypper --non-interactive install zlib-devel
which zypper > /dev/null && sudo zypper --non-interactive install libbz2-devel
which zypper > /dev/null && sudo zypper --non-interactive install libxml2-devel
which zypper > /dev/null && sudo zypper --non-interactive install libffi-devel
which zypper > /dev/null && sudo zypper --non-interactive install tk-devel


#which apt-get && sudo apt-get install --no-install-recommends make build-essential libssl-dev \
#    zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
#    libncurses5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev

ls -lah ${PYTHON_PREFIX} > /dev/null || mkdir -p ${PYTHON_PREFIX}
ls -lah ${PYTHON_PREFIX_TEMP} > /dev/null || mkdir ${PYTHON_PREFIX_TEMP}

cd ${PYTHON_PREFIX_TEMP}

wget -O Python-${PYTHON_VERSION}.tar.xz -c https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tar.xz

tar xJf Python-${PYTHON_VERSION}.tar.xz

cd ${PYTHON_PREFIX_TEMP}/Python-${PYTHON_VERSION}
./configure \
    --prefix=${PYTHON_PREFIX} \
    --libdir=${PYTHON_PREFIX_LIB}

make -j8 
make -j8 install

rm -rf ${PYTHON_PREFIX_TEMP}
