#
# Conditional build:
%bcond_without	apidocs		# disable gtk-doc
#
Summary:	A Telepathy account manager
Summary(pl.UTF-8):	Zarządca kont Telepathy
Name:		telepathy-mission-control
Version:	4.64
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://dl.sourceforge.net/mission-control/%{name}-%{version}.tar.gz
# Source0-md5:	e232060c1b6cf9afa84160a1d2d405fb
URL:		http://mission-control.sourceforge.net/
BuildRequires:	GConf2-devel
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.8
BuildRequires:	dbus-glib-devel >= 0.61
%{?with_apidocs:BuildRequires:	gtk-doc-automake}
BuildRequires:	libtelepathy-devel >= 0.0.54
BuildRequires:	libtool
BuildRequires:	libxslt-progs
BuildRequires:	pkgconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
An account manager for Telepathy.

%description -l pl.UTF-8
Zarządca kont dla Telepathy.

%package devel
Summary:	Header files for mission control library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki mission control
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for mission control library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki mission control.

%package static
Summary:	Static mission control library
Summary(pl.UTF-8):	Statyczna biblioteka mission control
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static mission control library.

%description static -l pl.UTF-8
Statyczna biblioteka mission control.

%package apidocs
Summary:	mission control library API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki mission control
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
mission control library API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki mission control.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--%{?with_apidocs:en}%{!?with_apidocs:dis}able-gtk-doc \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_datadir}/mission-control
install -d $RPM_BUILD_ROOT%{_datadir}/mission-control/profiles

%{!?with_apidocs:rm -rf $RPM_BUILD_ROOT%{_gtkdocdir}}

%clean
rm -rf $RPM_BUILD_ROOT

%pretrans
# this needs to be a file
if [ -d %{_libexecdir}/mission-control ]; then
	rm -rf %{_libexecdir}/mission-control
fi

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README
%attr(755,root,root) %{_bindir}/mc-account
%attr(755,root,root) %{_libexecdir}/mission-control
%attr(755,root,root) %{_libdir}/libmissioncontrol-client.so.*.*.*
%attr(755,root,root) %{_libdir}/libmissioncontrol-server.so.*.*.*
%attr(755,root,root)    %{_libdir}/libmcclient.so.*.*.*
%{_datadir}/dbus-1/services/org.freedesktop.Telepathy.MissionControl.service
%dir %{_datadir}/mission-control
%dir %{_datadir}/mission-control/profiles


%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmissioncontrol-client.so
%attr(755,root,root) %{_libdir}/libmissioncontrol-server.so
%{_libdir}/libmissioncontrol-client.la
%{_libdir}/libmissioncontrol-server.la
%{_libdir}/libmcclient.la
%{_libdir}/libmcclient.so
%dir %{_includedir}/libmcclient/_gen
%{_includedir}/libmcclient/_gen/*.h
%dir %{_includedir}/libmcclient/
%{_includedir}/libmcclient/*.h
%dir %{_includedir}/libmissioncontrol
%{_includedir}/libmissioncontrol/*.h
%dir %{_includedir}/libmissioncontrol/_gen
%{_includedir}/libmissioncontrol/_gen/*.h
%dir %{_includedir}/mission-control
%{_includedir}/mission-control/*.h
%dir %{_includedir}/mission-control/_gen/
%{_includedir}/mission-control/_gen/*.h
%{_pkgconfigdir}/*.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libmissioncontrol-client.a
%{_libdir}/libmissioncontrol-server.a
%{_libdir}/libmcclient.a

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libmissioncontrol
%{_gtkdocdir}/libmissioncontrol-server
%endif
