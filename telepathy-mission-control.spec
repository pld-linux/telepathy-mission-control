#
# Conditional build:
%bcond_without	apidocs		# disable gtk-doc
#
Summary:	A Telepathy account manager
Summary(pl.UTF-8):	Zarządca kont Telepathy
Name:		telepathy-mission-control
Version:	5.2.0
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://telepathy.freedesktop.org/releases/telepathy-mission-control/%{name}-%{version}.tar.gz
# Source0-md5:	dc7ce2105d1f569a1a6f7db06be4bc68
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
%{__aclocal} -I m4
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
%attr(755,root,root) %{_bindir}/mc-account-convert
%attr(755,root,root) %{_bindir}/mc-tool
%attr(755,root,root) %{_bindir}/mc-wait-for-name
%attr(755,root,root) %{_libexecdir}/mission-control-5
%{_mandir}/man1/mc-account-convert.1*
%{_mandir}/man1/mc-tool.1*
%{_mandir}/man1/mc-wait-for-name.1*
%{_mandir}/man8/mission-control-5.8*
%attr(755,root,root) %{_libdir}/libmcclient-%{version}.so
%{_datadir}/dbus-1/services/org.freedesktop.Telepathy.AccountManager.service
%{_datadir}/dbus-1/services/org.freedesktop.Telepathy.MissionControl5.service
%dir %{_datadir}/mission-control
%dir %{_datadir}/mission-control/profiles

%files static
%defattr(644,root,root,755)
%{_libdir}/libmcclient.a

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmcclient.so
%{_libdir}/libmcclient.la
%dir %{_includedir}/libmcclient/_gen
%{_includedir}/libmcclient/_gen/*.h
%dir %{_includedir}/libmcclient/
%{_includedir}/libmcclient/*.h
%{_pkgconfigdir}/*.pc

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libmcclient
%{_gtkdocdir}/libmissioncontrol-server
%endif
