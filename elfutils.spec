#
# Conditional build:
%bcond_without	tests	# do not perform tests
#
Summary:	A collection of utilities and DSOs to handle compiled objects
Summary(pl.UTF-8):	Zestaw narzędzi i bibliotek do obsługi skompilowanych obiektów
Name:		elfutils
Version:	0.177
Release:	0.1
License:	GPL v2+ or LGPL v3+ (libraries), GPL v3+ (programs)
Group:		Development/Tools
Source0:	https://sourceware.org/elfutils/ftp/%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	0b583722f911e1632544718d502aab87
Patch0:		%{name}-pl.po.patch
Patch1:		%{name}-debian-manpages.patch
Patch2:		%{name}-awk.patch
Patch3:		%{name}-align.patch
Patch4:		%{name}-paxflags.patch
Patch5:		%{name}-sparc.patch
URL:		https://sourceware.org/elfutils/
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake >= 1:1.11
BuildRequires:	bzip2-devel
BuildRequires:	gawk
BuildRequires:	gcc >= 6:4.3
BuildRequires:	gettext-tools
BuildRequires:	glibc-devel >= 6:2.7
BuildRequires:	libstdc++-devel
BuildRequires:	perl-tools-pod
BuildRequires:	rpmbuild(macros) >= 1.315
BuildRequires:	sharutils
BuildRequires:	xz-devel
BuildRequires:	zlib-devel
%if %{with tests} && %(test -d /proc/self ; echo $?)
# native test needs proc (for libdwfl -p PID to work)
BuildRequires:	MOUNTED_PROC
%endif
Requires:	%{name}-libelf = %{version}-%{release}
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
for well-formed ELF files). Also included are numerous helper
libraries which implement DWARF, ELF, and machine-specific ELF
handling.

%description -l pl.UTF-8
Elfutils to zestaw narzędzi, składający się z ld (linkera), nm (do
listowania symboli z plików obiektów), size (do listowania rozmiarów
sekcji plików obiektów lub archiwów), strip (do usuwania symboli),
readline (do oglądania surowych struktur plików ELF) oraz elflint (do
sprawdzania poprawności plików ELF). Dołączone są także liczne
biblioteki pomocnicze z zaimplementowaną obsługą DWARF, ELF i ELF
specyficznych dla architektury.

%package devel
Summary:	Development part of libraries to handle compiled objects
Summary(pl.UTF-8):	Część programistyczna bibliotek do obsługi skompilowanych obiektów
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	bzip2-devel
Requires:	xz-devel
Requires:	zlib-devel
Obsoletes:	libelf-devel

%description devel
The elfutils-devel package contains the development part of libraries
to create applications for handling compiled objects. libelf allows
you to access the internals of the ELF object file format, so you can
see the different sections of an ELF file. libebl provides some
higher-level ELF access functionality. libdwarf provides access to the
DWARF debugging information. libasm provides a programmable assembler
interface.

%description devel -l pl.UTF-8
Pakiet elfutils-devel zawiera część programistyczną bibliotek do
tworzenia aplikacji obsługujących skompilowane obiekty. libelf pozwala
na dostęp do wnętrzności formatu pliku obiektowego ELF, co pozwala na
oglądanie różnych sekcji pliku ELF. libebl udostępnia funkcjonalność
dostępu do plików ELF trochę wyższego poziomu. libdwarf pozwala na
dostęp do informacji DWARF służących do odpluskwiania. libasm
udostępnia programowalny interfejs asemblera.

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
Obsoletes:	libelf-static

%description static
The elfutils-static package contains the static libraries to create
applications for handling compiled objects. libelf allows you to
access the internals of the ELF object file format, so you can see the
different sections of an ELF file. libebl provides some higher-level
ELF access functionality. libdwarf provides access to the DWARF
debugging information. libasm provides a programmable assembler
interface.

%description static -l pl.UTF-8
Pakiet elfutils-static zawiera statyczne biblioteki do tworzenia
aplikacji obsługujących skompilowane obiekty. libelf pozwala na dostęp
do wnętrzności formatu pliku obiektowego ELF, co pozwala na oglądanie
różnych sekcji pliku ELF. libebl udostępnia funkcjonalność dostępu do
plików ELF trochę wyższego poziomu. libdwarf pozwala na dostęp do
informacji DWARF służących do odpluskwiania. libasm udostępnia
programowalny interfejs asemblera.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%{__rm} po/stamp-po

# temporarily disable failing tests (depending on arch)
%ifarch x32
%{__sed} -i -e 's/run-backtrace-native-biarch.sh//' tests/Makefile.am
%endif

%build
#%%{__gettextize}
%{__aclocal} -I m4
%{__autoheader}
%{__autoconf}
%{__automake}
%configure \
	--disable-silent-rules \
	--disable-werror \
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

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	libelf -p /sbin/ldconfig
%postun	libelf -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS CONTRIBUTING ChangeLog NEWS NOTES README THANKS TODO
%attr(755,root,root) %{_bindir}/eu-*
%attr(755,root,root) %{_libdir}/libasm-*.so
%attr(755,root,root) %ghost %{_libdir}/libasm.so.1
%attr(755,root,root) %{_libdir}/libdw-*.so
%attr(755,root,root) %ghost %{_libdir}/libdw.so.1
%dir %{_libdir}/elfutils
%attr(755,root,root) %{_libdir}/elfutils/lib*.so
%{_mandir}/man1/eu-*.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libasm.so
%attr(755,root,root) %{_libdir}/libdw.so
%attr(755,root,root) %{_libdir}/libelf.so
%{_libdir}/libebl.a
%{_includedir}/elfutils
%{_includedir}/dwarf.h
%{_includedir}/gelf.h
%{_includedir}/libelf.h
%{_includedir}/nlist.h
%{_pkgconfigdir}/libdw.pc
%{_pkgconfigdir}/libelf.pc

%files libelf -f %{name}.lang
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/libelf-*.so
%attr(755,root,root) %ghost /%{_lib}/libelf.so.1

%files static
%defattr(644,root,root,755)
%{_libdir}/libasm.a
%{_libdir}/libdw.a
%{_libdir}/libelf.a
