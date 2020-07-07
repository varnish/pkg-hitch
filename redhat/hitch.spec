%global hitch_user	hitch
%global hitch_group	hitch
%global hitch_homedir	%{_localstatedir}/lib/hitch
%global hitch_confdir	%{_sysconfdir}/hitch
%global hitch_datadir	%{_datadir}/hitch

Name:		hitch
Version:	%{versiontag}
Release:	%{releasetag}%{?dist}
Summary:	Client-side SSL terminator for Varnish Plus.

License:	BSD
URL:		https://github.com/varnish/hitch
Source:		%{srcname}.tgz

Provides:	hitch

Prefix: /

BuildRequires:	make
BuildRequires:	libev-devel
BuildRequires:	openssl-devel
BuildRequires:  flex-devel
BuildRequires:  bison-devel
BuildRequires:	systemd-units

Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units

%description
Hitch is a network proxy that terminates TLS/SSL connections and
forwards the unencrypted traffic to some backend. It is designed to
handle tens of thousands of connections efficiently on multicore
machines.


%prep
%setup -q -n %{srcname}

%build
%configure --prefix=%{_prefix}
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

%{__install} -p -D -m 0644 hitch.service %{buildroot}%{_unitdir}/hitch.service
%{__install} -p -D -m 0644 hitch.conf %{buildroot}%{hitch_confdir}/hitch.conf
%{__install} -d -m 0755 %{buildroot}%{hitch_homedir}
%{__install} -d -m 0755 %{buildroot}%{hitch_datadir}


%clean
rm -rf %{buildroot}


%pre
getent group hitch  >/dev/null || groupadd -r %{hitch_group}
getent passwd hitch >/dev/null || \
    useradd -r -g %{hitch_group} -s /sbin/nologin -d %{hitch_homedir} %{hitch_user}

%post
%{__install} -p -D -m 0740 -g %{hitch_group} -o %{hitch_user} -d $RPM_INSTALL_PREFIX/var/lib/hitch-ocsp
%systemd_post hitch.service


%preun
%systemd_preun hitch


%postun
%systemd_postun_with_restart hitch


%files
%defattr(-,root,root,-)
%dir %{hitch_confdir}
%dir %{hitch_datadir}
%doc /usr/share/doc/%{name}/
%config(noreplace) %{hitch_confdir}/hitch.conf
%{_unitdir}/hitch.service
%{_sbindir}/hitch
%{_mandir}/man8/hitch.8*
%{_mandir}/man5/*.5*
%attr(-,%{hitch_user},%{hitch_group}) %dir %{hitch_homedir}


%changelog
* Fri May 15 2015 Varnish Software <support@varnish-software.com> - %{versiontag}-%{releasetag}
- This changelog is not in use.
