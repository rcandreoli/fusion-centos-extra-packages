#!/bin/sh

export MAJOR=1      # major version
export MINOR=0      # minor version
export RELEASE=0    # changes when the version has new features
export FIX=0       # changes when the version has fixes
export VERSION=${MAJOR}.${MINOR}.${RELEASE}.${FIX}
export PKGVER=1

BASE_DIR=`pwd -P`
DELIVERED_FOLDER="delivered_packages"
BINARIES_FOLDER="unpacked_packages_${VERSION}"
RPMS_SOURCE="/root/rpmbuild/SOURCES"
SPECS_DIR="../spec"
RPMS_BUILD="/root/rpmbuild/BUILD"
RPMS_DIR="/root/rpmbuild/RPMS/x86_64"
RELEASE_DIR="/root/entregas/centos_extra_package"
DIR_TMP="/tmp"


mkdir -p $RELEASE_DIR



#pacotes extras ja entregues:

P1="CENTOS_FUSION_EXTRA_COMPONENTS_20160519.tar.gz"
P2="CENTOS_FUSION_EXTRA_COMPONENTS_20170305.tar.gz"
P3="CENTOS_FUSION_EXTRA_COMPONENTS_20170420_v3.tar.gz"
P4="CENTOS_FUSION_EXTRA_COMPONENTS_20170518_sqlite_3.18.tar.gz"

#limpa pasta dos pacotes descompactados
rm -rf ../${BINARIES_FOLDER}
mkdir ../${BINARIES_FOLDER}

#--pacote 1 - P1
#copiar pacote e descomprimir para pasta usr
#tratamento para o pacote 1, criar diretoria usr
mkdir -p ../${BINARIES_FOLDER}/usr
cp ../${DELIVERED_FOLDER}/${P1} ../${BINARIES_FOLDER}/usr/
cd ../${BINARIES_FOLDER}/usr
tar zxvf ${P1}
if [ $? != 0 ];then
   echo -e "ERROR - Stop process - Decompress Fail - ${P1}"
   exit 1
fi
rm -f ${P1}
cd -

#--pacote 2 - P2
#copiar pacote e descomprimir para pasta 
cp ../${DELIVERED_FOLDER}/${P2} ../${BINARIES_FOLDER}/
cd ../${BINARIES_FOLDER}/
tar zxvf ${P2}
if [ $? != 0 ];then
   echo -e "ERROR - Stop process - Decompress Fail - ${P2}"
   exit 1
fi
rm -f ${P2}
cd -

#--pacote 3 - P3
#copiar pacote e descomprimir para pasta
cp ../${DELIVERED_FOLDER}/${P3} ../${BINARIES_FOLDER}/
cd ../${BINARIES_FOLDER}/
tar zxvf ${P3}
if [ $? != 0 ];then
   echo -e "ERROR - Stop process - Decompress Fail - ${P3}"
   exit 1
fi
rm -f ${P3}
cd -

#--pacote 4 - P4
#copiar pacote e descomprimir para pasta
cp ../${DELIVERED_FOLDER}/${P4} ../${BINARIES_FOLDER}/
cd ../${BINARIES_FOLDER}/
tar zxvf ${P4}
if [ $? != 0 ];then
   echo -e "ERROR - Stop process - Decompress Fail - ${P4}"
   exit 1
fi
rm -f ${P4}
cd -

#verificar todos os ficheiros que serao empacotados
cd ../${BINARIES_FOLDER}/
find  -type f -print0 |xargs -0 md5sum > ../centos-uaas-extra-package-${VERSION}-${PKGVER}.md5sum
sed "s/\ .\//\ \//g" ../centos-uaas-extra-package-${VERSION}-${PKGVER}.md5sum > centos-uaas-extra-package-${VERSION}-${PKGVER}.md5sum
rm -f ../centos-uaas-extra-package-${VERSION}-${PKGVER}.md5sum .
cd - 

#gerar rpm
cd ../${BINARIES_FOLDER}/
tar -zcvf ${RPMS_SOURCE}/centos-uaas-extra-package-${VERSION}-${PKGVER}.tar.gz *
cd -

rpmbuild -bb -D "VERSION ${VERSION}" -D "RELEASE ${PKGVER}" ${SPECS_DIR}/centos-uaas-extra-package.spec

mv $RPMS_DIR/centos-uaas-extra-package-${VERSION}-${PKGVER}*.rpm ${RELEASE_DIR}/

#limpando diretorias
rm -f ${RPMS_SOURCE}/fusion-server-${VERSION}-${PKGVER}.tar.gz
rm -rf ${RPMS_BUILD}/fusion-server-${VERSION}-${PKGVER}
rm -rf ../${BINARIES_FOLDER}

echo -e "####                  | "
echo -e "####Fim do Processo  .|."
