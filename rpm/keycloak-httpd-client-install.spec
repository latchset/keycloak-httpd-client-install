%global srcname keycloak-httpd-client-install
%global summary Tools to configure Apache HTTPD as Keycloak client

%if 0%{?fedora}
%global with_python3 1
%endif

Name:           %{srcname}
Version:        1.2
Release:        0%{?dist}
Summary:        %{summary}

%global git_tag RELEASE_%(r=%{version}; echo $r | tr '.' '_')

License:        GPLv3
URL:            http://pypi.python.org/pypi/%{srcname}
Source0:        https://github.com/latchset/python-keycloak/archive/%{git_tag}.tar.gz#/%{srcname}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python2-devel
%if 0%{?with_python3}
BuildRequires:  python3-devel
%endif

Requires:       %{_bindir}/keycloak-httpd-client-install

%description
Keycloak is a federated Identity Provider (IdP). Apache HTTPD supports
a variety of authentication modules which can be configured to utilize
a Keycloak IdP to perform authentication. This package contains
libraries and tools which can automate and simplify configuring an
Apache HTTPD authentication module and registering as a client of a
Keycloak IdP.

%package -n python2-%{srcname}
Summary:        %{summary}

%{?python_provide:%python_provide python2-%{srcname}}

Requires:       %{name} = %{version}-%{release}
Requires:       python-requests
Requires:       python-requests-oauthlib
Requires:       python-jinja2
Requires:       %{_bindir}/keycloak-httpd-client-install

%description -n python2-%{srcname}
Keycloak is an authentication server. This package contains libraries and
programs which can invoke the Keycloak REST API and configure clients
of a Keycloak server.

%if 0%{?with_python3}
%package -n python3-%{srcname}
Summary:        %{summary}

%{?python_provide:%python_provide python3-%{srcname}}

Requires:       %{name} = %{version}-%{release}
Requires:       python3-requests
Requires:       python3-requests-oauthlib
Requires:       python3-jinja2

%description -n python3-%{srcname}
Keycloak is an authentication server. This package contains libraries and
programs which can invoke the Keycloak REST API and configure clients
of a Keycloak server.

%endif

%prep
%autosetup -n %{srcname}-%{version}

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

%install
# Must do the python2 install first because the scripts in /usr/bin are
# overwritten with every setup.py install, and in general we want the
# python3 version to be the default.
%py2_install
%if 0%{?with_python3}
# py3_install won't overwrite files if they have a timestamp greater-than
# or equal to the py2 installed files. If both the py2 and py3 builds execute
# quickly the files end up with the same timestamps thus leaving the py2
# version in the py3 install. Therefore remove any files susceptible to this.
rm %{buildroot}%{_bindir}/keycloak-httpd-client-install
%py3_install
%endif

install -d -m 755 %{buildroot}/%{_mandir}/man8
install -c -m 644 doc/keycloak-httpd-client-install.8 %{buildroot}/%{_mandir}/man8

%files
%license LICENSE.txt
%doc README.md doc/ChangeLog
%{_datadir}/%{srcname}/

