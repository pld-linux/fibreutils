%define		_enable_debug_packages	0
%define		subver	2010-03-31
%include	/usr/lib/rpm/macros.perl
Summary:	HP Array Configuration Utility CLI
Name:		fibreutils
Version:	3.1
Release:	2
License:	Proprietary
Group:		Applications/System
Source0:	ftp://ftp.hp.com/pub/softlib/software11/COL28042/co-82357-1/hp-fc-enablement-%{subver}.tar.gz
# NoSource0-md5:	3e05533f8b3f29b08130f59f79ae4657
NoSource:	0
URL:		http://h20000.www2.hp.com/bizsupport/TechSupport/SoftwareDescription.jsp?swItem=co-82357-1
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRequires:	sed >= 4.0
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Miscellaneous scripts and programs to compliment HP supported FC
drivers:
- lssd
- lssg
- adapter_info
- hp_rescan
- scsi_info

%prep
%setup -q -n hp-fc-enablement-%{subver}
%ifarch %{ix86}
ARCH=i386
%endif
%ifarch %{x8664}
ARCH=x86_64
%endif
%ifarch ia64
ARCH=ia64
%endif

# fibreutils
S=%{name}-%{version}-%{release}.$ARCH.rpm
install -d fibreutils
cd fibreutils
rpm2cpio ../$S | cpio -dimu
cd ..

mv fibreutils/opt/hp/hp_fibreutils .
%{__sed} -i -e '
	s#/opt/hp/hp_fibreutils/lssd.cache#/var/cache/lssd.cache#g
	s#/opt/hp/hp_fibreutils/lssg.cache#/var/cache/lssg.cache#
	s#/opt/hp/hp_fibreutils/scsi_info#%{_sbindir}/scsi_info#g
' hp_fibreutils/ls*

# libs (for hpacucli at least)
install -d libs
cd libs
rpm2cpio ../hp-fc-enablement-*.noarch.rpm | cpio -dimu
cd ..
mv libs/opt/hp/hp-fc-enablement/*-libs libs

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_libdir}}
# fibreutils
install -p hp_fibreutils/* $RPM_BUILD_ROOT%{_sbindir}

# qlogic libs
%ifarch %{ix86}
ARCH=ia32
%endif
%ifarch %{x8664}
ARCH=x86_64
%endif
%ifarch ia64
ARCH=ia64
%endif
install -p libs/qlogic-libs/libqlsdm-$ARCH.so $RPM_BUILD_ROOT%{_libdir}/libqlsdm.so

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/adapter_info
%attr(755,root,root) %{_sbindir}/hp_rescan
%attr(755,root,root) %{_sbindir}/lssd
%attr(755,root,root) %{_sbindir}/lssg
%attr(755,root,root) %{_sbindir}/scsi_info
%attr(755,root,root) %{_libdir}/libqlsdm.so
