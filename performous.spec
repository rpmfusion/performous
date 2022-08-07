%global gitdate 20210814
%global commit0 e0a28a61df442b4a4a34521cd3aa8e37e3f9ce3c
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global commit1 0fe8be431ebc7562379cd0f791110233c04420da
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})

Name:           performous
Epoch:          1
Version:        1.2.0
Release:        4%{?dist}
Summary:        Free cross-platform music and rhythm / party game

# The main code is GPLv2+, and there are fonts under ASL 2.0 and SIL licenses
License:        GPLv2+ and ASL 2.0 and OFL
URL:            https://performous.org
Source0:        https://github.com/performous/performous/archive/refs/tags/%{version}/%{name}-%{version}.tar.gz
Source1:        https://github.com/performous/compact_enc_det/archive/%{commit1}/ced-%{shortcommit1}.tar.gz
Source3:        performous.appdata.xml
Patch0:         performous-ced-offline.patch
Patch1:         performous-gcc12.patch
Patch2:         performous-ffmpeg.patch

BuildRequires:  alsa-lib-devel
BuildRequires:  aubio-devel
BuildRequires:  boost-devel
BuildRequires:  boost-system
BuildRequires:  boost-filesystem
BuildRequires:  cmake
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

Requires:       %{name}-data = %{?epoch}:%{version}-%{release}
Requires:       ffmpeg-libs%{?_isa}

%description
A karaoke, band and dancing game where one or more players perform a song and
the game scores their performances. Supports songs in UltraStar, Frets on Fire
and StepMania formats. Microphones and instruments from SingStar, Guitar Hero
and Rock Band as well as some dance pads are auto-detected.


%package data
Summary:        Data for Performous, the music and rhythm / party game
Requires:       %{name} = %{?epoch}:%{version}-%{release}
BuildArch:      noarch

%description data
This package contains the data files for Performous, as found in the %{name}
package.


%prep
%autosetup -p1 -n %{name}-%{version}
mkdir -p %{__cmake_builddir}/ced-src
tar -xf %{SOURCE1} -C %{__cmake_builddir}/ced-src/ --strip 1
cp -p "docs/license/SIL OFL Font License New Rocker.txt" SIL-OFL.txt


%build
# Jack support is disabled because the engine can't be chosen at run-time and
# jack will always take precedence over pulseaudio
%cmake -DSHARE_INSTALL:PATH=%{_datadir}/performous \
       -DCMAKE_BUILD_TYPE:STRING=RelWithDebInfo
%cmake_build


%install
%cmake_install

## Menu
mkdir -p %buildroot%{_datadir}/applications
desktop-file-validate %buildroot%{_datadir}/applications/%{name}.desktop

## Appstream
install -D -m 644 -p %{SOURCE3} %buildroot%{_metainfodir}/%{name}.appdata.xml
appstream-util validate-relax --nonet %buildroot%{_metainfodir}/%{name}.appdata.xml

rm -rf %buildroot%{_libdir}/*.{a,la}

%find_lang Performous

%files -f Performous.lang
%license LICENSE.md
%doc docs/*.txt
%{_bindir}/*
%{_datadir}/applications/*.desktop
%{_metainfodir}/%{name}.appdata.xml
%{_datadir}/pixmaps/*.svg
%{_mandir}/man*/*

%files data
%license LICENSE.md
%license docs/license/Apache-2.0-DroidSansMono.txt
%license SIL-OFL.txt
%{_datadir}/%{name}/


%changelog
* Sun Aug 07 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1:1.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild and ffmpeg
  5.1

* Thu Jun 23 2022 Sérgio Basto <sergio@serjux.com> - 1:1.2.0-3
- Rebuilt for opencv 4.6.0

* Sat Apr 30 2022 Leigh Scott <leigh123linux@gmail.com> - 1:1.2.0-2
- Add epoch to the requires
- Spec file clean up

* Thu Apr 14 2022 Sérgio Basto <sergio@serjux.com> - 1:1.2.0-1
- Update performous to 1.2.0
- This new version is not 2.0.0 as someone wrote, so we need add a new epoch

* Wed Feb 09 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 2.0.0-0.9.20210814gite0a28a6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Aug 19 2021 Sérgio Basto <sergio@serjux.com> - 2.0.0-0.8.20210814gite0a28a6
- Update performous to 20210814gite0a28a6
- Use system aubio
- Update ced and make it build with download external project ced

* Thu Aug 19 2021 Leigh Scott <leigh123linux@gmail.com> - 2.0.0-0.7.20201029git57ad2fc
- Rebuild for new boost

* Tue Aug 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.0.0-0.6.20201029git57ad2fc
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

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
