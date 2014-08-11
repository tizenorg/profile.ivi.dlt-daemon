Name:             dlt
License:          MPL-2.0
Group:            Automotive/GENIVI
Summary:          GENIVI Diagnostic Log and Trace
Version:          2.11.0
Release:          1
Source:           %{name}-%{version}.tar.bz2
BuildRequires:    cmake
BuildRequires:    pkg-config
BuildRequires:    pkgconfig(dbus-1)
BuildRequires:    pkgconfig(zlib)
BuildRequires:    pkgconfig(libsystemd-journal)
Requires(post):   /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
GENIVI Diagnostic Log and Tracing Daemon and Tools

%package daemon
Summary:	GENIVI DLT Daemon

%description daemon
GENIVI Diagnostic Log and Tracing Daemon

%package bin
Summary:	GENIVI DLT utility binaries

%description bin
GENIVI DLT utility binaries

%package test
Summary:	GENIVI DLT test binaries

%description test
GENIVI DLT test binaries

%package -n libdlt
Summary:	GENIVI DLT library

%description -n libdlt
GENIVI DLT library

%package devel
Summary:         Automotive DLT Development Package
Requires:        libdlt = %{version}-%{release}

%description devel
Files needed for developing against the Automotive DLT

%prep
%setup -q -n %{name}-%{version}

%build
mkdir build
cd build

cmake -DWITH_SYSTEMD=ON -DWITH_SYSTEMD_JOURNAL=ON \
      -DWITH_MAN=OFF -DWITH_DLT_EXAMPLES=OFF ..
make %{?jobs:-j %jobs}

%install
rm -rf "$RPM_BUILD_ROOT"
cd build
make install DESTDIR=$RPM_BUILD_ROOT

%post -n libdlt -p /sbin/ldconfig

%postun -n libdlt -p /sbin/ldconfig

%clean
rm -rf "$RPM_BUILD_ROOT"

%files daemon
%defattr(-,root,root,-)
%{_bindir}/dlt-daemon
%config %{_sysconfdir}/dlt.conf
%{_prefix}/lib/systemd/system/dlt.service

%files test
%defattr(-,root,root,-)
%{_bindir}/dlt-test*
%{_datadir}/dlt-filetransfer/*

%files bin
%defattr(-,root,root,-)
%{_bindir}/dlt-adaptor*
%{_bindir}/dlt-convert
%{_bindir}/dlt-dbus
%{_bindir}/dlt-receive
%{_bindir}/dlt-system
%{_bindir}/dlt-control
%config %{_sysconfdir}/dlt-system.conf
%{_prefix}/lib/systemd/system/dlt-adaptor-udp.service
%{_prefix}/lib/systemd/system/dlt-receive.service
%{_prefix}/lib/systemd/system/dlt-system.service
%{_prefix}/lib/systemd/system/dlt-dbus.service
%config %{_sysconfdir}/dlt-dbus.conf

%files -n libdlt
%defattr(-,root,root,-)
%{_libdir}/*so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/dlt/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
