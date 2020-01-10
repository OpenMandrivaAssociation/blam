%define name blam
%define version 1.8.9
%define release %mkrel 2
%define _requires_exceptions lib.*x11\\|lib.*gtk
Summary: RSS aggregator written in C# using Mono, GTK# and RSS.NET
Name: %{name}
Version: %{version}
Release: %{release}
Epoch: 1
Source0: http://blam.cmartin.tk/downloads/%{name}-%{version}.tar.bz2
Patch0: blam-1.8.9-fix-build.patch
Patch1: blam-1.8.4-desktopentry.patch
# gw add planet mandriva feed
Patch2: blam-1.8.6-planetmandriva.patch
Patch3: blam-1.8.9-fix-dbus-configure-check.patch

License: GPLv2+
Group: Networking/Other
Url:  http://blam.cmartin.tk/
BuildArch: noarch
BuildRequires: mono-devel
BuildRequires: gnome-sharp2-devel
BuildRequires: gnome-desktop-sharp-devel
BuildRequires: glade-sharp2
BuildRequires: dbus-sharp-glib-devel
BuildRequires: webkit-sharp-devel
BuildRequires: notify-sharp-devel
BuildRequires: pkgconfig(gconf-2.0)
BuildRequires: imagemagick
BuildRequires: desktop-file-utils
BuildRequires: intltool
Requires(post): desktop-file-utils scrollkeeper
Requires(postun): desktop-file-utils scrollkeeper

%description
This is a GNOME RSS aggregator based on Mono.

%prep
%setup -q -n %name-%version
%autopatch -p1

autoconf

%build
./configure --prefix=%_prefix --sysconfdir=%_sysconfdir --disable-schemas-install
%make

%install
%makeinstall_std
mkdir -p %buildroot{%_liconsdir,%_iconsdir,%_miconsdir}
cp icons/48x48/%name.png %buildroot%_liconsdir/%name.png
cp icons/32x32/%name.png %buildroot%_iconsdir/%name.png
cp icons/16x16/%name.png %buildroot%_miconsdir/%name.png

%find_lang %name
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
