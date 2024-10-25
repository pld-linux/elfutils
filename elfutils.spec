# TODO:
# - package debuginfod.service
#
# Conditional build:
%bcond_without	debuginfod	# debuginfod server and client
%bcond_without	tests	# do not perform tests
#
Summary:	A collection of utilities and DSOs to handle compiled objects
Summary(pl.UTF-8):	Zestaw narzędzi i bibliotek do obsługi skompilowanych obiektów
Name:		elfutils
Version:	0.192
Release:	1
License:	GPL v2+ or LGPL v3+ (libraries), GPL v3+ (programs)
Group:		Development/Tools
Source0:	https://sourceware.org/elfutils/ftp/%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	a6bb1efc147302cfc15b5c2b827f186a
Patch0:		%{name}-pl.po.patch
Patch1:		%{name}-debian-manpages.patch
Patch3:		%{name}-align.patch
Patch4:		%{name}-paxflags.patch
Patch5:		%{name}-sparc.patch
Patch6:		disable-tests.patch
URL:		https://sourceware.org/elfutils/
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake >= 1:1.11
%{?with_tests:BuildRequires:	bsdtar}
BuildRequires:	bzip2-devel
BuildRequires:	gawk
BuildRequires:	gcc >= 6:4.3
BuildRequires:	gettext-tools >= 0.19.6
BuildRequires:	glibc-devel >= 6:2.7
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	perl-tools-pod
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.527
BuildRequires:	sharutils
BuildRequires:	xz-devel
BuildRequires:	zlib-devel
BuildRequires:	zstd-devel >= 1.4.0
%if %{with tests} && %(test -d /proc/self ; echo $?)
# native test needs proc (for libdwfl -p PID to work)
BuildRequires:	MOUNTED_PROC
%endif
%if %{with debuginfod}
BuildRequires:	curl-devel >= 7.29.0
BuildRequires:	json-c-devel >= 0.11
BuildRequires:	libarchive-devel >= 3.1.2
BuildRequires:	libmicrohttpd-devel >= 0.9.33
BuildRequires:	sqlite3-devel >= 3.7.17
%endif
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# fails to build with -Wl,-s
%define		filterout_ld	(-Wl,)?-[sS] (-Wl,)?--strip.*
%if %{with tests} && 0%(echo %{rpmcflags} | grep -q '\<-g' ; echo $?)
# tests require debug symbols
%define		specflags	-g
%endif

%define		programprefix	eu-

%description
Elfutils is a collection of utilities, including ld (a linker), nm
(for listing symbols from object files), size (for listing the section
sizes of an object or archive file), strip (for discarding symbols),
readline (the see the raw ELF file structures), and elflint (to check
for well-formed ELF files).

%description -l pl.UTF-8
Elfutils to zestaw narzędzi, składający się z ld (linkera), nm (do
listowania symboli z plików obiektów), size (do listowania rozmiarów
sekcji plików obiektów lub archiwów), strip (do usuwania symboli),
readline (do oglądania surowych struktur plików ELF) oraz elflint (do
sprawdzania poprawności plików ELF).

%package libs
Summary:	Libraries to handle compiled objects
Summary(pl.UTF-8):	Biblioteki do obsługi skompilowanych obiektów
Group:		Libraries
Requires:	%{name}-libelf = %{version}-%{release}
Requires:	zstd >= 1.4.0

%description libs
Libraries which implement DWARF, ELF, and machine-specific ELF
handling.

%description libs -l pl.UTF-8
Biblioteki z zaimplementowaną obsługą DWARF, ELF i ELF specyficznych
dla architektury.

%package devel
Summary:	Development part of libraries to handle compiled objects
Summary(pl.UTF-8):	Część programistyczna bibliotek do obsługi skompilowanych obiektów
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	bzip2-devel
Requires:	xz-devel
Requires:	zlib-devel
Requires:	zstd-devel >= 1.4.0
Obsoletes:	libelf-devel < 0.8.14
Obsoletes:	libelf0-devel < 0.8.14

