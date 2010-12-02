Summary:	Open Source installer build tool for Windows applications
Name:		nsis
Version:	2.34
Release:	0.1
License:	zlib/libpng
Group:		Development/Tools
URL:		http://nsis.sourceforge.net/
Source0:	http://downloads.sourceforge.net/nsis/%{name}-%{version}-src.tar.bz2
# Source0-md5:	60243c2562710eeac45bda1378e4c88c
Source1:	http://downloads.sourceforge.net/nsis/%{name}-%{version}.zip
# Source1-md5:	565d17b3ff12dffcf678ec252a892c04
BuildRequires:	libstdc++-devel
BuildRequires:	scons >= 0.96.93
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
%scons \
	PREFIX=%{_prefix} \
	PREFIX_DEST=$RPM_BUILD_ROOT \
	PREFIX_CONF=%{_sysconfdir} \
	SKIPSTUBS="all" \
	SKIPPLUGINS="all" \
	SKIPUTILS="Library/RegTool,UIs,Makensisw,zip2exe,MakeLangId,NSIS Menu" \
	SKIPMISC="all" \
	VERSION="%{version}" \
	STRIP="false"

%install
rm -rf $RPM_BUILD_ROOT
%scons install \
	PREFIX=%{_prefix} \
	PREFIX_DEST=$RPM_BUILD_ROOT \
	PREFIX_CONF=%{_sysconfdir} \
	SKIPSTUBS="all" \
	SKIPPLUGINS="all" \
	SKIPUTILS="Library/RegTool,UIs,Makensisw,zip2exe,MakeLangId,NSIS Menu" \
	SKIPMISC="all" \
	VERSION="%{version}" \
	STRIP="false"

install -d $RPM_BUILD_ROOT%{_datadir}/nsis
cp -fr Bin Contrib Include Menu Plugins Stubs $RPM_BUILD_ROOT%{_datadir}/nsis

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYING Docs Examples
%config(noreplace) %{_sysconfdir}/nsisconf.nsh
%attr(755,root,root) %{_bindir}/GenPat
%attr(755,root,root) %{_bindir}/LibraryLocal
%attr(755,root,root) %{_bindir}/makensis
%{_datadir}/nsis
%exclude %{_datadir}/doc/nsis
