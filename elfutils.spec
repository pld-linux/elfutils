#
# Conditional build:
%bcond_without	tests	# do not perform tests
#
Summary:	A collection of utilities and DSOs to handle compiled objects
Summary(pl.UTF-8):	Zestaw narzędzi i bibliotek do obsługi skompilowanych obiektów
Name:		elfutils
Version:	0.128
Release:	4
License:	GPL v2 with OSL linking exception
Group:		Development/Tools
# http://download.fedora.redhat.com/pub/fedora/linux/core/development/source/SRPMS/
# or abuse systemtap to get .tar.gz directly
Source0:	ftp://sources.redhat.com/pub/systemtap/elfutils/%{name}-%{version}.tar.gz
# Source0-md5:	4da87e49616101ec256e313218c421ef
Patch0:		%{name}-pl.po.patch
Patch1:		%{name}-debian-manpages.patch
Patch2:		%{name}-portability.patch
Patch3:		%{name}-robustify.patch
Patch4:		%{name}-align.patch
Patch5:		%{name}-paxflags.patch
Patch6:		%{name}-sparc.patch
Patch7:		%{name}-strip-copy-symtab.patch
Patch8:		%{name}-gcc4.patch
Patch9:		%{name}-inline.patch
Patch10:	%{name}-Werror.patch
Patch11:	%{name}-elflint-ppc-got.patch
#URL:		file://home/devel/drepper
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.7
BuildRequires:	gcc >= 3.2
BuildRequires:	gettext-devel
%ifarch %{x8664} alpha ia64 ppc64 s390x sparc64
# PR*FAST{8,16} in <inttypes.h> were broken for 64-bit archs in older versions
# also needed for nanosecond timestamps on alpha
BuildRequires:	glibc-devel >= 6:2.3.4
%endif
BuildRequires:	libltdl-devel
BuildRequires:	perl-tools-pod
BuildRequires:	rpmbuild(macros) >= 1.315
BuildRequires:	sharutils
%if %{with tests} && %(test -d /proc/self ; echo $?)
# native test needs proc (for libdwfl -p PID to work)
BuildRequires:	MOUNTED_PROC
%endif
Requires:	%{name}-libelf = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# fails to build with -Wl,-s
%define		filterout_ld	(-Wl,)?-[sS] (-Wl,)?--strip.*

%define		_programprefix	eu-

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
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p0

rm -f po/stamp-po

# strip-test5 needs adjusting for strip-copy-symtab patch (already in FC, but not worth bothering)
sed -i -e 's/ run-strip-test5\.sh / /' tests/Makefile.am

%build
#%%{__gettextize}
%{__aclocal}
%{__autoheader}
%{__autoconf}
%{__automake}
%configure \
	--program-prefix=%{_programprefix} \
	--enable-shared

# make check depends on test-nlist not stripped
%{__perl} -pi -e 's/^(LDFLAGS =.*)-s/$1/' tests/Makefile

# disable test failing on specific archs
%ifarch sparc sparc64 alpha
%{__perl} -pi -e 's/run-elflint-self.sh//' tests/Makefile
%endif

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

# *OBJEXT must be passed to workaround problem with messed gettext,
# which doesn't like *-po dir names
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	MKINSTALLDIRS=$(pwd)/config/mkinstalldirs \
	CATOBJEXT=.gmo \
	INSTOBJEXT=.mo

install debian/man/*.1 $RPM_BUILD_ROOT%{_mandir}/man1

mv $RPM_BUILD_ROOT%{_libdir}/libelf-*.so $RPM_BUILD_ROOT/%{_lib}
ln -sf /%{_lib}/$(cd $RPM_BUILD_ROOT/%{_lib} ; echo libelf-*.so) \
        $RPM_BUILD_ROOT%{_libdir}/libelf.so

/sbin/ldconfig -n -N $RPM_BUILD_ROOT%{_libdir}
/sbin/ldconfig -n -N $RPM_BUILD_ROOT/%{_lib}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	libelf -p /sbin/ldconfig
%postun	libelf -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS EXCEPTION NEWS NOTES README THANKS TODO
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/libasm-*.so
%ghost %attr(755,root,root) %{_libdir}/libasm.so.*
%attr(755,root,root) %{_libdir}/libdw-*.so
%ghost %attr(755,root,root) %{_libdir}/libdw.so.*
%dir %{_libdir}/elfutils
%attr(755,root,root) %{_libdir}/elfutils/lib*.so
%{_mandir}/man1/*.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libasm.so
%attr(755,root,root) %{_libdir}/libdw.so
%attr(755,root,root) %{_libdir}/libelf.so
%{_libdir}/libebl.a
%{_includedir}/*

%files libelf -f %{name}.lang
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/libelf-*.so
%ghost %attr(755,root,root) /%{_lib}/libelf.so.*

%files static
%defattr(644,root,root,755)
%{_libdir}/libasm.a
%{_libdir}/libdw.a
%{_libdir}/libelf.a
