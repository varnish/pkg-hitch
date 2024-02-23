#!/usr/bin/env bash

set -e

export RUBYOPT=-W0

user="varnishcache"

function upload {
    distro=$1
    shift
    distrel=$1
    shift
    comp=$1
    shift
    set -x
    package_cloud push $user/$comp/$distro/$distrel $@
    set +x
}

for i in xenial bionic focal jammy; do
    echo "***** Ubuntu - $i *****"
    upload ubuntu $i hitch packages/ubuntu-$i/*.deb
done
for i in stretch buster bullseye; do
    echo "***** Debian - $i *****"
    upload debian $i hitch packages/debian-$i/*.deb
done
for i in 7; do
    echo "***** Centos - $i *****"
    upload el $i hitch packages/centos-$i/*.rpm
done
for i in 8 9; do
    echo "***** Almalinux - $i *****"
    upload el $i hitch packages/almalinux-$i/*.rpm
done
