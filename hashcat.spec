Name: hashcat
Version: 5.1.0
Release: 1%{?dist}
Summary: Advanced password recovery utility

License: MIT
URL: https://github.com/%{name}/%{name}

Source0: %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
Patch0: 0001-Fedora-build-patches.patch

BuildRequires: bash-completion
BuildRequires: opencl-headers
BuildRequires: xxhash-devel
BuildRequires: gcc

Requires: bash-completion

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

%prep
%autosetup -p1
sed -e 's/\.\/hashcat/hashcat/' -i *.sh

%build
%set_build_flags
%make_build PREFIX=%{_prefix}

%install
%make_install PREFIX=%{_prefix} LIBRARY_FOLDER=%{_libdir}
ln -s lib%{name}.so.%{version} "%{buildroot}%{_libdir}/lib%{name}.so"

%files
%license docs/license.txt
%doc README.md
%doc docs/{changes,contact,credits,limits,performance,readme,rules,status_codes,team,user_manuals}.txt
%doc charsets/ layouts/ masks/ rules/
%{_datadir}/bash-completion/completions/%{name}
%{_libdir}/lib%{name}.so.%{version}
%{_datadir}/%{name}
%{_bindir}/%{name}

%files devel
%{_includedir}/%{name}
%{_libdir}/lib%{name}.so

%changelog
* Wed Feb 06 2019 Vitaly Zaitsev <vitaly@easycoding.org> - 5.1.0-1
- Initial SPEC release.
