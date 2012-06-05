Name:       perl-HTML-Parser
Summary:    Perl module for parsing HTML
Version:    3.65
Release:    1
Group:      Development/Libraries
License:    GPL+ or Artistic
URL:        http://search.cpan.org/dist/HTML-Parser/
Source0:    %{name}-%{version}.tar.gz
Source1001: packaging/perl-HTML-Parser.manifest 
Requires:   perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:   perl(HTML::Tagset) >= 3.03
BuildRequires:  perl(HTML::Tagset) >= 3.03, perl(ExtUtils::MakeMaker), perl(Test::Simple)


%description
The HTML-Parser module for perl to parse and extract information from
HTML documents, including the HTML::Entities, HTML::HeadParser,
HTML::LinkExtor, HTML::PullParser, and HTML::TokeParser modules.


%prep
%setup -q

chmod -c a-x eg/*

%build
cp %{SOURCE1001} .

if test -f Makefile.PL; then
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?jobs:-j%jobs}
else
%{__perl} Build.PL  --installdirs vendor
./Build
fi

%install
rm -rf %{buildroot}
if test -f Makefile.PL; then
make pure_install PERL_INSTALL_ROOT=%{buildroot}
else
./Build install --installdirs vendor
fi
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'
find %{buildroot} -type f -name '*.bs' -empty -exec rm -f {} ';'
%{_fixperms} %{buildroot}/*

file=$RPM_BUILD_ROOT%{_mandir}/man3/HTML::Entities.3pm
iconv -f iso-8859-1 -t utf-8 <"$file" > "${file}_"
mv -f "${file}_" "$file"
chmod -R u+w $RPM_BUILD_ROOT/*

%check
make test

%files
%manifest perl-HTML-Parser.manifest
%defattr(-,root,root,-)
%{perl_vendorarch}/HTML/*
%{perl_vendorarch}/auto/HTML/*
%doc %{_mandir}/man3/*.3pm*
