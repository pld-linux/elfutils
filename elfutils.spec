Summary:	A collection of utilities and DSOs to handle compiled objects
Summary(pl):	Zestaw narz�dzi i bibliotek do obs�ugi skompilowanych obiekt�w
Name:		elfutils
Version:	0.76
Release:	8
License:	GPL
Group:		Development/Tools
Source0:	%{name}-%{version}.tar.gz
Patch0:		%{name}-pl.po.patch
#URL:		file://home/devel/drepper
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gcc >= 3.2
BuildRequires:	gettext-devel
BuildRequires:  libltdl-devel
BuildRequires:	sharutils
Requires:	elfutils-libelf = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define _programprefix eu-

%description
Elfutils is a collection of utilities, including ld (a linker), nm
(for listing symbols from object files), size (for listing the section
sizes of an object or archive file), strip (for discarding symbols),
readline (the see the raw ELF file structures), and elflint (to check
for well-formed ELF files). Also included are numerous helper
libraries which implement DWARF, ELF, and machine-specific ELF
handling.

%description -l pl
Elfutils to zestaw narz�dzi, sk�adaj�cy si� z ld (linkera), nm (do
listowania symboli z plik�w obiekt�w), size (do listowania rozmiar�w
sekcji plik�w obiekt�w lub archiw�w), strip (do usuwania symboli),
readline (do ogl�dania surowych struktur plik�w ELF) oraz elflint (do
sprawdzania poprawno�ci plik�w ELF). Do��czone s� tak�e liczne
biblioteki pomocnicze z zaimplementowan� obs�ug� DWARF, ELF i ELF
specyficznych dla architektury.

%package devel
Summary:	Development part of libraries to handle compiled objects
Summary(pl):	Cz�� programistyczna bibliotek do obs�ugi skompilowanych obiekt�w
Group:		Development/Libraries
Obsoletes:	libelf-devel
Requires:	elfutils = %{version}-%{release}

%description devel
The elfutils-devel package contains the development part of libraries
to create applications for handling compiled objects. libelf allows
you to access the internals of the ELF object file format, so you can
see the different sections of an ELF file. libebl provides some
higher-level ELF access functionality. libdwarf provides access to the
DWARF debugging information. libasm provides a programmable assembler
interface.

%description devel -l pl
Pakiet elfutils-devel zawiera cz�� programistyczn� bibliotek do
tworzenia aplikacji obs�uguj�cych skompilowane obiekty. libelf pozwala
na dost�p do wn�trzno�ci formatu pliku obiektowego ELF, co pozwala na
ogl�danie r�nych sekcji pliku ELF. libebl udost�pnia funkcjonalno��
dost�pu do plik�w ELF troch� wy�szego poziomu. libdwarf pozwala na
dost�p do informacji DWARF s�u��cych do odpluskwiania. libasm
udost�pnia programowalny interfejs asemblera.

%package libelf
Summary:	Library to read and write ELF files
Summary(pl):	Biblioteki do odczytu i zapisu plik�w ELF
Group:		Libraries
#Obsoletes:	libelf

%description libelf
The elfutils-libelf package provides a DSO which allows reading and
writing ELF files on a high level. Third party programs depend on this
package to read internals of ELF files. The programs of the elfutils
package use it also to generate new ELF files.

%description libelf -l pl
Pakiet elfutils-libelf udost�pnia bibliotek� dzielon�, kt�ra pozwala
na wysokopoziomowe czytanie i zapisywanie plik�w ELF. Inne programy
wymagaj� tego pakietu, aby odczytywa� zawarto�� plik�w ELF. Programy z
pakietu elfutils u�ywaj� jej tak�e do generowania nowych plik�w ELF.

%package static
Summary:	Static libraries to handle compiled objects
Summary(pl):	Statyczne biblioteki do obs�ugi skompilowanych obiekt�w
Group:		Development/Libraries
Obsoletes:	libelf-static
Requires:	elfutils-devel = %{version}-%{release}

%description static
The elfutils-static package contains the static libraries to create
applications for handling compiled objects. libelf allows you to
access the internals of the ELF object file format, so you can see the
different sections of an ELF file. libebl provides some higher-level
ELF access functionality. libdwarf provides access to the DWARF
debugging information. libasm provides a programmable assembler
interface.

%description static -l pl
Pakiet elfutils-static zawiera statyczne biblioteki do tworzenia
aplikacji obs�uguj�cych skompilowane obiekty. libelf pozwala na dost�p
do wn�trzno�ci formatu pliku obiektowego ELF, co pozwala na ogl�danie
r�nych sekcji pliku ELF. libebl udost�pnia funkcjonalno�� dost�pu do
plik�w ELF troch� wy�szego poziomu. libdwarf pozwala na dost�p do
informacji DWARF s�u��cych do odpluskwiania. libasm udost�pnia
programowalny interfejs asemblera.

%prep
%setup -q
%patch -p1

%build
%{__aclocal}
%{__autoheader}
%{__automake}
%{__autoconf}
%configure \
	--program-prefix=%{_programprefix} \
	--enable-shared

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_prefix}

# *OBJEXT must be passed to workaround problem with messed gettext,
# which doesn't like *-po dir names
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	CATOBJEXT=.gmo INSTOBJEXT=.mo

chmod +x $RPM_BUILD_ROOT%{_prefix}/%{_lib}/lib*.so*
chmod +x $RPM_BUILD_ROOT%{_prefix}/%{_lib}/elfutils/lib*.so*

%find_lang libelf
%find_lang libasm
%find_lang libdwarf
%find_lang libebl
%find_lang %{name}
cat libasm.lang libdwarf.lang libebl.lang >> %{name}.lang

%clean
rm -rf ${RPM_BUILD_ROOT}

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	libelf -p /sbin/ldconfig
%postun	libelf -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README TODO
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*-*.so
%dir %{_libdir}/elfutils
%attr(755,root,root) %{_libdir}/elfutils/lib*.so
%exclude %{_libdir}/libelf-*.so

%files devel
%defattr(644,root,root,755)
%doc libdwarf/AVAILABLE
%{_includedir}/*
%{_libdir}/lib*.so
%exclude %{_libdir}/lib*-*.so

%files libelf -f libelf.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libelf-*.so

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
