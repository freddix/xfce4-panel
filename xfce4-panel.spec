%define		xfce_version	4.11.0

Summary:	Next generation panel for Xfce
Name:		xfce4-panel
Version:	4.11.1
Release:	1
License:	GPL v2, LGPL v2
Group:		X11/Applications
Source0:	http://archive.xfce.org/src/xfce/xfce4-panel/4.11/%{name}-%{version}.tar.bz2
# Source0-md5:	21e056bdfb7a6b4d70e4ded619b2a88d
URL:		http://www.xfce.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	docbook-dtd412-xml
BuildRequires:	docbook-style-xsl
BuildRequires:	exo-devel
BuildRequires:	garcon-devel
BuildRequires:	gettext-devel
BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	libtool
BuildRequires:	libwnck2-devel
BuildRequires:	libxfce4ui-devel >= %{xfce_version}
BuildRequires:	libxml2-devel
BuildRequires:	libxslt-progs
BuildRequires:	pkg-config
BuildRequires:	startup-notification-devel
BuildRequires:	xfce4-dev-tools >= %{xfce_version}
Requires(post,postun):	/usr/bin/gtk-update-icon-cache
Requires(post,postun):	hicolor-icon-theme
Requires:	%{name}-libs = %{version}-%{release}
Requires:	exo
Requires:	garcon
Requires:	xdg-icon-theme
Requires:	xfconf
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
xfce4-panel is the panel for the Xfce desktop environment.

%package apidocs
Summary:	Xfce panel API documentation
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
Xfce panel API documentation.

%package libs
Summary:	xfce4panel library
Group:		Development/Libraries

%description libs
This package contains xfce4panel library.

%package devel
Summary:	Header files for building Xfce panel plugins
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for building Xfce panel plugins.

%prep
%setup -q

%build
%{__gtkdocize}
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__automake}
%{__autoconf}
%configure \
	--disable-silent-rules		\
	--disable-static		\
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_datadir}/xfce4/panel-plugins
install -d $RPM_BUILD_ROOT%{_datadir}/xfce4/panel/plugins
install -d $RPM_BUILD_ROOT%{_libdir}/xfce4/panel/plugins
install -d $RPM_BUILD_ROOT%{_libdir}/xfce4/{modules,panel-plugins}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/{,xfce4/panel/plugins}/*.la
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/locale/ur_PK

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor

%postun
%update_icon_cache hicolor

%post	libs -p /usr/sbin/ldconfig
%postun	libs -p /usr/sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README docs/README.gtkrc-2.0
%dir %{_sysconfdir}/xdg/xfce4/panel
%{_sysconfdir}/xdg/xfce4/panel/default.xml
%attr(755,root,root) %{_bindir}/*

%dir %{_datadir}/xfce4/panel
%dir %{_datadir}/xfce4/panel/plugins
%dir %{_libdir}/xfce4/panel
%dir %{_libdir}/xfce4/panel/plugins
# compat dirs
%{_datadir}/xfce4/panel-plugins
%{_libdir}/xfce4/modules
%{_libdir}/xfce4/panel-plugins

%attr(755,root,root) %{_libdir}/xfce4/panel/migrate
%attr(755,root,root) %{_libdir}/xfce4/panel/plugins/*.so
%attr(755,root,root) %{_libdir}/xfce4/panel/wrapper-1.0
%{_datadir}/xfce4/panel/plugins/*.desktop

%{_iconsdir}/hicolor/*/*/*
%{_desktopdir}/*.desktop

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libxfce4panel-1.0

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libxfce4panel-1.0.so.?
%attr(755,root,root) %{_libdir}/libxfce4panel-1.0.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libxfce4panel-1.0.so
%{_includedir}/xfce4/libxfce4panel-1.0
%{_pkgconfigdir}/*.pc

