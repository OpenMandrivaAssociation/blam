%define name blam
%define version 1.8.8
%define release %mkrel 1
%define _requires_exceptions lib.*x11\\|lib.*gtk
Summary: RSS aggregator written in C# using Mono, GTK# and RSS.NET
Name: %{name}
Version: %{version}
Release: %{release}
Epoch: 1
Source0: http://blam.cmartin.tk/downloads/%{name}-%{version}.tar.bz2
Patch1: blam-1.8.4-desktopentry.patch
# gw add planet mandriva feed
Patch2: blam-1.8.6-planetmandriva.patch

License: GPLv2+
Group: Networking/Other
Url:  http://blam.cmartin.tk/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch: noarch
BuildRequires: mono-devel
BuildRequires: gnome-sharp2-devel
BuildRequires: gnome-desktop-sharp-devel
BuildRequires: glade-sharp2
BuildRequires: ndesk-dbus-glib-devel
BuildRequires: webkit-sharp-devel
BuildRequires: notify-sharp-devel
BuildRequires: imagemagick
BuildRequires: desktop-file-utils
BuildRequires: intltool
Requires(post): desktop-file-utils scrollkeeper
Requires(postun): desktop-file-utils scrollkeeper

%description
This is a GNOME RSS aggregator based on Mono.

%prep
%setup -q -n %name-%version
%patch1 -p1
%patch2 -p1 -b .planetmandriva

%build
./configure --prefix=%_prefix --sysconfdir=%_sysconfdir --disable-schemas-install
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
