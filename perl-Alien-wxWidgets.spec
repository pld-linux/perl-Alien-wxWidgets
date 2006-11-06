#
# Conditional build:
%bcond_without	tests	# do not perform "make test"
%bcond_with	unicode	# use Unicode version of wxGTK2
#
%include	/usr/lib/rpm/macros.perl
%define		pdir	Alien
%define		pnam	wxWidgets
Summary:	Alien::wxWidgets - building, finding and using wxWidgets binaries
Summary(pl):	Alien::wxWidgets - budowanie, znajdowanie i wykorzystywanie binariów wxWidgets
Name:		perl-Alien-wxWidgets
Version:	0.22
Release:	0.1
# same as perl
License:	GPL v1+ or Artistic
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-module/Alien/%{pdir}-%{pnam}-%{version}.tar.gz
# Source0-md5:	98de414f8d378170ede6cf96a0e2f73e
Patch0:		%{name}-nobuild.patch
URL:		http://search.cpan.org/dist/Alien-wxWidgets/
BuildRequires:  perl-Module-Build >= 0.2611-1
BuildRequires:  perl-Module-Pluggable >= 3.1-4
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRequires:  wxGTK2-%{?with_unicode:unicode-}devel >= 2.6.3
BuildRequires:  wxGTK2-%{?with_unicode:unicode-}gl-devel >= 2.6.3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Alien::wxWidgets allows wxPerl to easily find information about your
wxWidgets installation. It can store this information for multiple
wxWidgets versions or configurations (debug, Unicode, etc.). It can
also build and install a private copy of wxWidgets as part of the
build process.

%description -l pl
Alien::wxWidgets pozwala wxPerlowi ³atwo uzyskaæ informacje na temat
instalacji wxWidgets. Mo¿e przechowywaæ informacje o wielu wersjach
lub konfiguracjach (debug, Unicode, itp.). Mo¿e tak¿e zbudowaæ i
zainstalowaæ prywatn± kopiê wxWidgets jako czê¶æ procesu budowania.

%prep
%setup -q -n %{pdir}-%{pnam}-%{version}
%patch0 -p1

%build
WX_CONFIG=wx-gtk2-%{?with_unicode:unicode}%{!?with_unicode:ansi}-config
export WX_CONFIG
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor
    
%{__make} \
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
%{perl_vendorarch}/auto/Alien/wxWidgets/*
%{_mandir}/man3/*
