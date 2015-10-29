# These are on by default, unless explicitly disabled.
%bcond_without lua
%bcond_without pulse
%bcond_without ecore
%bcond_without glib
%bcond_without dbus
%bcond_without telephony
%bcond_without websockets
%bcond_without smack
%bcond_without sysmon

# These are off by default, unless explicitly enabled.
#
# Notes:
#   By default we build with distro-default compilation flags which
#   enables optimizations. If you want to build with full debugging
#   ie. with optimization turned off and full debug info (-O0 -g3)
#   pass '--with debug' to rpmbuild on the command line. Similary
#   you can chose to compile with/without pulse, ecore, glib, qt,
#   dbus, and telephony support.
#
#   qt is the macro for controlling Qt4 support, which is not supported
#   in Tizen any more. qt5 is the corrsponding macro for controlling
#   Qt5 support.
#
#%bcond_with qt
#%bcond_with debug

Summary: Resource policy framework
Name: murphy
Version: 0.0.74
Release: 1
License: BSD-3-Clause
Group: System/Service
URL: http://01.org/murphy/
Source0: %{name}-%{version}.tar.gz
Source1001: %{name}.manifest

Requires(post): /bin/systemctl
#Requires(post): libcap-tools
Requires(postun): /bin/systemctl

BuildRequires: flex
BuildRequires: bison
BuildRequires: pkgconfig(lua)
BuildRequires: pkgconfig(libsystemd-daemon)
BuildRequires: pkgconfig(libsystemd-journal)
#BuildRequires: pkgconfig(libcap)
BuildRequires: pkgconfig(libtzplatform-config)
#%if %{with pulse}
#BuildRequires: pkgconfig(libpulse)
#%endif
#%if %{with ecore}
#BuildRequires: pkgconfig(ecore)
#BuildRequires: mesa-libEGL
#BuildRequires: mesa-libGLESv2
#%endif
%if %{with glib}
BuildRequires: pkgconfig(glib-2.0)
%endif
%if %{with qt}
BuildRequires: pkgconfig(QtCore)
%endif
%if %{with dbus}
BuildRequires: pkgconfig(dbus-1)
%endif
#%if %{with telephony}
#BuildRequires: pkgconfig(ofono)
#%endif
#%if %{with websockets}
#BuildRequires: libwebsockets-devel
#%endif
BuildRequires: pkgconfig(json-c)
#%if %{with smack}
#BuildRequires: pkgconfig(libsmack)
#%endif

%description
This package contains the basic Murphy daemon.

%package devel
Summary: The header files and libraries needed for Murphy development
Group: System/Libraries
Requires: %{name} = %{version}-%{release}
Requires: libjson-devel

%description devel
This package contains header files and libraries necessary for development.

%package doc
Summary: Documentation for Murphy
Group: SDK/Documentation

%description doc
This package contains documentation.

#%if %{with pulse}
#%package pulse
#Summary: Murphy PulseAudio mainloop integration
#Group: System/Libraries
#Requires: %{name} = %{version}-%{release}

#%description pulse
#This package contains the Murphy PulseAudio mainloop integration runtime files.

#%package pulse-devel
#Summary: Murphy PulseAudio mainloop integration development files
#Group: System/Libraries
#Requires: %{name}-pulse = %{version}-%{release}
#Requires: %{name} = %{version}-%{release}

#%description pulse-devel
#This package contains the Murphy PulseAudio mainloop integration development
#files.
#%endif

#%if %{with ecore}
#%package ecore
#Summary: Murphy EFL/ecore mainloop integration
#Group: System/Libraries
#Requires: %{name} = %{version}-%{release}

#%description ecore
#This package contains the Murphy EFL/ecore mainloop integration runtime files.

#%package ecore-devel
#Summary: Murphy EFL/ecore mainloop integration development files
#Group: System/Libraries
#Requires: %{name}-ecore = %{version}-%{release}
#Requires: %{name} = %{version}-%{release}

