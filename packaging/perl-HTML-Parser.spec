%define real_name HTML-Parser

Name:           perl-%{real_name}
Summary:        Perl module for parsing HTML
Version:        3.69
Release:        3%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
Source0:        %{real_name}-%{version}.tar.gz 
Source1001:     packaging/perl-HTML-Parser.manifest 
URL:            http://search.cpan.org/dist/HTML-Parser/
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildRequires:  perl(Carp)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(ExtUtils::ParseXS)
BuildRequires:  perl(HTML::Tagset) >= 3
BuildRequires:  perl(Test::More)
BuildRequires:  perl(URI)
BuildRequires:  perl(XSLoader)
BuildRequires:  perl(Pod::Simple)
BuildRequires:  perl(Test::Pod) 
Requires:       perl(HTML::Tagset) >= 3
Requires:       perl(URI)
Requires:       perl(XSLoader)
%if %{undefined perl_bootstrap}
# This creates cycle with perl-HTTP-Message. Weaken the dependency here because
# it's just a recommended dependency per META.yml.
BuildRequires:  perl(HTTP::Headers)
Requires:       perl(HTTP::Headers)
%endif

%{?perl_default_filter}
%{?perl_default_subpackage_tests}

%description
The HTML-Parser module for perl to parse and extract information from
HTML documents, including the HTML::Entities, HTML::HeadParser,
HTML::LinkExtor, HTML::PullParser, and HTML::TokeParser modules.

%prep
%setup -q -n HTML-Parser-3.69

chmod -c a-x eg/*

%build
cp %{SOURCE1001} .
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
#file=%{buildroot}%{_mandir}/man3/HTML::Entities.3pm
#iconv -f iso-8859-1 -t utf-8 <"$file" > "${file}_"
#mv -f "${file}_" "$file"
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type f -name '*.bs' -empty -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'
chmod -R u+w %{buildroot}/*

%check
make test

%files
%manifest perl-HTML-Parser.manifest
%doc Changes README TODO eg/
%{perl_vendorarch}/HTML/*
%{perl_vendorarch}/auto/HTML/*
#%{_mandir}/man3/*.3pm*


