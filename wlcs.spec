#
# Conditional build:
%bcond_without	asan	# Address Sanitizer module
%bcond_without	tsan	# Thread Sanitizer module
%bcond_without	ubsan	# Undefined Behaviour Sanitizer module

%ifnarch %{ix86} %{x8664} x32 %{arm} aarch64 ppc ppc64 s390 s390x sparc sparcv9 sparc64
%undefine	with_asan
%undefine	with_ubsan
%endif
%ifnarch %{x8664} aarch64 ppc64 s390x
%undefine	with_tsan
%endif
Summary:	Wayland Conformance Test Suite
Summary(pl.UTF-8):	Wayland Conformance Test Suite - testy zgodności Waylanda
Name:		wlcs
Version:	1.7.0
Release:	2
License:	GPL v3
Group:		Libraries
#Source0Download: https://github.com/MirServer/wlcs/releases
Source0:	https://github.com/MirServer/wlcs/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	67d7233657987b335944fe658a76dd2c
URL:		https://github.com/MirServer/wlcs
BuildRequires:	boost-devel
BuildRequires:	cmake >= 3.5
BuildRequires:	gmock-devel
BuildRequires:	gtest-devel
%{?with_asan:BuildRequires:	libasan-devel}
# c++20
BuildRequires:	libstdc++-devel >= 6:8
%{?with_tsan:BuildRequires:	libtsan-devel}
%{?with_ubsan:BuildRequires:	libubsan-devel}
BuildRequires:	pkgconfig
# client, server, scanner
BuildRequires:	wayland-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Wayland Conformance Test Suite.

%description -l pl.UTF-8
Wayland Conformance Test Suite - testy zgodności Waylanda.

%package devel
Summary:	Header files for wlcs
Summary(pl.UTF-8):	Pliki nagłówkowe wlcs
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	wayland-devel

%description devel
Header files for wlcs.

%description devel -l pl.UTF-8
Pliki nagłówkowe wlcs.

%prep
%setup -q

%build
install -d build
cd build
%cmake .. \
	%{cmake_on_off asan WLCS_BUILD_ASAN} \
	%{cmake_on_off tsan WLCS_BUILD_TSAN} \
	%{cmake_on_off ubsan WLCS_BUILD_UBSAN}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.rst
%dir %{_libexecdir}/wlcs
%attr(755,root,root) %{_libexecdir}/wlcs/wlcs*

%files devel
%defattr(644,root,root,755)
%{_includedir}/wlcs
%{_pkgconfigdir}/wlcs.pc