#%description ecore-devel
#This package contains the Murphy EFL/ecore mainloop integration development
#files.
#%endif

%if %{with glib}
%package glib
Summary: Murphy glib mainloop integration
Group: System/Libraries
Requires: %{name} = %{version}-%{release}

%description glib
This package contains the Murphy glib mainloop integration runtime files.

%package glib-devel
Summary: Murphy glib mainloop integration development files
Group: System/Libraries
Requires: %{name}-glib = %{version}-%{release}
Requires: %{name} = %{version}-%{release}

%description glib-devel
This package contains the Murphy glib mainloop integration development
files.
%endif

%if %{with qt}
%package qt
Summary: Murphy Qt mainloop integration
Group: System/Libraries
Requires: %{name} = %{version}-%{release}

%description qt
This package contains the Murphy Qt mainloop integration runtime files.

%package qt-devel
Summary: Murphy Qt mainloop integration development files
Group: System/Libraries
Requires: %{name}-qt = %{version}-%{release}
Requires: %{name} = %{version}-%{release}

%description qt-devel
This package contains the Murphy Qt mainloop integration development
files.
%endif

%package tests
Summary: Various test binaries for Murphy
Group: System/Testing
Requires: %{name} = %{version}-%{release}
Requires: %{name} = %{version}-%{release}

%description tests
This package contains various test binaries for Murphy.

%prep
%setup -q
cp %{SOURCE1001} .

%build
%if %{with debug}
export CFLAGS="-O0 -g3"
V="V=1"
%endif

CONFIG_OPTIONS=""
DYNAMIC_PLUGINS="domain-control"

#%if %{with pulse}
#CONFIG_OPTIONS="$CONFIG_OPTIONS --enable-gpl --enable-pulse"
#%else
CONFIG_OPTIONS="$CONFIG_OPTIONS --disable-pulse"
#%endif

#%if %{with ecore}
#CONFIG_OPTIONS="$CONFIG_OPTIONS --enable-gpl --enable-ecore"
#%else
CONFIG_OPTIONS="$CONFIG_OPTIONS --disable-ecore"
#%endif

%if %{with glib}
CONFIG_OPTIONS="$CONFIG_OPTIONS --enable-gpl --enable-glib"
%else
CONFIG_OPTIONS="$CONFIG_OPTIONS --disable-glib"
%endif

%if %{with qt}
CONFIG_OPTIONS="$CONFIG_OPTIONS --enable-qt"
%else
CONFIG_OPTIONS="$CONFIG_OPTIONS --disable-qt"
%endif

%if %{with dbus}
CONFIG_OPTIONS="$CONFIG_OPTIONS --enable-gpl --enable-libdbus"
%else
CONFIG_OPTIONS="$CONFIG_OPTIONS --disable-libdbus"
%endif

#%if %{with telephony}
#CONFIG_OPTIONS="$CONFIG_OPTIONS --enable-gpl --enable-telephony"
#%else
CONFIG_OPTIONS="$CONFIG_OPTIONS --disable-telephony"
#%endif

#%if %{with websockets}
#CONFIG_OPTIONS="$CONFIG_OPTIONS --enable-websockets"
#%else
CONFIG_OPTIONS="$CONFIG_OPTIONS --disable-websockets"
#%endif

#%if %{with smack}
#CONFIG_OPTIONS="$CONFIG_OPTIONS --enable-smack"
#%else
CONFIG_OPTIONS="$CONFIG_OPTIONS --disable-smack"
#%endif

./bootstrap
%configure $CONFIG_OPTIONS --with-dynamic-plugins=$DYNAMIC_PLUGINS
%__make clean
%__make %{?_smp_mflags} $V

%install
rm -rf %{buildroot}
%make_install

# Make sure we have a plugin dir even if all the basic plugins
# are configured to be built in.
mkdir -p %{buildroot}%{_libdir}/murphy/plugins

