%define name blam
%define version 1.8.6
%define release %mkrel 2
%define _requires_exceptions lib.*x11\\|lib.*gtk
Summary: RSS aggregator written in C# using Mono, GTK# and RSS.NET
Name: %{name}
Version: %{version}
Release: %{release}
Epoch: 1
Source0: http://www.cmartin.tk/blam/%{name}-%{version}.tar.bz2
Patch: blam-1.8.5-new-gnome-print-sharp.patch
Patch1: blam-1.8.4-desktopentry.patch
# gw add planet mandriva feed
Patch2: blam-1.8.6-planetmandriva.patch
#gw from Fedora: xulrunner patches:
Patch4:	blam-xulrunner.patch
Patch5: blam-xulrunner-configure.patch

License: GPLv2+
Group: Networking/Other
Url:  http://www.cmartin.tk/blam.html
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch: noarch
BuildRequires: mono-devel
BuildRequires: gnome-sharp2-devel
BuildRequires: gnome-desktop-sharp-devel
BuildRequires: glade-sharp2
BuildRequires: gecko-sharp2
BuildRequires: ndesk-dbus-glib
BuildRequires: libgnomeui2-devel
BuildRequires: webkit-sharp-devel
BuildRequires: imagemagick
BuildRequires: desktop-file-utils
#gw if we run autoconf
BuildRequires: automake
BuildRequires: intltool
BuildRequires: libtool
Requires(post): desktop-file-utils scrollkeeper
Requires(postun): desktop-file-utils scrollkeeper

%description
This is a GNOME RSS aggregator based on Mono.

%prep
%setup -q -n %name-%version
%patch -p1
%patch1 -p1
%patch2 -p1 -b .planetmandriva
#patch4 -p1 -b .xl
#patch5 -p1 -b .xlc
#gw patch 0,5
autoconf

%build
./configure --prefix=%_prefix --sysconfdir=%_sysconfdir --disable-static --disable-schemas-install
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std
mkdir -p %buildroot{%_liconsdir,%_iconsdir,%_miconsdir}
cp icons/48x48/%name.png %buildroot%_liconsdir/%name.png
cp icons/32x32/%name.png %buildroot%_iconsdir/%name.png
cp icons/16x16/%name.png %buildroot%_miconsdir/%name.png

%find_lang %name

%if %mdkversion < 200900
%post
%update_scrollkeeper
%update_desktop_database
%post_install_gconf_schemas %name
%{update_menus}
%update_icon_cache hicolor
%endif

%preun
%preun_uninstall_gconf_schemas %name

%if %mdkversion < 200900
%postun
%{clean_menus}
%clean_scrollkeeper
%clean_desktop_database
%clean_icon_cache hicolor
%endif

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
%_mandir/man1/blam.1*
%_iconsdir/hicolor/*/apps/*
%_liconsdir/%name.png
%_iconsdir/%name.png
%_miconsdir/%name.png
