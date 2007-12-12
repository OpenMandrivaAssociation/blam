%define name blam
%define version 1.8.4
%define release %mkrel 10
#fixed2
%{?!mkrel:%define mkrel(c:) %{-c: 0.%{-c*}.}%{!?_with_unstable:%(perl -e '$_="%{1}";m/(.\*\\D\+)?(\\d+)$/;$rel=${2}-1;re;print "$1$rel";').%{?subrel:%subrel}%{!?subrel:1}.%{?distversion:%distversion}%{?!distversion:%(echo $[%{mdkversion}/10])}}%{?_with_unstable:%{1}}%{?distsuffix:%distsuffix}%{?!distsuffix:mdk}}

Summary: RSS aggregator written in C# using Mono, GTK# and RSS.NET
Name: %{name}
Version: %{version}
Release: %{release}
Epoch: 1
Source0: http://www.cmartin.tk/blam/%{name}-%{version}.tar.bz2
Patch: blam-firefox.patch
Patch1: blam-1.8.4-desktopentry.patch
# gw add planet mandriva feed
Patch2: blam-20060709-planetmandriva.patch
License: GPL
Group: Networking/Other
Url:  http://www.cmartin.tk/blam.html
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: mono-devel
BuildRequires: gnome-sharp2
BuildRequires: glade-sharp2
BuildRequires: gecko-sharp2
BuildRequires: libgnomeui2-devel
BuildRequires: mozilla-firefox-devel >= 0.10
BuildRequires: perl-XML-Parser
BuildRequires: ImageMagick
BuildRequires: desktop-file-utils
#gw if we run autoconf
BuildRequires: automake1.8
BuildRequires: intltool
BuildRequires: libtool
Requires: libmozilla-firefox = %(rpm -q --queryformat %{VERSION} mozilla-firefox)
Requires(post): desktop-file-utils scrollkeeper
Requires(postun): desktop-file-utils scrollkeeper

%description
This is a GNOME RSS aggregator based on Mono.

%prep
%setup -q -n %name-%version
%patch1 -p1
%patch2 -p1 -b .planetmandriva
%if %mdkversion <= 200700
%patch -p1 -b .firefox
./autogen.sh
%endif

%build
%configure2_5x --prefix=%_prefix --libdir=%_libdir --sysconfdir=%_sysconfdir \
%if %mdkversion > 200700
	--with-mozilla=firefox
%else
	--with-mozilla=mozilla-firefox
%endif

#gw parallel build is broken
make

%install
rm -rf $RPM_BUILD_ROOT
GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 %makeinstall_std
mkdir -p %buildroot{%_liconsdir,%_iconsdir,%_miconsdir}
convert -scale 48x48 icons/%name.png %buildroot%_liconsdir/%name.png
convert -scale 32x32 icons/%name.png %buildroot%_iconsdir/%name.png
convert -scale 16x16 icons/%name.png %buildroot%_miconsdir/%name.png
mkdir -p %buildroot/%_menudir
cat > %buildroot/%_menudir/%name << EOF
?package(%name): \
        command="%_bindir/%name" \
        needs="X11" \
        section="Internet/News" \
        icon="%name.png" \
        title="BLAM!" \
	startup_notify="true" \
	mimetypes="text/rss,application/rss+xml" \
        longtitle="GNOME RSS aggregator" xdg="true"
EOF


%find_lang %name
rm -f %buildroot%_prefix/lib/%name/*.a

%post
%update_scrollkeeper
%update_desktop_database
%post_install_gconf_schemas %name
%{update_menus}

%preun
%preun_uninstall_gconf_schemas

%postun
%{clean_menus}
%clean_scrollkeeper
%clean_desktop_database

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %name.lang
%defattr(-,root,root)
%doc AUTHORS ChangeLog NEWS README
%_sysconfdir/gconf/schemas/%name.schemas
%_bindir/%name
%_prefix/lib/%name
%_datadir/applications/%name.desktop
%_datadir/%name
%_datadir/pixmaps/%name.png
%_mandir/man1/blam.1*
%_menudir/%name
%_liconsdir/%name.png
%_iconsdir/%name.png
%_miconsdir/%name.png


