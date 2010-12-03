Summary:	Open Source installer build tool for Windows applications
Name:		nsis
Version:	2.10
Release:	0.2
License:	zlib/libpng
Group:		Development/Tools
URL:		http://nsis.sourceforge.net/
Source0:	http://downloads.sourceforge.net/nsis/%{name}-%{version}-1-src.tar.bz2
# Source0-md5:	800cb67e4043b12bc29bd049f8382dca
Source1:	http://downloads.sourceforge.net/nsis/%{name}-%{version}.zip
# Source1-md5:	a4eca14f4fd429fee18db892e8041484
BuildRequires:	libstdc++-devel
%ifarch %{x8664}
BuildRequires:	libstdc++32-devel
%endif
BuildRequires:	scons >= 0.96.93
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
NSIS (Nullsoft Scriptable Install System) is a professional Open
Source system to create Windows installers. It is designed to be as
small and flexible as possible and is therefore very suitable for
Internet distribution.

%prep
%setup -q -n %{name}-%{version}-src -a1
%{__cp} -aux %{name}-%{version}/* .

%{__rm} -rf Docs/StrFunc

%build
# build & install must use exactly same args to cmake, so make shell wrapper
# not to mistake.
cat <<'EOF' > build.sh
#!/bin/sh
%scons \
	APPEND_CCFLAGS="%{rpmcflags}" \
	APPEND_CXXFLAGS="%{rpmcxxflags}" \
	APPEND_LINKFLAGS="%{rpmldflags}" \
	PREFIX=%{_datadir}/nsis \
	SKIPSTUBS="all" \
	SKIPPLUGINS="all" \
	SKIPUTILS="Library/LibraryLocal,Library/RegTool,UIs,Makensisw,zip2exe,MakeLangId,NSIS Menu" \
	SKIPMISC="all" \
	VERSION="%{version}" \
	STRIP="false" \
	"$@"
EOF
chmod a+rx build.sh
./build.sh

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/nsis
cp -a NSIS.chm Bin Contrib Include Menu Plugins Stubs $RPM_BUILD_ROOT%{_datadir}/nsis

sh -x ./build.sh install \
	PREFIX=$RPM_BUILD_ROOT%{_datadir}/nsis

install -d $RPM_BUILD_ROOT{%{_bindir},%{_sysconfdir}}
#mv $RPM_BUILD_ROOT{%{_datadir}/nsis,%{_bindir}}/makensis
#mv $RPM_BUILD_ROOT{%{_datadir}/nsis,%{_sysconfdir}}/nsisconf.nsh

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a Examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Docs/*
#%config(noreplace) %{_sysconfdir}/nsisconf.nsh
#%attr(755,root,root) %{_bindir}/GenPat
#%attr(755,root,root) %{_bindir}/LibraryLocal
#%attr(755,root,root) %{_bindir}/makensis
%{_datadir}/nsis

%{_examplesdir}/%{name}-%{version}
