Name:           performous
Version:        1.1
Release:        4%{?dist}
Summary:        Free cross-platform music and rhythm / party game

# The main code is GPLv2+, and there are fonts under ASL 2.0 and SIL licenses
License:        GPLv2+ and ASL 2.0 and OFL
URL:            http://performous.org
Source0:        https://github.com/performous/performous/archive/%{version}/%{name}-%{version}.tar.gz
Source1:        https://raw.githubusercontent.com/performous/performous/master/licence.txt
Source2:        performous.appdata.xml

BuildRequires:  gcc-c++, cmake, cairo-devel, SDL2-devel
BuildRequires:  boost-devel, boost-system, boost-filesystem
BuildRequires:  librsvg2-devel, libxml2-devel, alsa-lib-devel
BuildRequires:  recode, glew-devel, help2man, libvorbis-devel
BuildRequires:  libsigc++20-devel, glibmm24-devel, libxml++-devel
BuildRequires:  ImageMagick-devel, ImageMagick-c++-devel
BuildRequires:  ffmpeg-devel, libraw1394-devel, libtheora-devel
BuildRequires:  pango-devel, portaudio-devel, gettext
BuildRequires:  opencv-devel, portmidi-devel
BuildRequires:  libepoxy-devel
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib

Obsoletes:      ultrastar-ng <= 0.3.0
Provides:       ultrastar-ng = %{version}
Requires:       %{name}-data = %{version}-%{release}

%description
A karaoke, band and dancing game where one or more players perform a song and
the game scores their performances. Supports songs in UltraStar, Frets on Fire
and StepMania formats. Microphones and instruments from SingStar, Guitar Hero
and Rock Band as well as some dance pads are auto-detected.


%package data
Summary:        Data for Performous, the music and rhythm / party game
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch

%description data
This package contains the data files for Performous, as found in the %{name}
package.


%prep
%autosetup
cp -p %{SOURCE1} .
cp -p "docs/license/SIL OFL Font License New Rocker.txt" SIL-OFL.txt
# Incorrect FSF address
# https://github.com/performous/performous/issues/328
sed -i -e 's/59 Temple Place, Suite 330, Boston, MA  02111-1307/51 Franklin St, Fifth Floor, Boston, MA  02110-1301/g' \
    tools/gh_fsb/*.{c,h}


%build
mkdir -p build
cd build
# Jack support is disabled because the engine can't be chosen at run-time and
# jack will always take precedence over pulseaudio
#%%cmake -DSHARE_INSTALL:PATH=share/performous \
%cmake -DSHARE_INSTALL:PATH=%{_datadir}/performous \
       -DCMAKE_BUILD_TYPE:STRING=RelWithDebInfo \
       ..
%make_build


%install
cd build
%make_install

## Menu
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop

## Appstream
install -D -m 644 -p %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/metainfo/%{name}.appdata.xml
appstream-util validate-relax --nonet $RPM_BUILD_ROOT%{_datadir}/metainfo/%{name}.appdata.xml

rm -rf $RPM_BUILD_ROOT%{_libdir}/*.{a,la}

%find_lang Performous


%ldconfig_scriptlets


%files -f build/Performous.lang
%license licence.txt
%doc docs/*.txt
%{_bindir}/*
%{_datadir}/applications/*.desktop
%{_datadir}/metainfo/%{name}.appdata.xml
%{_datadir}/pixmaps/*.svg
%{_mandir}/man*/*

%files data
%license licence.txt
%license docs/license/Apache-2.0-DroidSansMono.txt
%license SIL-OFL.txt
%{_datadir}/%{name}


%changelog
* Mon Mar 04 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 27 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 28 2018 Aurelien Bompard <abompard@fedoraproject.org> - 1.1-2
- modernize spec file.

* Sat Feb 13 2016 Aurelien Bompard <abompard@fedoraproject.org> - 1.1-1
- version 1.1

* Mon Nov 10 2014 Aurelien Bompard <abompard@fedoraproject.org> - 1.0-1
- version 1.0

* Sun Apr 21 2013 Aurelien Bompard <abompard@fedoraproject.org> - 0.7.0-2
- implement suggestion from upstream:
  https://github.com/performous/performous/issues/28#issuecomment-16729156

* Sun Nov 18 2012 Aurelien Bompard <abompard@fedoraproject.org> -  0.7.0-1
- version 0.7.0

* Fri Nov 12 2010 Aurelien Bompard <abompard@fedoraproject.org> -  0.6.1-1
- version 0.6.1

* Wed Oct 27 2010 Aurelien Bompard <abompard@fedoraproject.org> -  0.6.0-1
- version 0.6.0

* Sun Aug 08 2010 Aurelien Bompard <abompard@fedoraproject.org> -  0.5.1-3
- update summary and description

* Wed Jul 14 2010 Aurelien Bompard <abompard@fedoraproject.org> -  0.5.1-2
- fix desktop file

* Sun Apr 11 2010 Aurelien Bompard <abompard@fedoraproject.org> -  0.5.1-1
- version 0.5.1

* Tue Dec 01 2009 Aurelien Bompard <abompard@fedoraproject.org> -  0.4.0-1
- version 0.4.0

* Tue Jul 07 2009 Aurelien Bompard <abompard@fedoraproject.org> 0.3.1-1
- version 0.3.1

* Sun Nov 16 2008 Aurelien Bompard <abompard@fedoraproject.org> 0.3.0-1
- version 0.3.0

* Mon Nov 05 2007 Aurelien Bompard <abompard@fedoraproject.org> 0.2.1-1
- version 0.2.1

* Fri Nov 02 2007 Aurelien Bompard <abompard@fedoraproject.org> 0.2.0-1
- version 0.2.0

* Sat May 19 2007 Aurelien Bompard <abompard@fedoraproject.org> 0.1.4-1
- initial release
