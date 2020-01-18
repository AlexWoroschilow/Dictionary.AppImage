#! /bin/bash

set -ex

PYTHON_NAME="python-3.6"
PYTHON_VERSION="3.6.10"
PYTHON_PREFIX="$@"

PYTHON_PREFIX_LIB="${PYTHON_PREFIX}/lib"
PYTHON_PREFIX_TEMP="${PYTHON_PREFIX}/tmp"

GLIBC_VERSION=`getconf GNU_LIBC_VERSION`

#which yum && yum install gcc
#which yum && yum install make
#which yum && yum install wget
#which yum && yum install tar

#which zypper && zypper install gcc
#which zypper && zypper install make
#which zypper && zypper install wget
#which zypper && zypper install tar

which apt-get && sudo apt-get install --no-install-recommends make build-essential libssl-dev \
    zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
    libncurses5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev

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
