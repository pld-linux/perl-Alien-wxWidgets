#
# Conditional build:
%bcond_without	tests	# do not perform "make test"
%bcond_with	unicode	# use Unicode version of wxGTK2
#
%include	/usr/lib/rpm/macros.perl
%define		pdir	Alien
%define		pnam	wxWidgets
Summary:	Alien::wxWidgets - building, finding and using wxWidgets binaries
Summary(pl.UTF-8):	Alien::wxWidgets - budowanie, znajdowanie i wykorzystywanie binariów wxWidgets
Name:		perl-Alien-wxWidgets
Version:	0.43
Release:	0.1
# same as perl
License:	GPL v1+ or Artistic
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-module/Alien/%{pdir}-%{pnam}-%{version}.tar.gz
# Source0-md5:	5dacc6e2c2e175458fe8377aa26b019a
Patch0:		%{name}-nobuild.patch
URL:		http://search.cpan.org/dist/Alien-wxWidgets/
BuildRequires:	perl-Module-Build >= 0.2611-1
BuildRequires:	perl-Module-Pluggable >= 3.1-4
BuildRequires:	perl-ExtUtils-CBuilder >= 0.24
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRequires:	wxGTK2-%{?with_unicode:unicode-}devel >= 2.6.3
BuildRequires:	wxGTK2-%{?with_unicode:unicode-}gl-devel >= 2.6.3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Alien::wxWidgets allows wxPerl to easily find information about your
wxWidgets installation. It can store this information for multiple
wxWidgets versions or configurations (debug, Unicode, etc.). It can
also build and install a private copy of wxWidgets as part of the
build process.

%description -l pl.UTF-8
Alien::wxWidgets pozwala wxPerlowi łatwo uzyskać informacje na temat
instalacji wxWidgets. Może przechowywać informacje o wielu wersjach
lub konfiguracjach (debug, Unicode, itp.). Może także zbudować i
zainstalować prywatną kopię wxWidgets jako część procesu budowania.

%prep
%setup -q -n %{pdir}-%{pnam}-%{version}
%patch0 -p1

%build
WX_CONFIG=wx-gtk2-%{?with_unicode:unicode}%{!?with_unicode:ansi}-config
export WX_CONFIG
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor

%{__make} \
	CC="%{__cc}" \
	OPTIMIZE="%{rpmcflags}"

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%dir %{perl_vendorarch}/Alien
%{perl_vendorarch}/Alien/*.pm
%dir %{perl_vendorarch}/Alien/wxWidgets
%{perl_vendorarch}/Alien/wxWidgets/*.pm
%dir %{perl_vendorarch}/auto/Alien
%dir %{perl_vendorarch}/auto/Alien/wxWidgets
%{perl_vendorarch}/Alien/wxWidgets/*
%{_mandir}/man3/*
