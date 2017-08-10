Summary: RPM Fusion Server 
Name: fusion-server 
Version: %{VERSION} 
Release: %{RELEASE} 
License: GPL
Group: System/Utilities
URL: http://www.tlantic.com/
Vendor: TLANTIC
Packager: Rodrigo C. Andreoli
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}
Source0: %{name}-%version-%release.tar.gz

%description
Pacote RPM fusion-server

%prep
rm -rf %{name}-%{version}-%release
mkdir -p %{name}-%{version}-%release
tar -zxf $RPM_SOURCE_DIR/%{name}-%{version}-%{release}.tar.gz

%install
mkdir -p $RPM_BUILD_ROOT/opt/fusion/
mkdir -p $RPM_BUILD_ROOT/etc/init.d
mkdir -p $RPM_BUILD_ROOT/etc/httpd/conf
mkdir -p $RPM_BUILD_ROOT/tmp
cd %{name}-%{version}-%{release}
cp -r opt/fusion $RPM_BUILD_ROOT/opt
cp -r etc/init.d/*fusion*  $RPM_BUILD_ROOT/etc/init.d/
cp etc/httpd/conf/httpd.conf $RPM_BUILD_ROOT/tmp/
cp -r etc/init.d/httpd $RPM_BUILD_ROOT/tmp/

%files
%defattr(0755,root,root)
/opt/fusion/*
/etc/init.d/*fusion*
%defattr(0644,root,root)
/tmp/httpd.conf
/tmp/httpd

%post
#config automatic start for fusion
chkconfig --del fusion
chkconfig --add fusion --level 35

#verificar se existe link simbolico, remover e recria-lo
#if [ -e /opt/fusion/running ] ; then
#   echo "Link simbolico /opt/fusion/running existe!"
#   rm /opt/fusion/running -f
#   ln -s x86_64/debug/%{version}/ running
#else
#   cd /opt/fusion
#   ln -s x86_64/debug/%{version}/ running
#   cd -  
#fi

#config httpd for fusion
MOVE_HTTPD="0"
if [ "${MOVE_HTTPD}" == "1" ]
then
   if [ -e /etc/httpd/conf/httpd.conf.unifo2.before.fusion  ]
   then
      cp /etc/httpd/conf/httpd.conf /etc/httpd/conf/httpd.conf.fusion.bkp
      mv -f  /tmp/httpd.conf /etc/httpd/conf/httpd.conf
      cp /etc/init.d/httpd /tmp/httpd_initd.fusion.bkp
      mv -f  /tmp/httpd /etc/init.d/httpd
   else
     cp /etc/httpd/conf/httpd.conf /etc/httpd/conf/httpd.conf.unifo2.before.fusion
     mv -f  /tmp/httpd.conf /etc/httpd/conf/httpd.conf
     cp /etc/init.d/httpd //tmp/httpd_initd.unifo2.before.fusion
     mv -f /tmp/httpd /etc/init.d/httpd
   fi
fi

#apply necessary configurations on fx-boot-config.xml
StoreServerIP=$(/sbin/ifconfig | grep "inet addr" | awk -F: '{print $2}' | awk '{print $1}' | sort | head -1)	

#tratar configuracoes dynamic xml
sed -i 's/\(.*\)\(retailstore-id"\)\( *\)\(value="\)\(.*\)\("\)\(.*\)/\1\2\3\4'0'\6\7/g' /opt/fusion/x86_64/debug/%{version}.%{release}/config/common/fx-boot-dynamic-config.xml.installer
sed -i 's/\(.*\)\(workstation-id"\)\( *\)\(value="\)\(.*\)\("\)\(.*\)/\1\2\3\4'0'\6\7/g' /opt/fusion/x86_64/debug/%{version}.%{release}/config/common/fx-boot-dynamic-config.xml.installer 
sed -i 's/\(.*\)\(server-ip-address"\)\( *\)\(value="\)\(.*\)\("\)\(.*\)/\1\2\3\4'127.0.0.1'\6\7/g' /opt/fusion/x86_64/debug/%{version}.%{release}/config/common/fx-boot-dynamic-config.xml.installer 
cp -a /opt/fusion/x86_64/debug/%{version}.%{release}/config/common/fx-boot-dynamic-config.xml.installer /opt/fusion/x86_64/debug/%{version}.%{release}/config/common/fx-boot-dynamic-config.xml

#tratar configuracoes xsl
sed -i "s/<workstation\ enabled=\"yes\">/<workstation\ enabled=\"no\">/g" /opt/fusion/x86_64/debug/%{version}.%{release}/config/common/fx-boot-config.xsl.installer
sed -i "s/<wmsserver\ enabled=\"no\">/<wmsserver\ enabled=\"yes\">/g" /opt/fusion/x86_64/debug/%{version}.%{release}/config/common/fx-boot-config.xsl.installer

cp -a /opt/fusion/x86_64/debug/%{version}.%{release}/config/common/fx-boot-config.xsl.installer /opt/fusion/x86_64/debug/%{version}.%{release}/config/common/fx-boot-config.xsl

#apply changes on database
COUNTRY=`psql -U postgres novounifodb -A -t -c "select value from businessunitproperty where propertyid=145 and value <> '' limit 1"`

echo "FUSION_NOINSTALL_DB SPEC == ${FUSION_NOINSTALL_DB}"

if [ "${FUSION_NOINSTALL_DB}" == "" ]
then
   if [ -z ${TLAN_CURRENT_VERSION} ]
   then
       /opt/fusion/dbscripts/install_fusiondb.sh %{version}-%{release} ${COUNTRY}
   else
       /opt/fusion/dbscripts/install_fusiondb.sh %{version}-%{release} ${COUNTRY} ${TLAN_CURRENT_VERSION}
   fi
else
   echo "A base de dados do UAAS devera ser atualizada manualmente"
fi

#alterar permissoes da pasta versions
chmod 777 /opt/fusion/versions -R

#criar ficheiro de log script migrate_sequences_unifo2_to_uaas.sh
echo "New Version installed %{version}-%{release}" >> /opt/fusion/tools/rollout/rollout_sequencenumbers.log
chmod 666 /opt/fusion/tools/rollout/rollout_sequencenumbers.log

#verificar
#echo "Verificando..."
#ls /opt/fusion/

