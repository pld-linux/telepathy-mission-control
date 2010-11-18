#
# Conditional build:
%bcond_without	apidocs		# disable gtk-doc
#
Summary:	A Telepathy account manager
Summary(pl.UTF-8):	Zarządca kont Telepathy
Name:		telepathy-mission-control
Version:	5.6.1
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://telepathy.freedesktop.org/releases/telepathy-mission-control/%{name}-%{version}.tar.gz
# Source0-md5:	0627423bfdf1f5616a4250205ec35b70
URL:		http://mission-control.sourceforge.net/
BuildRequires:	GConf2-devel
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.9
BuildRequires:	dbus-glib-devel >= 0.82
BuildRequires:	docbook-dtd412-xml
BuildRequires:	glib2-devel >= 1:2.24.0
%{?with_apidocs:BuildRequires:	gtk-doc >= 1.3}
BuildRequires:	libtool
BuildRequires:	libxslt-progs
BuildRequires:	pkgconfig
BuildRequires:	python-modules
BuildRequires:	telepathy-glib-devel >= 0.11.9
Conflicts:	libtelepathy < 0.3.3-4
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
Requires:	dbus-glib-devel >= 0.61
Requires:	telepathy-glib-devel >= 0.11.9

%description devel
Header files for mission control library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki mission control.

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
	--disable-static \
	--%{?with_apidocs:en}%{!?with_apidocs:dis}able-gtk-doc \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/mission-control/profiles

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_datadir}/telepathy/{clients,managers}

%{!?with_apidocs:rm -rf $RPM_BUILD_ROOT%{_gtkdocdir}}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

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
%attr(755,root,root) %{_bindir}/mc-tool
%attr(755,root,root) %{_bindir}/mc-wait-for-name
%attr(755,root,root) %{_libexecdir}/mission-control-5
%{_mandir}/man1/mc-tool.1*
%{_mandir}/man1/mc-wait-for-name.1*
%{_mandir}/man8/mission-control-5.8*
%attr(755,root,root) %{_libdir}/libmission-control-plugins.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmission-control-plugins.so.0
%{_datadir}/dbus-1/services/org.freedesktop.Telepathy.AccountManager.service
%{_datadir}/dbus-1/services/org.freedesktop.Telepathy.MissionControl5.service
%dir %{_datadir}/mission-control
%dir %{_datadir}/mission-control/profiles
%dir %{_datadir}/telepathy
%dir %{_datadir}/telepathy/clients
%dir %{_datadir}/telepathy/managers

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmission-control-plugins.so
%{_includedir}/mission-control-5.5
%{_pkgconfigdir}/*.pc

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/mission-control-plugins
%endif
