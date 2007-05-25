Summary:	A Telepathy account manager
Summary(pl.UTF-8):	Zarządca kont Telepathy
Name:		telepathy-mission-control
Version:	4.22
Release:	1
License:	LGPL
Group:		Libraries
Source0:	http://dl.sourceforge.net/mission-control/%{name}-%{version}.tar.gz
# Source0-md5:	aa8a8264c596c666f886f85356b56e09
URL:		http://mission-control.sourceforge.net/
BuildRequires:	GConf2-devel
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.8
BuildRequires:	dbus-glib-devel >= 0.61
BuildRequires:	gtk-doc-automake
BuildRequires:	libtelepathy-devel
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

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	HTML_DIR=%{_gtkdocdir}

install -d $RPM_BUILD_ROOT%{_libdir}/mission-control
install -d $RPM_BUILD_ROOT%{_datadir}/mission-control
install -d $RPM_BUILD_ROOT%{_datadir}/mission-control/profiles

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
%{_gtkdocdir}/*

%files static
%defattr(644,root,root,755)
%{_libdir}/libmissioncontrol-config.a
%{_libdir}/libmissioncontrol-server.a
%{_libdir}/libmissioncontrol.a
