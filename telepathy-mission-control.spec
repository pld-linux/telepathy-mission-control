# TODO:
# - aegis (libcreds) - MeeGo platform specific?
# - libaccounts-sso (not only MeeGo, see http://code.google.com/p/accounts-sso/)
# - mce (Maemo-specific)
#
# Conditional build:
%bcond_without	apidocs		# disable gtk-doc
%bcond_with	uoa		# libaccounts-sso (single sign-on, aka Ubuntu Online Accounts) support
%bcond_with	upower		# enable legacy UPower support

Summary:	A Telepathy account manager
Summary(pl.UTF-8):	Zarządca kont Telepathy
Name:		telepathy-mission-control
Version:	5.16.4
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	https://telepathy.freedesktop.org/releases/telepathy-mission-control/%{name}-%{version}.tar.gz
# Source0-md5:	eab6c941038702edeece1168f395300c
URL:		http://mission-control.sourceforge.net/
BuildRequires:	NetworkManager-devel >= 0.7.0
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.9
BuildRequires:	dbus-devel >= 0.95
BuildRequires:	dbus-glib-devel >= 0.82
BuildRequires:	docbook-dtd412-xml
BuildRequires:	glib2-devel >= 1:2.46.0
%{?with_apidocs:BuildRequires:	gtk-doc >= 1.17}
%{?with_uoa:BuildRequires:	libaccounts-glib-devel >= 0.26}
BuildRequires:	libtool
BuildRequires:	libxslt-progs
BuildRequires:	pkgconfig
BuildRequires:	python >= 1:2.6
BuildRequires:	python-modules >= 1:2.6
BuildRequires:	rpmbuild(macros) >= 1.527
BuildRequires:	telepathy-glib-devel >= 0.20.0
%{?with_upower:BuildRequires:	upower-devel < 0.99.0}
Requires(post,postun):	glib2 >= 1:2.46.0
Requires:	dbus-glib >= 0.82
Requires:	dbus-libs >= 0.95
Requires:	glib2 >= 1:2.46.0
%{?with_uoa:Requires:	libaccounts-glib >= 0.26}
Requires:	telepathy-glib >= 0.20.0
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
Requires:	dbus-devel >= 0.95
Requires:	dbus-glib-devel >= 0.82
Requires:	glib2-devel >= 1:2.46.0
Requires:	telepathy-glib-devel >= 0.20.0
Obsoletes:	telepathy-mission-control-static

%description devel
Header files for mission control library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki mission control.

%package apidocs
Summary:	mission control library API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki mission control
Group:		Documentation
Requires:	gtk-doc-common
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

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
	%{__enable_disable apidocs gtk-doc} \
	%{?with_uoa:--enable-libaccounts-sso} \
	--disable-static \
	%{__enable_disable upower} \
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
%doc AUTHORS ChangeLog NEWS README
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
%{_pkgconfigdir}/mission-control-plugins.pc

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/mission-control-plugins
%endif
