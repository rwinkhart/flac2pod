#!/usr/bin/env bash

echo -e '\n\nthe value entered in this field will only affect the version reported to the package manager - the latest source is used regardless\n'
read -r -p "version number: " version
read -r -p "revision number: " revision

echo -e '\noptions (please enter the number only):'
echo -e '\n1. gitHub release tag\n2. local\n'
read -r -p "source (for build scripts): " source

if [ "$source" == "1" ]; then
    source='https://github.com/rwinkhart/flac2pod/releases/download/v$pkgver/flac2pod-$pkgver.tar.xz'
else
    source=local://flac2pod-"$version".tar.xz
fi

# generic packaging
echo -e '\npackaging as generic...\n'
mkdir -p output/generictemp/usr/{bin,lib/flac2pod}
cp -r lib/. output/generictemp/usr/lib/flac2pod/
ln -s /usr/lib/flac2pod/flac2pod.py output/generictemp/usr/bin/flac2pod
ln -s /usr/lib/flac2pod/flac2pod-artconvert.py output/generictemp/usr/bin/flac2pod-artconvert
ln -s /usr/lib/flac2pod/flac2pod-flacgain.py output/generictemp/usr/bin/flac2pod-flacgain
cp -r share output/generictemp/usr/
tar -C output/generictemp -cvJf output/flac2pod-"$version".tar.xz usr/
rm -rf output/generictemp
sha512="$(sha512sum output/flac2pod-"$version".tar.xz | awk '{print $1;}')"
echo -e "\nsha512 sum:\n$sha512"
echo -e "\ngeneric packaging complete\n"

# PKGBUILD creation
echo -e '\ngenerating PKGBUILD...'
echo "# Maintainer: Randall Winkhart <idgr at tutanota dot com>
pkgname=flac2pod
pkgver="$version"
pkgrel="$revision"
pkgdesc='Converts your FLAC library to be iPod-ready'
url='https://github.com/rwinkhart/flac2pod'
arch=('any')
license=('GPL2')
depends=(ffmpeg flac python python-mutagen python-pillow)
source=(\""$source"\")
sha512sums=('"$sha512"')

package() {
    tar xf flac2pod-"\"\$pkgver\"".tar.xz -C "\"\${pkgdir}\""
}
" > output/PKGBUILD
    echo -e "\nPKGBUILD generated\n"