# Note that there is no %%files section for the unversioned python module if we are building for several python runtimes
%files -n python2-%{srcname}
%{python2_sitelib}/*
%if ! 0%{?with_python3}
%{_bindir}/keycloak-httpd-client-install
%{_bindir}/keycloak-rest
%{_mandir}/man8/*
%endif

%if 0%{?with_python3}
%files -n python3-%{srcname}
%{python3_sitelib}/*
%{_bindir}/keycloak-httpd-client-install
%{_bindir}/keycloak-rest
%{_mandir}/man8/*
%endif

%changelog

* Mon Nov 18 2019 Jakub Hrozek <jhrozek@redhat.com> - 1.2
- Prepare for version 1.2 release : Commit 200501f
- Use links to the new upstream : Commit 80851d8
- Merge pull request #1 from jhrozek/py2 : Commit dc23221
- Merge pull request #2 from jhrozek/fix_spec : Commit 5d9b41b
- Fix python2 incompatibility : Commit d60f325
- Fix rpm spec file : Commit 6dd6b7d

* Wed Jul 03 2019 John Dennis <jdennis@redhat.com> - 1.1
- Prepare for version 1.1 release : Commit 8aed72e
- Add --version option to display version : Commit 4ecf96a
- Merge pull request #10 from jhrozek/logout-uri : Commit 0194770
- Add a new --oidc-logout-uri command line option : Commit 1428515
- Merge pull request #9 from jhrozek/man : Commit 77d7bf1
- doc: Fix a typo in --oidc-redirect-uri description : Commit d4b7037

* Fri Jun 14 2019 John Dennis <jdennis@redhat.com> - 1.0
- Make mellon be the default for --client-type : Commit 826eac4
- Add warning in man page about client-type defaulting to openidc : Commit af56341
- Merge pull request #7 from jhrozek/deprecated_opts : Commit 266ed07
- Let the deprecated options set the same option variables as the new options : Commit 4ddefdc
- Do not directly require --protected-locatins, check if the arg is set instead : Commit 7780025
- update ChangeLog to include OIDC work : Commit cb3ee6f
- add mod_auth_openidc to README.md : Commit 471acc2
- Remove stages option : Commit 4c9eef6
- Man page edits, rename descriptor originate method : Commit dd689e9
- First cut at updating man page to include mod_auth_openidc changes : Commit 7a1f14a
- Change default OIDC clientid to {client_hostname}-{app_name} : Commit 655ef93
- Rename command line tool keycloak_cli.py to keycloak-rest : Commit 16b20aa
- A few ValueErrors should have been ConfigurationErrors : Commit 4eae263
- Unify logging configuration : Commit edd023d
- Introduce module files utils.py and keycloak_rest.py : Commit 9cf2e9a
- Implement OIDC client : Commit 69cb3fd
- Unify command line args between Mellon & OIDC clients : Commit eb8b6f6
- Fix some issues with using --stages : Commit 80c0bc6
- refactor into Client classes : Commit 24210b5
- add stages, e.g. mellon,keycloak : Commit e119883
- clean up some pylint errors : Commit 96adc8f
- initial clean up of REST : Commit 85c2fe6

* Tue Jan 09 2018 John Dennis <jdennis@redhat.com> - 0.8
- Bump version to 0.8 : Commit 671fb01
- CVE-2017-15111 unsafe /tmp log file in --log-file option in keycloak_cli.py : Commit 07f26e2
- CVE-2017-15112 unsafe use of -p/--admin-password on command line : Commit c3121b2
- Fix prior patch, use join_path() instead of concatenation : Commit bee4ab8
- fix spelling typo : Commit dd6139a

* Thu Nov 02 2017 John Dennis <jdennis@redhat.com> - 0.7
- fix rhbz#1481322, mellon-root and mellon-protected-locations need to be validated : Commit ef41c53

* Tue Feb 28 2017 John Dennis <jdennis@redhat.com> - 0.6
- Fix double slashes, add --tls-verify, fix anonymous auth logic : Commit efa2715

* Fri Jan 06 2017 John Dennis <jdennis@redhat.com> - 0.5
- * fix bug with default ports 80 and 443   default ports should not be present in URL * add utility get_entity_id_from_metadata() * add get_server_info() REST query : Commit 6269916
- fix reference to doc : Commit 472e2c6

* Wed Jun  8 2016 John Dennis <jdennis@redhat.com> - 0.4-1
- new upstream
- add methods to add/remove client redirect URI
- add function to parse SP metadata to extract AssertionConsumerServiceURL's
- Add all AssertionConsumerServiceURL's as redirect URI's during
  client registration.

* Fri May 20 2016 John Dennis <jdennis@redhat.com> - 0.3-1
- new upstream
  See ChangeLog for details

* Tue May 17 2016 John Dennis <jdennis@redhat.com> - 0.2-1
- new upstream
- Add keycloak-httpd-client-install.8 man page

* Fri May 13 2016 John Dennis <jdennis@redhat.com> - 0.1-1
- Initial version
