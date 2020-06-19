# hashcat require an ancient version of minizip.
# On Fedora we can use compatibility package, but
# on RHEL we must use bundled version.
%if 0%{?fedora}
%bcond_without zlib
%else
%bcond_with zlib
%endif

%global makeflags PREFIX=%{_prefix} LIBRARY_FOLDER=%{_libdir} SHARED_ROOT_FOLDER=%{_libdir} DOCUMENT_FOLDER=%{_docdir}/hashcat-doc

Name: hashcat
Version: 6.0.0
Release: 3%{?dist}
Summary: Advanced password recovery utility

License: MIT and Public Domain
URL: https://github.com/%{name}/%{name}
Source0: %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

Patch0: %{name}-build-fixes.patch
Patch1: %{name}-packaged-minizip.patch

# https://github.com/hashcat/hashcat/issues/2463
Patch100: %{name}-nvidia-opencl.patch

BuildRequires: bash-completion
BuildRequires: opencl-headers
BuildRequires: xxhash-devel
BuildRequires: zlib-devel
BuildRequires: gcc

%if %{with zlib}
BuildRequires: minizip-compat-devel
%else
Provides: bundled(zlib) = 1.2.11
Provides: bundled(minizip) = 1.2.11
%endif

Requires: bash-completion
%if 0%{?fedora}
Recommends: mesa-libOpenCL%{?_isa}
Recommends: pocl%{?_isa}
Recommends: %{name}-doc = %{?epoch:%{epoch}:}%{version}-%{release}
%endif

# Upstream does not support Big Endian architectures.
ExcludeArch: ppc64 s390x

%description
Hashcat is the world's fastest and most advanced password recovery
utility, supporting five unique modes of attack for over 200
highly-optimized hashing algorithms. hashcat currently supports
CPUs, GPUs, and other hardware accelerators on Linux, Windows,
and Mac OS, and has facilities to help enable distributed password
cracking.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
%{summary}.

%package doc
Summary: Documentation files for %{name}
Requires: %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
BuildArch: noarch

%description doc
%{summary}.

%prep
%setup -q
%patch0 -p1
%patch100 -p1
rm -rf deps/{OpenCL-Headers,xxHash}
%if %{with zlib}
%patch1 -p1
rm -rf deps/zlib
%endif
sed -e 's/\.\/hashcat/hashcat/' -i *.sh
chmod -x *.sh
rm -f modules/.lock

%build
%set_build_flags
%make_build \
    %{makeflags} \
%if %{with zlib}
    USE_SYSTEM_ZLIB=1
%else
    USE_SYSTEM_ZLIB=0
%endif

%install
%make_install %{makeflags}
ln -s lib%{name}.so.%{version} %{buildroot}%{_libdir}/lib%{name}.so
mkdir -p %{buildroot}%{_datadir}/bash-completion/completions
install -m 0744 -p extra/tab_completion/hashcat.sh %{buildroot}%{_datadir}/bash-completion/completions/%{name}

%files
%license docs/license.txt
%doc README.md
%{_datadir}/bash-completion/completions/%{name}
%{_libdir}/lib%{name}.so.%{version}
%{_libdir}/%{name}/
%{_bindir}/%{name}

%files devel
%{_includedir}/%{name}
%{_libdir}/lib%{name}.so

%files doc
%doc docs/ charsets/ layouts/ masks/ rules/
%doc example.dict example*.sh

%changelog
* Fri Jun 19 2020 Vitaly Zaitsev <vitaly@easycoding.org> - 6.0.0-3
- Backported upstream patch with NVIDIA OpenCL fixes.

* Thu Jun 18 2020 Vitaly Zaitsev <vitaly@easycoding.org> - 6.0.0-2
- Fixed packaging issues, related to modules.

* Wed Jun 17 2020 Vitaly Zaitsev <vitaly@easycoding.org> - 6.0.0-1
- Updated to version 6.0.0.

* Tue Feb 25 2020 Vitaly Zaitsev <vitaly@easycoding.org> - 5.1.0-7
- Allow to install without mesa-libOpenCL.
- Added pocl as a weak dependency on Fedora.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 24 2019 Vitaly Zaitsev <vitaly@easycoding.org> - 5.1.0-4
- Switched to regular build instead of debug.

* Mon Feb 18 2019 Vitaly Zaitsev <vitaly@easycoding.org> - 5.1.0-3
- Fixed problem with dependencies on EPEL7.

* Thu Feb 07 2019 Vitaly Zaitsev <vitaly@easycoding.org> - 5.1.0-2
- Moved documentation to a separate package.

* Wed Feb 06 2019 Vitaly Zaitsev <vitaly@easycoding.org> - 5.1.0-1
- Initial SPEC release.
