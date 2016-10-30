# TODO: provide configurations for other configurations (e.g. x11)?
#
# Conditional build:
%bcond_without	tests		# do not perform "make test"
%bcond_without	gtk2		# wxGTK2 packages support
%bcond_without	gtk3		# wxGTK3 packages support
%bcond_without	ansi		# ANSI wx packages support
%bcond_without	unicode		# Unicode wx packages support
#
%include	/usr/lib/rpm/macros.perl
%define		pdir	Alien
%define		pnam	wxWidgets
Summary:	Alien::wxWidgets - building, finding and using wxWidgets binaries
Summary(pl.UTF-8):	Alien::wxWidgets - budowanie, znajdowanie i wykorzystywanie binariów wxWidgets
Name:		perl-Alien-wxWidgets
Version:	0.67
Release:	3
# same as perl
License:	GPL v1+ or Artistic
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-module/Alien/%{pdir}-%{pnam}-%{version}.tar.gz
# Source0-md5:	510a7817fdaf59089b50a877a621d770
Patch0:		%{name}-nobuild.patch
URL:		http://search.cpan.org/dist/Alien-wxWidgets/
BuildRequires:	perl-ExtUtils-CBuilder >= 0.24
BuildRequires:	perl-Module-Build >= 0.28
BuildRequires:	perl-Module-Pluggable >= 3.1-4
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	perl(File::Spec) >= 1.50
BuildRequires:	rpm-perlprov >= 4.1-13
%if %{with gtk2}
%if %{with ansi}
BuildRequires:	wxGTK2-devel >= 2.6.3
BuildRequires:	wxGTK2-gl-devel >= 2.6.3
%endif
%if %{with unicode}
BuildRequires:	wxGTK2-unicode-devel >= 2.6.3
BuildRequires:	wxGTK2-unicode-gl-devel >= 2.6.3
%endif
%endif
%if %{with gtk3}
%if %{with ansi}
BuildRequires:	wxGTK3-devel >= 2.6.3
BuildRequires:	wxGTK3-gl-devel >= 2.6.3
%endif
%if %{with unicode}
BuildRequires:	wxGTK3-unicode-devel >= 2.6.3
BuildRequires:	wxGTK3-unicode-gl-devel >= 2.6.3
%endif
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		wx_ver		%(rpm -q wxWidgets-devel --qf '%%{VERSION}')
%define		wx_ver_tag	%(echo %{wx_ver} | tr . _)

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
for toolkit in %{?with_gtk2:gtk2} %{?with_gtk3:gtk3} ; do
for charset in %{?with_ansi:ansi} %{?with_unicode:unicode} ; do
export WX_CONFIG=wx-${toolkit}-${charset}-config
%{__perl} Build.PL \
	destdir=$RPM_BUILD_ROOT \
	installdirs=vendor \
	--wxWidgets-build=0

./Build

%{?with_tests:./Build test}
done
done

%install
rm -rf $RPM_BUILD_ROOT

./Build install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%dir %{perl_vendorarch}/Alien
%{perl_vendorarch}/Alien/wxWidgets.pm
%dir %{perl_vendorarch}/Alien/wxWidgets
%{perl_vendorarch}/Alien/wxWidgets/Utility.pm
%dir %{perl_vendorarch}/Alien/wxWidgets/Config
%if %{with gtk2}
%if %{with ansi}
%{perl_vendorarch}/Alien/wxWidgets/Config/gtk2_%{wx_ver_tag}_gcc_3_4.pm
%endif
%if %{with unicode}
%{perl_vendorarch}/Alien/wxWidgets/Config/gtk2_%{wx_ver_tag}_uni_gcc_3_4.pm
%endif
%endif
%if %{with gtk3}
# should be gtk3_*.pm?
%if %{with ansi}
%{perl_vendorarch}/Alien/wxWidgets/Config/gtk_%{wx_ver_tag}_gcc_3_4.pm
%endif
%if %{with unicode}
%{perl_vendorarch}/Alien/wxWidgets/Config/gtk_%{wx_ver_tag}_uni_gcc_3_4.pm
%endif
%endif
%{_mandir}/man3/Alien::wxWidgets*.3pm*
