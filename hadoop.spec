Name:             hadoop
Version:          0.20.0
Release:          1
Summary:          Distributed filesystem and task tracker
Group:            System Environment/Daemons
URL:              http://hadoop.apache.org/
Vendor:           Apache Software Foundation
Packager:         Rogerio Carvalho Schneider <stockrt@gmail.com>
License:          ASL 2.0
BuildArch:        noarch
Source0:          %{name}-%{version}.tar.gz
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires(pre):    shadow-utils
Requires:         jdk

# Preparing:
#wget http://linorg.usp.br/apache/hadoop/core/hadoop-0.20.0/hadoop-0.20.0.tar.gz
#cp hadoop-0.20.0.tar.gz ~/rpmbuild/SOURCES/

%description
Distributed filesystem (HDFS) and task tracker.

%prep
%setup -q

%build
# Patch a few defaults into hadoop-env.sh
# VER
sed -i -e 's|.*HADOOP_CLASSPATH=.*|HADOOP_CLASSPATH=$HADOOP_CONF_DIR:$(build-classpath hadoop)|' \
       -e 's|# export HADOOP_PID_DIR=.*|export HADOOP_PID_DIR=/var/run/hadoop|' \
       -e 's|# export JAVA_HOME=.*|export JAVA_HOME=/usr/java/latest|' \
       conf/hadoop-env.sh

%install
rm -rf %{buildroot}
install -m 0755 -d %{buildroot}%{_prefix}/local/%{name}
for D in $(find . -mindepth 1 -maxdepth 1 -type d | cut -c 3- | egrep -vw 'build|contrib|docs|src')
do
	cp -a $D %{buildroot}%{_prefix}/local/%{name}/
done
install -m 0644 *.jar %{buildroot}%{_prefix}/local/%{name}/
install -m 0755 -d %{buildroot}%{_var}/run/hadoop
install -m 0755 -d %{buildroot}%{_var}/log/hadoop

# Packing list
(	cd %{buildroot}
	echo '%defattr(-,root,root,-)'
	echo '%attr(0755,hadoop,hadoop) %{_var}/run/hadoop'
	echo '%attr(0755,hadoop,hadoop) %{_var}/log/hadoop'
	find %{buildroot}%{_prefix}/local/%{name} -type d -printf '%%%dir %p\n' | sed -e 's#%{buildroot}##g'
	find %{buildroot}%{_prefix}/local/%{name} -type f -printf '%p\n' | grep -v 'conf/' | sed -e 's#%{buildroot}##g'
	find %{buildroot}%{_prefix}/local/%{name}/conf -type f -printf '%%%config(noreplace) %p\n' | sed -e 's#%{buildroot}##g'
) > filelist

%clean
rm -rf %{buildroot}

%pre
getent group hadoop >/dev/null || groupadd -r hadoop
getent passwd hadoop >/dev/null || \
       useradd -m -r -g hadoop -c "HDFS runtime user" \
       -s /bin/bash hadoop
exit 0

%check

%post

%preun

%files -f filelist

%changelog
* Mon Jun  8 2009 - Rogerio Carvalho Schneider <stockrt@gmail.com> - 0.20.0-1
- Initial version for Hadoop-0.20.0 release
