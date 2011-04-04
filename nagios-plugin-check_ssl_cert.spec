%define		plugin	check_ssl_cert
Summary:	Nagios plugin to check the CA and validity of an X.509 certificate
Summary(pl.UTF-8):	Wtyczka Nagiosa sprawdzająca CA i ważność certyfikatu X.509
Name:		nagios-plugin-%{plugin}
Version:	1.9.1
Release:	1
License:	GPL v3
Group:		Networking
Source0:	https://trac.id.ethz.ch/projects/nagios_plugins/downloads/%{plugin}-%{version}.tar.gz
# Source0-md5:	26b768e65e244f1057b443d7b4c8d49d
Source1:	check_ssl_cert.cfg
Patch0:		ca_path.patch
URL:		https://trac.id.ethz.ch/projects/nagios_plugins/wiki/check_ssl_cert
BuildRequires:	rpm >= 4.4.9-56
Requires:	expect
Requires:	nagios-common
Requires:	sed >= 4.0
Suggests:	ca-certificates-update
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/nagios/plugins
%define		plugindir	%{_prefix}/lib/nagios/plugins
%if "%{pld_release}" == "th"
%define		openssldir	/etc/openssl/certs
%else
%define		openssldir	/var/lib/openssl/certs
%endif

%description
check_ssl_cert is a Nagios plugin to check X.509 certificates. It
checks if the server is running and delivers a valid certificate. It
also checks if the CA matches a given pattern, and checks the
validity.

%description -l pl.UTF-8
Wtyczka Nagiosa sprawdzająca certyfikaty X.509. Wtyczka ta sprawdza
czy serwer działa poprawnie oraz czy dostarcza ważny certyfikat.
Dodatkowo sprawdza czy CA pasuje do określonego wzorca i weryfikuje
jego poprawność.

%prep
%setup -q -n %{plugin}-%{version}
%patch0 -p1
%{__sed} -i -e 's,@cadir@,%{openssldir},' %{plugin}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{plugindir},%{_mandir}/man1}
install -p %{plugin} $RPM_BUILD_ROOT%{plugindir}/%{plugin}
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/%{plugin}.cfg
cp -p check_ssl_cert.1 $RPM_BUILD_ROOT%{_mandir}/man1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYRIGHT INSTALL NEWS README TODO VERSION
%attr(640,root,nagios) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{plugin}.cfg
%attr(755,root,root) %{plugindir}/%{plugin}
%{_mandir}/man1/check_ssl_cert.1*