%global commit0 57ad2fc71f625a432f5e82b15bcf44081a29e8f8
%global gitdate 20201029
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

%undefine __cmake_in_source_build

Name:           performous
Version:        2.0.0
Release:        0.5.%{gitdate}git%{shortcommit0}%{?dist}
Summary:        Free cross-platform music and rhythm / party game

# The main code is GPLv2+, and there are fonts under ASL 2.0 and SIL licenses
License:        GPLv2+ and ASL 2.0 and OFL
URL:            https://performous.org
Source0:        https://github.com/performous/performous/archive/%{commit0}/%{name}-%{shortcommit0}.tar.gz
Source1:        https://github.com/performous/compact_enc_det/archive/26faf8f/ced-26faf8f.tar.gz
Source2:        https://github.com/performous/aubio/archive/712511e/aubio-712511e.tar.gz
Source3:        performous.appdata.xml

BuildRequires:  alsa-lib-devel
BuildRequires:  boost-devel
BuildRequires:  boost-system
BuildRequires:  boost-filesystem
BuildRequires:  cmake3
BuildRequires:  cairo-devel
BuildRequires:  cpprest-devel
BuildRequires:  desktop-file-utils
BuildRequires:  ffmpeg-devel
BuildRequires:  glew-devel
BuildRequires:  gcc-c++
BuildRequires:  gettext
BuildRequires:  glibmm24-devel
BuildRequires:  glm-devel
BuildRequires:  help2man
BuildRequires:  ImageMagick-devel
BuildRequires:  ImageMagick-c++-devel
BuildRequires:  libepoxy-devel
BuildRequires:  libappstream-glib
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  libvorbis-devel
BuildRequires:  libsigc++20-devel
BuildRequires:  librsvg2-devel
BuildRequires:  libxml2-devel
BuildRequires:  libxml++-devel
BuildRequires:  libraw1394-devel
BuildRequires:  libtheora-devel
BuildRequires:  opencv-devel
BuildRequires:  openblas-devel
BuildRequires:  blas-devel
BuildRequires:  lapack-devel
BuildRequires:  fftw-devel
BuildRequires:  openssl-devel
BuildRequires:  pango-devel
BuildRequires:  portaudio-devel
BuildRequires:  portmidi-devel
BuildRequires:  recode
BuildRequires:  SDL2-devel
BuildRequires:  python

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
%autosetup -p1 -n %{name}-%{commit0}
tar -xf %{SOURCE1} -C 3rdparty/ced/ --strip 1
tar -xf %{SOURCE2} -C 3rdparty/aubio/ --strip 1
cp -p "docs/license/SIL OFL Font License New Rocker.txt" SIL-OFL.txt


%build
# Jack support is disabled because the engine can't be chosen at run-time and
# jack will always take precedence over pulseaudio
#cmake -DSHARE_INSTALL:PATH=share/performous \
%cmake -DSHARE_INSTALL:PATH=%{_datadir}/performous \
       -DCMAKE_BUILD_TYPE:STRING=RelWithDebInfo -DUSE_BOOST_REGEX=1
%cmake_build


%install
%cmake_install

## Menu
mkdir -p %buildroot%{_datadir}/applications
desktop-file-validate %buildroot%{_datadir}/applications/%{name}.desktop

## Appstream
install -D -m 644 -p %{SOURCE3} %buildroot%{_datadir}/metainfo/%{name}.appdata.xml
appstream-util validate-relax --nonet %buildroot%{_datadir}/metainfo/%{name}.appdata.xml

rm -rf %buildroot%{_libdir}/*.{a,la}

%find_lang Performous

%files -f Performous.lang
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
* Sat Apr 24 2021 Leigh Scott <leigh123linux@gmail.com> - 2.0.0-0.5.20201029git57ad2fc
- Rebuilt for removed libstdc++ symbol (#1937698)

* Wed Feb 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.0.0-0.4.20201029git57ad2fc
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 04 2021 Sérgio Basto <sergio@serjux.com> - 2.0.0-0.3.20201029git57ad2fc
- Update to 20201029git57ad2fc

* Fri Jan  1 2021 Leigh Scott <leigh123linux@gmail.com> - 2.0.0-0.2.20200604git997f488
- Rebuilt for new ffmpeg snapshot

* Thu Aug 27 2020 Sérgio Basto <sergio@serjux.com> - 2.0.0-0.1.20200604git997f488
- Update to 20200604git997f488
- Update Version https://github.com/performous/performous/projects/2
- Fix crash on startup rfbz #5720

* Tue Aug 18 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.2-0.8.20190419git4ed8ec7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jun 10 2020 Leigh Scott <leigh123linux@gmail.com> - 1.2-0.7.20190419git4ed8ec7
- Rebuilt for opencv-4.3

* Thu Jun 04 2020 Leigh Scott <leigh123linux@gmail.com> - 1.2-0.6.20190419git4ed8ec7
- Rebuilt for Boost 1.73

* Tue Mar 10 2020 leigh123linux <leigh123linux@googlemail.com> - 1.2-0.5.20190419git4ed8ec7
- Patch for pango-1.44.7

* Wed Feb 05 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.2-0.4.20190419git4ed8ec7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Aug 07 2019 Leigh Scott <leigh123linux@gmail.com> - 1.2-0.3.20190419git4ed8ec7
- Rebuild for new ffmpeg version

* Thu May 02 2019 Leigh Scott <leigh123linux@gmail.com> - 1.2-0.2.20190419git4ed8ec7
- Add buildrequires openssl-devel

* Thu May 02 2019 Leigh Scott <leigh123linux@gmail.com> - 1.2-0.1.20190419git4ed8ec7
- Update to latest git snapshot
- Short out the horrible buildrequires mess
- Don't fix fsf address, it isn't our job

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
