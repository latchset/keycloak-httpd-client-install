%global srcname keycloak-httpd-client-install
%global summary Tools to configure Apache HTTPD as Keycloak client

Name:           %{srcname}
Version:        1.3
Release:        %{?release_string}%{!?release_string: 1}%{?dist}
Summary:        %{summary}


License:        GPL-3.0-or-later
URL:            https://github.com/lachset/keycloak-httpd-client-install
Source0:        https://github.com/lachset/keycloak-httpd-client-install/releases/download/%{version}/keycloak-httpd-client-install-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  (python3-setuptools if python3-devel >= 3.12)
# runtime deps for import check
BuildRequires:  python3-requests
BuildRequires:  python3-requests-oauthlib
BuildRequires:  python3-jinja2
BuildRequires:  python3-lxml

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

%{?python_provide:%python_provide python3-%{srcname}}

Requires:       %{name} = %{version}-%{release}
Requires:       python3-requests
Requires:       python3-requests-oauthlib
Requires:       python3-jinja2
Requires:       python3-lxml

%description -n python3-%{srcname}
Keycloak is an authentication server. This package contains libraries and
programs which can invoke the Keycloak REST API and configure clients
of a Keycloak server.

%prep
%autosetup -n %{srcname}-%{version} -p1

%build
%py3_build

%install
%py3_install

install -d -m 755 %{buildroot}/%{_mandir}/man8
install -c -m 644 doc/keycloak-httpd-client-install.8 %{buildroot}/%{_mandir}/man8

%check
%py3_check_import keycloak_httpd_client

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
