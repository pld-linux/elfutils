Summary:	A collection of utilities and DSOs to handle compiled objects.
Name:		elfutils
Version:	0.76
Release:	4
License:	GPL
Group:		Development/Tools
#URL: file://home/devel/drepper
Source0:	%{name}-%{version}.tar.gz
Requires:	elfutils-libelf = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
BuildRequires:	gcc >= 3.2
BuildRequires:	sharutils

%define _programprefix eu-

%description
Elfutils is a collection of utilities, including ld (a linker), nm
(for listing symbols from object files), size (for listing the section
sizes of an object or archive file), strip (for discarding symbols),
readline (the see the raw ELF file structures), and elflint (to check
for well-formed ELF files). Also included are numerous helper
libraries which implement DWARF, ELF, and machine-specific ELF
handling.

%package devel
Summary:	Development libraries to handle compiled objects.
Group:		Development/Tools
Obsoletes:	libelf-devel
Requires:	elfutils = %{version}-%{release}

%description devel
The elfutils-devel package contains the libraries to create
applications for handling compiled objects. libelf allows you to
access the internals of the ELF object file format, so you can see the
different sections of an ELF file. libebl provides some higher-level
ELF access functionality. libdwarf provides access to the DWARF
debugging information. libasm provides a programmable assembler
interface.

%package libelf
Summary:	Library to read and write ELF files.
Group:		Development/Tools
Obsoletes:	libelf

%description libelf
The elfutils-libelf package provides a DSO which allows reading and
writing ELF files on a high level. Third party programs depend on this
package to read internals of ELF files. The programs of the elfutils
package use it also to generate new ELF files.

%prep
%setup -q

%build
%{__aclocal}
%{__autoheader}
%{__automake}
%{__autoconf}
%configure \
   --program-prefix=%{_programprefix} \
   --enable-shared

%install
rm -rf $RPM_BUILD_ROOT
install -d ${RPM_BUILD_ROOT}%{_prefix}

#make check
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

chmod +x ${RPM_BUILD_ROOT}%{_prefix}/%{_lib}/lib*.so*
chmod +x ${RPM_BUILD_ROOT}%{_prefix}/%{_lib}/elfutils/lib*.so*


# XXX Nuke unpackaged files
{ cd ${RPM_BUILD_ROOT}
  rm -f .%{_bindir}/eu-ld
  rm -f .%{_includedir}/elfutils/libasm.h
  rm -f .%{_includedir}/elfutils/libdw.h
  rm -f .%{_includedir}/elfutils/libdwarf.h
  rm -f .%{_libdir}/libasm-%{version}.so
  rm -f .%{_libdir}/libasm.a
  rm -f .%{_libdir}/libdw-%{version}.so
  rm -f .%{_libdir}/libdw.a
  rm -f .%{_libdir}/libdwarf.a
}

#%%check
#make check

%clean
rm -rf ${RPM_BUILD_ROOT}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post libelf -p /sbin/ldconfig

%postun libelf -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README TODO libdwarf/AVAILABLE
%attr(755,root,root) %{_bindir}/eu-elflint
#%{_bindir}/eu-ld
%attr(755,root,root) %{_bindir}/eu-nm
%attr(755,root,root) %{_bindir}/eu-readelf
%attr(755,root,root) %{_bindir}/eu-size
%attr(755,root,root) %{_bindir}/eu-strip
#%{_libdir}/libasm-%{version}.so
%{_libdir}/libebl-%{version}.so
#%{_libdir}/libdw-%{version}.so
%{_libdir}/libdwarf-%{version}.so
#%{_libdir}/libasm*.so.*
%{_libdir}/libebl*.so.*
#%{_libdir}/libdw*.so.*
%{_libdir}/libdwarf*.so.*
%dir %{_libdir}/elfutils
%{_libdir}/elfutils/lib*.so

%files devel
%defattr(644,root,root,755)
%{_includedir}/dwarf.h
%{_includedir}/libelf.h
%{_includedir}/gelf.h
%{_includedir}/nlist.h
%dir %{_includedir}/elfutils
%{_includedir}/elfutils/elf-knowledge.h
%{_includedir}/elfutils/libebl.h
#%{_libdir}/libasm.a
%{_libdir}/libebl.a
%{_libdir}/libelf.a
#%{_libdir}/libdw.a
#%{_libdir}/libasm.so
%{_libdir}/libebl.so
%{_libdir}/libelf.so
#%{_libdir}/libdw.so
#%{_libdir}/libdwarf.so

%files libelf
%defattr(644,root,root,755)
%{_libdir}/libelf-%{version}.so
%{_libdir}/libelf*.so.*
