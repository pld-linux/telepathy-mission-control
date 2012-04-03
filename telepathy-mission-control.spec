#
# Conditional build:
%bcond_without	apidocs		# disable gtk-doc
#
Summary:	A Telepathy account manager
Summary(pl.UTF-8):	Zarządca kont Telepathy
Name:		telepathy-mission-control
Version:	5.12.0
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://telepathy.freedesktop.org/releases/telepathy-mission-control/%{name}-%{version}.tar.gz
# Source0-md5:	f39dcfef785a37dc21efa9af06be2e61
URL:		http://mission-control.sourceforge.net/
BuildRequires:	NetworkManager-devel >= 0.7.0
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.9
BuildRequires:	dbus-devel >= 0.95
BuildRequires:	dbus-glib-devel >= 0.82
BuildRequires:	docbook-dtd412-xml
BuildRequires:	glib2-devel >= 1:2.30.0
%{?with_apidocs:BuildRequires:	gtk-doc >= 1.17}
BuildRequires:	libtool
BuildRequires:	libxslt-progs
BuildRequires:	pkgconfig
BuildRequires:	python >= 2.5
BuildRequires:	python-modules >= 2.5
BuildRequires:	rpmbuild(macros) >= 1.527
BuildRequires:	telepathy-glib-devel >= 0.18.0
BuildRequires:	upower-devel
Requires(post,postun):	glib2 >= 1:2.26.0
Requires:	glib2 >= 1:2.30.0
Requires:	telepathy-glib >= 0.18.0
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
Requires:	dbus-glib-devel >= 0.82
Requires:	glib2-devel >= 1:2.30.0
Requires:	telepathy-glib-devel >= 0.18.0

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
	--disable-gnome-keyring \
	--disable-libaccounts-sso \
	%{__enable_disable apidocs gtk-doc} \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/mission-control/profiles

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_datadir}/telepathy/{clients,managers} \
	   $RPM_BUILD_ROOT%{_libdir}/mission-control-plugins.0

%{!?with_apidocs:rm -rf $RPM_BUILD_ROOT%{_gtkdocdir}}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%pretrans
# this needs to be a file
if [ -d %{_libexecdir}/mission-control ]; then
	rm -rf %{_libexecdir}/mission-control
fi

%post
/sbin/ldconfig
%glib_compile_schemas

%postun
/sbin/ldconfig
%glib_compile_schemas

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
%dir %{_libdir}/mission-control-plugins.0
%{_datadir}/dbus-1/services/org.freedesktop.Telepathy.AccountManager.service
%{_datadir}/dbus-1/services/org.freedesktop.Telepathy.MissionControl5.service
%{_datadir}/glib-2.0/schemas/im.telepathy.MissionControl.FromEmpathy.gschema.xml
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