# Get rid of any *.la files installed by libtool.
rm -f %{buildroot}%{_libdir}/*.la

# Clean up also the murphy DB installation.
rm -f %{buildroot}%{_libdir}/murphy/*.la

# Generate list of linkedin plugins (depends on the configuration).
outdir="`pwd`"
pushd %{buildroot}
find ./%{_libdir} -name libmurphy-plugin-*.so* | \
sed 's#^./*#/#g' > $outdir/filelist.plugins-base
popd
echo "Found the following linked-in plugin files:"
cat $outdir/filelist.plugins-base | sed 's/^/    /g'

# Generate list of header files, filtering ones that go to subpackages.
outdir="`pwd`"
pushd %{buildroot}
find ./%{_includedir}/murphy | \
grep -E -v '((pulse)|(ecore)|(glib)|(qt))-glue' | \
sed 's#^./*#/#g' > $outdir/filelist.devel-includes
popd

# Replace the default sample/test config files with the packaging ones.
rm -f %{buildroot}%{_sysconfdir}/murphy/*
cp packaging/murphy-lua.conf %{buildroot}%{_sysconfdir}/murphy/murphy.conf

# Copy tmpfiles.d config file in place
mkdir -p %{buildroot}%{_tmpfilesdir}
cp packaging/murphyd.conf %{buildroot}%{_tmpfilesdir}

# Copy the systemd files in place.
#mkdir -p %%{buildroot}%%{_unitdir}
mkdir -p %{buildroot}%{_unitdir_user}
cp packaging/murphyd.service %{buildroot}%{_unitdir_user}

%if %{with dbus}
mkdir -p %{buildroot}%{_sysconfdir}/dbus-1/system.d
sed "s/@TZ_SYS_USER_GROUP@/%{TZ_SYS_USER_GROUP}/g" \
    packaging/org.Murphy.conf.in > packaging/org.Murphy.conf
cp packaging/org.Murphy.conf \
    %{buildroot}%{_sysconfdir}/dbus-1/system.d/org.Murphy.conf
%endif

%clean
rm -rf %{buildroot}

%post
/bin/systemctl --user enable --global murphyd.service
setcap 'cap_net_admin=+ep' %{_bindir}/murphyd
ldconfig

%postun
if [ "$1" = "0" ]; then
systemctl --user disable --global murphyd.service
fi
ldconfig

%if %{with glib}
%post glib
ldconfig

%postun glib
ldconfig
%endif

#%if %{with pulse}
#%post pulse
#ldconfig

#%postun pulse
#ldconfig
#%endif

#%if %{with ecore}
#%post ecore
#ldconfig

#%postun ecore
#ldconfig
#%endif

%if %{with qt}
%post qt
ldconfig

%postun qt
ldconfig
%endif

%files -f filelist.plugins-base
%defattr(-,root,root,-)
%manifest murphy.manifest
%{_bindir}/murphyd
%config %{_sysconfdir}/murphy
%{_unitdir_user}/murphyd.service
%{_tmpfilesdir}/murphyd.conf
%if %{with dbus}
%{_sysconfdir}/dbus-1/system.d
%config %{_sysconfdir}/dbus-1/system.d/org.Murphy.conf
%endif
#%if %{with websockets}
#%{_datadir}/murphy
#%endif

%{_libdir}/libmurphy-common.so.*
%{_libdir}/libmurphy-core.so.*
%{_libdir}/libmurphy-resolver.so.*
%{_libdir}/libmurphy-resource.so.*
%{_libdir}/libmurphy-resource-backend.so.*
%if %{with lua}
%{_libdir}/libmurphy-lua-utils.so.*
%{_libdir}/libmurphy-lua-decision.so.*
%endif
%{_libdir}/libmurphy-domain-controller.so.*
%{_libdir}/murphy/*.so.*
%{_libdir}/libbreedline*.so.*
%if %{with dbus}
%{_libdir}/libmurphy-libdbus.so.*
%{_libdir}/libmurphy-dbus-libdbus.so.*
%endif
%if %{with sysmon}
%{_libdir}/libmurphy-libdbus.so.*
%endif

%{_libdir}/murphy/plugins/plugin-domain-control.so
%{_libdir}/murphy/plugins/plugin-resource-native.so

%files devel -f filelist.devel-includes
%defattr(-,root,root,-)
%{_includedir}/murphy-db
%{_libdir}/libmurphy-common.so
%{_libdir}/libmurphy-core.so
%{_libdir}/libmurphy-resolver.so
%{_libdir}/libmurphy-resource.so
%{_libdir}/libmurphy-resource-backend.so
%if %{with lua}
%{_libdir}/libmurphy-lua-utils.so
%{_libdir}/libmurphy-lua-decision.so
%endif
%{_libdir}/libmurphy-domain-controller.so
%{_libdir}/murphy/*.so
%{_libdir}/pkgconfig/murphy-common.pc
%{_libdir}/pkgconfig/murphy-core.pc
%{_libdir}/pkgconfig/murphy-resolver.pc
%if %{with lua}
%{_libdir}/pkgconfig/murphy-lua-utils.pc
%{_libdir}/pkgconfig/murphy-lua-decision.pc
%endif
%{_libdir}/pkgconfig/murphy-domain-controller.pc
%{_libdir}/pkgconfig/murphy-db.pc
%{_libdir}/pkgconfig/murphy-resource.pc
%{_includedir}/breedline
%{_libdir}/libbreedline*.so
%{_libdir}/pkgconfig/breedline*.pc
%if %{with dbus}
%{_libdir}/libmurphy-libdbus.so
%{_libdir}/libmurphy-dbus-libdbus.so
%{_libdir}/pkgconfig/murphy-libdbus.pc
%{_libdir}/pkgconfig/murphy-dbus-libdbus.pc
%endif

%files doc
%defattr(-,root,root,-)
%doc %{_datadir}/doc/murphy/AUTHORS
%doc %{_datadir}/doc/murphy/CODING-STYLE
%doc %{_datadir}/doc/murphy/ChangeLog
%doc %{_datadir}/doc/murphy/NEWS
%doc %{_datadir}/doc/murphy/README
%license COPYING LICENSE-BSD

#%if %{with pulse}
#%files pulse
#%defattr(-,root,root,-)
#%{_libdir}/libmurphy-pulse.so.*
#%manifest murphy.manifest

#%files pulse-devel
#%defattr(-,root,root,-)
#%{_includedir}/murphy/common/pulse-glue.h
#%{_libdir}/libmurphy-pulse.so
#%{_libdir}/pkgconfig/murphy-pulse.pc
#%endif

#%if %{with ecore}
#%files ecore
#%defattr(-,root,root,-)
#%{_libdir}/libmurphy-ecore.so.*
#%manifest murphy.manifest

#%files ecore-devel
#%defattr(-,root,root,-)
#%{_includedir}/murphy/common/ecore-glue.h
#%{_libdir}/libmurphy-ecore.so
#%{_libdir}/pkgconfig/murphy-ecore.pc
#%endif

%if %{with glib}
%files glib
%defattr(-,root,root,-)
%{_libdir}/libmurphy-glib.so.*
%manifest murphy.manifest

%files glib-devel
%defattr(-,root,root,-)
%{_includedir}/murphy/common/glib-glue.h
%{_libdir}/libmurphy-glib.so
%{_libdir}/pkgconfig/murphy-glib.pc
%endif

%if %{with qt}
%files qt
%defattr(-,root,root,-)
%{_libdir}/libmurphy-qt.so.*
%manifest murphy.manifest

%files qt-devel
%defattr(-,root,root,-)
%{_includedir}/murphy/common/qt-glue.h
%{_libdir}/libmurphy-qt.so
%{_libdir}/pkgconfig/murphy-qt.pc
%endif

%files tests
%defattr(-,root,root,-)
%{_bindir}/resource-client
%{_bindir}/resource-api-test
%{_bindir}/resource-api-fuzz
%{_bindir}/resource-context-create
%{_bindir}/test-domain-controller
%{_bindir}/murphy-console
%manifest murphy.manifest

