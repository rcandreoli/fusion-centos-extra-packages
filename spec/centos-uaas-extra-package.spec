Summary: RPM Centos Extra Packages for Server 
Name: centos-uaas-extra-package
Version: %{VERSION} 
Release: %{RELEASE}
License: GPL
Group: Sonae/Fusion
URL: http://www.tlantic.com/
Vendor: TLANTIC
Packager: Rodrigo C. Andreoli
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}
Source0: %{name}-%{version}-%{release}.tar.gz
%global _enable_debug_package 0
%global debug_package %{nil}
%global __os_install_post /usr/lib/rpm/brp-compress %{nil}
%define __check_files %{nil}


%description
Pacote RPM Centos Extra Packages for Server 

%prep
rm -rf $RPM_BUILD_DIR/%{name}-%{version}-%{release}
mkdir -p $RPM_BUILD_DIR/%{name}-%{version}-%{release}
#tar -zxf $RPM_SOURCE_DIR/%{name}-%{version}-%{release}.tar.gz -C $RPM_BUILD_DIR/%{name}-%{version}-%{release}
cp $RPM_SOURCE_DIR/%{name}-%{version}-%{release}.tar.gz $RPM_BUILD_DIR/%{name}-%{version}-%{release}/

rm -rf /tmp/extrap
mkdir -p /tmp/extrap/
tar -zxf $RPM_SOURCE_DIR/%{name}-%{version}-%{release}.tar.gz -C /tmp/extrap/
`find /tmp/extrap -type f -print | sed "s/\/tmp\/extrap//1"    > /tmp/%{name}-%{version}-%{release}-files`

%install
export DONT_STRIP=1
rm -rf $RPM_BUILD_ROOT/
mkdir -p $RPM_BUILD_ROOT/
cp -rp $RPM_BUILD_DIR/* $RPM_BUILD_ROOT/

%files
%defattr(-,root,root)
/

%post
#nothingo to do after install
cd /%{name}-%{version}-%{release}
#tar zcvf %{name}-%{version}-%{release}.tar.gz *
tar zxvf %{name}-%{version}-%{release}.tar.gz -C /
rm -rf /%{name}-%{version}-%{release}

md5_check=`md5sum -c /%{name}-%{version}-%{release}.md5sum |grep FAILED|wc -l`
if [ "${md5_check}" == "0" ];then
   echo -e "ALL FILES HAVE BEEN SUCESSFULLY INSTALLED!"
else
   echo -e "FAILED - Please Check - ERROR"
   echo -e "Some files is NOTOK:"
   md5sum -c /%{name}-%{version}-%{release}.md5sum |grep FAILED
fi

mv /%{name}-%{version}-%{release}.md5sum /tmp/%{name}-%{version}-%{release}.md5sum.log
rpm -qa |grep %{name}
echo "RPM: %{name} -  RPM installation completed successfully!!"

%clean
rm -rf $RPM_BUILD_DIR
rm -rf $RPM_BUILD_ROOT

%changelog
* Mon Jul 31 2017 Rodrigo Cezar Andreoli <rodrigoa@tlantic.com>
- criacao do spec