%description devel
The elfutils-devel package contains the development part of libraries
to create applications for handling compiled objects. libelf allows
you to access the internals of the ELF object file format, so you can
see the different sections of an ELF file. libdw provides access to
the DWARF debugging information. libasm provides a programmable
assembler interface.

%description devel -l pl.UTF-8
Pakiet elfutils-devel zawiera część programistyczną bibliotek do
tworzenia aplikacji obsługujących skompilowane obiekty. libelf pozwala
na dostęp do wnętrzności formatu pliku obiektowego ELF, co pozwala na
oglądanie różnych sekcji pliku ELF. libdw pozwala na dostęp do
informacji DWARF służących do odpluskwiania. libasm udostępnia
programowalny interfejs asemblera.

%package libelf
Summary:	Library to read and write ELF files
Summary(pl.UTF-8):	Biblioteki do odczytu i zapisu plików ELF
Group:		Libraries
#Obsoletes:	libelf

%description libelf
The elfutils-libelf package provides a DSO which allows reading and
writing ELF files on a high level. Third party programs depend on this
package to read internals of ELF files. The programs of the elfutils
package use it also to generate new ELF files.

%description libelf -l pl.UTF-8
Pakiet elfutils-libelf udostępnia bibliotekę dzieloną, która pozwala
na wysokopoziomowe czytanie i zapisywanie plików ELF. Inne programy
wymagają tego pakietu, aby odczytywać zawartość plików ELF. Programy z
pakietu elfutils używają jej także do generowania nowych plików ELF.

%package static
Summary:	Static libraries to handle compiled objects
Summary(pl.UTF-8):	Statyczne biblioteki do obsługi skompilowanych obiektów
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	zstd >= 1.4.0
Obsoletes:	libelf-static < 0.8.14

%description static
The elfutils-static package contains the static libraries to create
applications for handling compiled objects. libelf allows you to
access the internals of the ELF object file format, so you can see the
different sections of an ELF file. libdw provides access to the DWARF
debugging information. libasm provides a programmable assembler
interface.

%description static -l pl.UTF-8
Pakiet elfutils-static zawiera statyczne biblioteki do tworzenia
aplikacji obsługujących skompilowane obiekty. libelf pozwala na dostęp
do wnętrzności formatu pliku obiektowego ELF, co pozwala na oglądanie
różnych sekcji pliku ELF. libdw pozwala na dostęp do informacji DWARF
służących do odpluskwiania. libasm udostępnia programowalny interfejs
asemblera.

%package debuginfod
Summary:	debuginfod server and client
Summary(pl.UTF-8):	Serwer i klient debuginfod
Group:		Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	%{name}-debuginfod-libs = %{version}-%{release}
Requires:	json-c >= 0.11
Requires:	libarchive >= 3.1.2
Requires:	libmicrohttpd >= 0.9.33
Requires:	sqlite3-libs >= 3.7.17

%description debuginfod
debuginfod server and client.

%description debuginfod -l pl.UTF-8
Serwer i klient debuginfod.

%package debuginfod-libs
Summary:	debuginfod library
Summary(pl.UTF-8):	Biblioteka debuginfod
Group:		Libraries
Requires:	%{name}-libelf = %{version}-%{release}
Requires:	curl-libs >= 7.29.0
Requires:	json-c >= 0.11
Conflicts:	elfutils-debuginfod < 0.187-3

%description debuginfod-libs
debuginfod library.

%description debuginfod-libs -l pl.UTF-8
Biblioteka debuginfod.

%package debuginfod-devel
Summary:	Header file for debuginfod library
Summary(pl.UTF-8):	Plik nagłówkowy biblioteki debuginfod
Group:		Development/Libraries
Requires:	%{name}-debuginfod-libs = %{version}-%{release}
Requires:	%{name}-devel = %{version}-%{release}

%description debuginfod-devel
Header file for debuginfod library.

%description debuginfod-devel -l pl.UTF-8
Plik nagłówkowy biblioteki debuginfod.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%{__rm} po/stamp-po

