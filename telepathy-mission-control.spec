#
# Conditional build:
%bcond_without	apidocs		# disable gtk-doc
#
Summary:	A Telepathy account manager
Summary(pl.UTF-8):	Zarządca kont Telepathy
Name:		telepathy-mission-control
Version:	4.30
Release:	1
License:	LGPL
Group:		Libraries
Source0:	http://dl.sourceforge.net/mission-control/%{name}-%{version}.tar.gz
# Source0-md5:	316db7a0a99cf6571a48a65cbbd35fe9
URL:		http://mission-control.sourceforge.net/
BuildRequires:	GConf2-devel
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.8
BuildRequires:	dbus-glib-devel >= 0.61
%{?with_apidocs:BuildRequires:	gtk-doc-automake}
BuildRequires:	libtelepathy-devel >= 0.0.50
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

install -d $RPM_BUILD_ROOT%{_libdir}/mission-control
install -d $RPM_BUILD_ROOT%{_datadir}/mission-control
install -d $RPM_BUILD_ROOT%{_datadir}/mission-control/profiles

%{!?with_apidocs:rm -rf $RPM_BUILD_ROOT%{_gtkdocdir}}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README
%attr(755,root,root) %{_bindir}/mc-account
%attr(755,root,root) %{_bindir}/mission-control
%attr(755,root,root) %{_libdir}/*.so.*.*.*
%{_datadir}/dbus-1/services/org.freedesktop.Telepathy.MissionControl.service
%dir %{_libdir}/mission-control
%dir %{_datadir}/mission-control
%dir %{_datadir}/mission-control/profiles

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/*.so
%{_libdir}/*.la
%dir %{_includedir}/libmissioncontrol
%{_includedir}/libmissioncontrol/*.h
%dir %{_includedir}/mission-control
%{_includedir}/mission-control/*.h
%{_pkgconfigdir}/*.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libmissioncontrol-config.a
%{_libdir}/libmissioncontrol-server.a
%{_libdir}/libmissioncontrol.a

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/*
%endif
