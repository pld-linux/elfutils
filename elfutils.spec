Summary: A collection of utilities and DSOs to handle compiled objects.
Name: elfutils
Version: 0.76
Release: 3
Copyright: GPL
Group: Development/Tools
#URL: file://home/devel/drepper
Source: elfutils-%{version}.tar.gz
Obsoletes: libelf libelf-devel
Requires: elfutils-libelf = %{version}-%{release}

# ExcludeArch: xxx

BuildRoot: %{_tmppath}/%{name}-root
BuildRequires: gcc >= 3.2
BuildRequires: sharutils

%define _gnu %{nil}
%define _programprefix eu-

%description
Elfutils is a collection of utilities, including ld (a linker),
nm (for listing symbols from object files), size (for listing the
section sizes of an object or archive file), strip (for discarding
symbols), readline (the see the raw ELF file structures), and elflint
(to check for well-formed ELF files).  Also included are numerous
helper libraries which implement DWARF, ELF, and machine-specific ELF
handling.

%package devel
Summary: Development libraries to handle compiled objects.
Group: Development/Tools
Requires: elfutils = %{version}-%{release}

%description devel
The elfutils-devel package contains the libraries to create
applications for handling compiled objects.  libelf allows you to
access the internals of the ELF object file format, so you can see the
different sections of an ELF file.  libebl provides some higher-level
ELF access functionality.  libdwarf provides access to the DWARF
debugging information.  libasm provides a programmable assembler
interface.

%package libelf
Summary: Library to read and write ELF files.
Group: Development/Tools

%description libelf
The elfutils-libelf package provides a DSO which allows reading and
writing ELF files on a high level.  Third party programs depend on
this package to read internals of ELF files.  The programs of the
elfutils package use it also to generate new ELF files.

%prep
%setup -q

%build
mkdir build-%{_target_platform}
cd build-%{_target_platform}
../configure \
  --prefix=%{_prefix} --exec-prefix=%{_exec_prefix} \
  --bindir=%{_bindir} --sbindir=%{_sbindir} --sysconfdir=%{_sysconfdir} \
  --datadir=%{_datadir} --includedir=%{_includedir} --libdir=%{_libdir} \
  --libexecdir=%{_libexecdir} --localstatedir=%{_localstatedir} \
  --sharedstatedir=%{_sharedstatedir} --mandir=%{_mandir} \
  --infodir=%{_infodir} --program-prefix=%{_programprefix} --enable-shared
cd ..

%install
rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}

cd build-%{_target_platform}
#make check
%makeinstall

chmod +x ${RPM_BUILD_ROOT}%{_prefix}/%{_lib}/lib*.so*
chmod +x ${RPM_BUILD_ROOT}%{_prefix}/%{_lib}/elfutils/lib*.so*

cd ..

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

%check
cd build-%{_target_platform}
make check

%clean
rm -rf ${RPM_BUILD_ROOT}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post libelf -p /sbin/ldconfig

%postun libelf -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc README TODO libdwarf/AVAILABLE
%{_bindir}/eu-elflint
#%{_bindir}/eu-ld
%{_bindir}/eu-nm
%{_bindir}/eu-readelf
%{_bindir}/eu-size
%{_bindir}/eu-strip
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
%defattr(-,root,root)
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
%defattr(-,root,root)
%{_libdir}/libelf-%{version}.so
%{_libdir}/libelf*.so.*

%changelog
* Mon Feb 24 2003 Elliot Lee <sopwith@redhat.com>
- debuginfo rebuild

* Thu Feb 20 2003 Jeff Johnson <jbj@redhat.com> 0.76-2
- use the correct way of identifying the section via the sh_info link.

* Sat Feb 15 2003 Jakub Jelinek <jakub@redhat.com> 0.75-2
- update to 0.75 (eu-strip -g fix)

* Tue Feb 11 2003 Jakub Jelinek <jakub@redhat.com> 0.74-2
- update to 0.74 (fix for writing with some non-dirty sections)

* Thu Feb  6 2003 Jeff Johnson <jbj@redhat.com> 0.73-3
- another -0.73 update (with sparc fixes).
- do "make check" in %%check, not %%install, section.

* Mon Jan 27 2003 Jeff Johnson <jbj@redhat.com> 0.73-2
- update to 0.73 (with s390 fixes).

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Jan 22 2003 Jakub Jelinek <jakub@redhat.com> 0.72-4
- fix arguments to gelf_getsymshndx and elf_getshstrndx
- fix other warnings
- reenable checks on s390x

* Sat Jan 11 2003 Karsten Hopp <karsten@redhat.de> 0.72-3
- temporarily disable checks on s390x, until someone has
  time to look at it

* Thu Dec 12 2002 Jakub Jelinek <jakub@redhat.com> 0.72-2
- update to 0.72

* Wed Dec 11 2002 Jakub Jelinek <jakub@redhat.com> 0.71-2
- update to 0.71

* Wed Dec 11 2002 Jeff Johnson <jbj@redhat.com> 0.69-4
- update to 0.69.
- add "make check" and segfault avoidance patch.
- elfutils-libelf needs to run ldconfig.

* Tue Dec 10 2002 Jeff Johnson <jbj@redhat.com> 0.68-2
- update to 0.68.

* Fri Dec  6 2002 Jeff Johnson <jbj@redhat.com> 0.67-2
- update to 0.67.

* Tue Dec  3 2002 Jeff Johnson <jbj@redhat.com> 0.65-2
- update to 0.65.

* Mon Dec  2 2002 Jeff Johnson <jbj@redhat.com> 0.64-2
- update to 0.64.

* Sun Dec 1 2002 Ulrich Drepper <drepper@redhat.com> 0.64
- split packages further into elfutils-libelf

* Sat Nov 30 2002 Jeff Johnson <jbj@redhat.com> 0.63-2
- update to 0.63.

* Fri Nov 29 2002 Ulrich Drepper <drepper@redhat.com> 0.62
- Adjust for dropping libtool

* Sun Nov 24 2002 Jeff Johnson <jbj@redhat.com> 0.59-2
- update to 0.59

* Thu Nov 14 2002 Jeff Johnson <jbj@redhat.com> 0.56-2
- update to 0.56

* Thu Nov  7 2002 Jeff Johnson <jbj@redhat.com> 0.54-2
- update to 0.54

* Sun Oct 27 2002 Jeff Johnson <jbj@redhat.com> 0.53-2
- update to 0.53
- drop x86_64 hack, ICE fixed in gcc-3.2-11.

* Sat Oct 26 2002 Jeff Johnson <jbj@redhat.com> 0.52-3
- get beehive to punch a rhpkg generated package.

* Wed Oct 23 2002 Jeff Johnson <jbj@redhat.com> 0.52-2
- build in 8.0.1.
- x86_64: avoid gcc-3.2 ICE on x86_64 for now.

* Tue Oct 22 2002 Ulrich Drepper <drepper@redhat.com> 0.52
- Add libelf-devel to conflicts for elfutils-devel

* Mon Oct 21 2002 Ulrich Drepper <drepper@redhat.com> 0.50
- Split into runtime and devel package

* Fri Oct 18 2002 Ulrich Drepper <drepper@redhat.com> 0.49
- integrate into official sources

* Wed Oct 16 2002 Jeff Johnson <jbj@redhat.com> 0.46-1
- Swaddle.