# temporarily disable failing tests (depending on arch)
%ifarch x32
%{__sed} -i -e 's/run-backtrace-native-biarch.sh//' tests/Makefile.am
%endif

# make sure this is not even tried on arch it has no chance to run
%ifarch %{ix86}
%{__sed} -i -e 's/run-disasm-x86-64.sh//' tests/Makefile.am
%endif

%build
#%%{__gettextize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	%{__enable_disable debuginfod} \
	--program-prefix=%{programprefix}

# make check depends on test-nlist not stripped
%{__perl} -pi -e 's/^(LDFLAGS =.*)-s/$1/' tests/Makefile

%{__make}
%{__make} -C debian/man

%if %{with tests}
# some tests rely on English messages
LC_ALL=C \
%{__make} -C tests check
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_mandir}/man1,/%{_lib}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install debian/man/*.1 $RPM_BUILD_ROOT%{_mandir}/man1

%{__mv} $RPM_BUILD_ROOT%{_libdir}/{libelf-*.so,libelf.so.*} $RPM_BUILD_ROOT/%{_lib}
ln -sf /%{_lib}/$(basename $RPM_BUILD_ROOT/%{_lib}/libelf-*.so) \
	$RPM_BUILD_ROOT%{_libdir}/libelf.so

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%post	libelf -p /sbin/ldconfig
%postun	libelf -p /sbin/ldconfig

%post	debuginfod-libs -p /sbin/ldconfig
%postun	debuginfod-libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS CONTRIBUTING ChangeLog NEWS NOTES README THANKS TODO
%attr(755,root,root) %{_bindir}/eu-*
%{_mandir}/man1/eu-*.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libasm-*.so
%attr(755,root,root) %ghost %{_libdir}/libasm.so.1
%attr(755,root,root) %{_libdir}/libdw-*.so
%attr(755,root,root) %ghost %{_libdir}/libdw.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libasm.so
%attr(755,root,root) %{_libdir}/libdw.so
%attr(755,root,root) %{_libdir}/libelf.so
%{_includedir}/dwarf.h
%{_includedir}/gelf.h
%{_includedir}/libelf.h
%{_includedir}/nlist.h
%dir %{_includedir}/elfutils
%{_includedir}/elfutils/elf-knowledge.h
%{_includedir}/elfutils/known-dwarf.h
%{_includedir}/elfutils/libasm.h
%{_includedir}/elfutils/libdw.h
%{_includedir}/elfutils/libdwelf.h
%{_includedir}/elfutils/libdwfl.h
%{_includedir}/elfutils/version.h
%{_pkgconfigdir}/libdw.pc
%{_pkgconfigdir}/libelf.pc
%{_mandir}/man3/elf*.3*
%{_mandir}/man3/libelf.3*

%files libelf -f %{name}.lang
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/libelf-*.so
%attr(755,root,root) %ghost /%{_lib}/libelf.so.1

%files static
%defattr(644,root,root,755)
%{_libdir}/libasm.a
%{_libdir}/libdw.a
%{_libdir}/libelf.a

%if %{with debuginfod}
%files debuginfod
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/debuginfod
%attr(755,root,root) %{_bindir}/debuginfod-find
%{_mandir}/man1/debuginfod-find.1*
%{_mandir}/man7/debuginfod-client-config.7*
%{_mandir}/man8/debuginfod.8*
# uncomment after packaging debuginfod.service
#%{_mandir}/man8/debuginfod.service.8*
%attr(755,root,root) /etc/profile.d/debuginfod.sh
%attr(755,root,root) /etc/profile.d/debuginfod.csh
# TODO: (but dir owned by fish currently)
#%{_datadir}/fish/vendor_conf.d/debuginfod.fish

%files debuginfod-libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdebuginfod-*.so
%attr(755,root,root) %ghost %{_libdir}/libdebuginfod.so.1

%files debuginfod-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdebuginfod.so
%{_includedir}/elfutils/debuginfod.h
%{_pkgconfigdir}/libdebuginfod.pc
%{_mandir}/man3/debuginfod_*.3*
%endif
