%global srcname keycloak-httpd-client
%global summary Tools to configure Apache HTTPD as Keycloak client

Name:           python-%{srcname}
Version:        0.0
Release:        3%{?dist}
Summary:        %{summary}

%global git_tag RELEASE_%(r=%{version}; echo $r | tr '.' '_')

License:        MIT
URL:            http://pypi.python.org/pypi/%{srcname}
Source0:        https://github.com/latchset/python-keycloak/archive/%{git_tag}.tar.gz#/%{srcname}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python3-devel

%description
Keycloak is an authentication server. This package contains libraries and
programs which can invoke the Keycloak REST API and configure clients
of a Keycloak server.

%package -n python2-%{srcname}
Summary:        %{summary}

%{?python_provide:%python_provide python2-%{srcname}}

Requires:       python-requests
Requires:       python-requests-oauthlib
Requires:       python-jinja2

%description -n python2-%{srcname}
Keycloak is an authentication server. This package contains libraries and
programs which can invoke the Keycloak REST API and configure clients
of a Keycloak server.

%package -n python3-%{srcname}
Summary:        %{summary}

%{?python_provide:%python_provide python3-%{srcname}}

Requires:       python3-requests
Requires:       python3-requests-oauthlib
Requires:       python3-jinja2

%description -n python3-%{srcname}
Keycloak is an authentication server. This package contains libraries and
programs which can invoke the Keycloak REST API and configure clients
of a Keycloak server.

%prep
%autosetup -n %{srcname}-%{version}

%build
%py2_build
%py3_build

%install
# Must do the python2 install first because the scripts in /usr/bin are
# overwritten with every setup.py install, and in general we want the
# python3 version to be the default.
%py2_install
%py3_install

# Note that there is no %%files section for the unversioned python module if we are building for several python runtimes
%files -n python2-%{srcname}
%license LICENSE.txt
%doc README.md
%doc doc/keycloak-httpd-client-install.md
%{python2_sitelib}/*
%{_bindir}/*
%{_datadir}/python-%{srcname}/*

%files -n python3-%{srcname}
%license LICENSE.txt
%doc README.md
%doc doc/keycloak-httpd-client-install.md
%{python3_sitelib}/*
%{_bindir}/*
%{_datadir}/python-%{srcname}/*

%changelog
