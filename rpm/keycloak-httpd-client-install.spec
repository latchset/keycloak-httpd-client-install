%global srcname keycloak-httpd-client-install
%global summary Tools to configure Apache HTTPD as Keycloak client

Name:           %{srcname}
Version:        1.4
Release:        %{?release_string}%{!?release_string: 1}%{?dist}
Summary:        %{summary}


License:        GPL-3.0-or-later
URL:            https://github.com/lachset/keycloak-httpd-client-install
Source0:        https://github.com/lachset/keycloak-httpd-client-install/releases/download/%{version}/keycloak-httpd-client-install-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python3-devel
Requires:       %{_bindir}/keycloak-httpd-client-install

%description
Keycloak is a federated Identity Provider (IdP). Apache HTTPD supports
a variety of authentication modules which can be configured to utilize
a Keycloak IdP to perform authentication. This package contains
libraries and tools which can automate and simplify configuring an
Apache HTTPD authentication module and registering as a client of a
Keycloak IdP.

%package -n python3-%{srcname}
Summary:        %{summary}

Requires:       %{name} = %{version}-%{release}

%description -n python3-%{srcname}
Keycloak is an authentication server. This package contains libraries and
programs which can invoke the Keycloak REST API and configure clients
of a Keycloak server.

%prep
%autosetup -n %{srcname}-%{version} -p1

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%check
%pyproject_check_import

%install
%pyproject_install
%pyproject_save_files '*'
install -d -m 755 %{buildroot}/%{_mandir}/man8
install -c -m 644 doc/keycloak-httpd-client-install.8 %{buildroot}/%{_mandir}/man8
gzip %{buildroot}/%{_mandir}/man8/keycloak-httpd-client-install.8

%files
%license LICENSE.txt
%doc README.md doc/ChangeLog
%{_datadir}/%{srcname}/

%files -n python3-%{srcname}
%{python3_sitelib}/*
%{_bindir}/keycloak-httpd-client-install
%{_bindir}/keycloak-rest
%{_mandir}/man8/*

%changelog
* Mon Aug 19 2024 Tomas Halman <tomas@halman.net> - 1.2-1
  Repository cleanup, preparing for new version
  Spec file is adopted from Fedora.
