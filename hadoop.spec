Name:          hadoop
Version:       0.20.0
Release:       1
Summary:       Hadoop Distributed File System and MapReduce implementation
Group:         System Environment/Daemons
URL:           http://hadoop.apache.org/core
Vendor:        Apache Software Foundation
Packager:      Rogério Carvalho Schneider <stockrt@gmail.com>
License:       ASL 2.0
BuildArch:     noarch
Source:        %{name}-%{version}.tar.gz
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id} -un)
Requires(pre): shadow-utils
Requires:      jdk

# Getting:
# mkdir -p ~/rpmbuild/SOURCES
# cd ~/rpmbuild/SOURCES
# wget http://linorg.usp.br/apache/hadoop/core/hadoop-0.20.0/hadoop-0.20.0.tar.gz

# Recommended Topdir
%define _topdir %(echo $HOME)/rpmbuild

# So the build does not fail due to unpackaged files or due to missing doc
# files:
%define _unpackaged_files_terminate_build 0
%define _missing_doc_files_terminate_build 0

# No debug package:
%define debug_package %{nil}

%description
Apache Hadoop Core is a software platform that lets one easily write and run
applications that process vast amounts of data.

Here's what makes Hadoop especially useful:
 * Scalable: Hadoop can reliably store and process petabytes.
 * Economical: It distributes the data and processing across clusters of
   commonly available computers. These clusters can number into the
   thousands of nodes.
 * Efficient: By distributing the data, Hadoop can process it in parallel on
   the nodes where the data is located. This makes it extremely rapid.
 * Reliable: Hadoop automatically maintains multiple copies of data and
   automatically redeploys computing tasks based on failures.

Hadoop implements MapReduce, using the Hadoop Distributed File System (HDFS).
MapReduce divides applications into many small blocks of work. HDFS creates
multiple replicas of data blocks for reliability, placing them on compute
nodes around the cluster. MapReduce can then process the data where it is
located.

%prep
%setup -q

%build
# hadoop-env.sh defaults
%{__sed} -i -e 's|.*JAVA_HOME=.*|export JAVA_HOME=/usr/java/latest|' \
         -e 's|.*HADOOP_CLASSPATH=.*|export HADOOP_CLASSPATH=$HADOOP_CONF_DIR:$(build-classpath hadoop)|' \
         -e 's|.*HADOOP_LOG_DIR=.*|export HADOOP_LOG_DIR=%{_var}/log/hadoop|' \
         -e 's|.*HADOOP_PID_DIR=.*|export HADOOP_PID_DIR=%{_var}/run/hadoop|' \
         conf/hadoop-env.sh

%install
%{__rm} -rf %{buildroot}
%{__install} -m 0755 -d %{buildroot}%{_prefix}/local/%{name}
for D in $(find . -mindepth 1 -maxdepth 1 -type d | cut -c 3- | %{__grep} -Evw 'build|docs|src')
do
	%{__cp} -a $D %{buildroot}%{_prefix}/local/%{name}/
done
%{__install} -m 0644 *.jar %{buildroot}%{_prefix}/local/%{name}/
%{__install} -m 0644 *.txt %{buildroot}%{_prefix}/local/%{name}/
%{__install} -m 0644 *.xml %{buildroot}%{_prefix}/local/%{name}/
%{__install} -m 0755 -d %{buildroot}%{_var}/run/hadoop
%{__install} -m 0755 -d %{buildroot}%{_var}/log/hadoop

# Packing list
(	cd %{buildroot}
	echo '%defattr(-,root,root,-)'
	echo '%attr(0755,hadoop,hadoop) %{_var}/run/hadoop'
	echo '%attr(0755,hadoop,hadoop) %{_var}/log/hadoop'
	find %{buildroot}%{_prefix}/local/%{name} -type d -printf '%%%dir %p\n' | %{__sed} -e 's|%{buildroot}||g'
	find %{buildroot}%{_prefix}/local/%{name} -type f -printf '%p\n' | %{__grep} -v 'conf/' | %{__sed} -e 's|%{buildroot}||g'
	find %{buildroot}%{_prefix}/local/%{name}/conf -type f -printf '%%%config(noreplace) %p\n' | %{__sed} -e 's|%{buildroot}||g'
) > filelist

%clean
%{__rm} -rf %{buildroot}

%pre
getent group hadoop >/dev/null || \
	groupadd -r hadoop
getent passwd hadoop >/dev/null || \
	useradd -m -r -g hadoop -c 'HDFS runtime user' -s /bin/bash hadoop
exit 0

%check

%post

%preun

%files -f filelist

%changelog
* Mon Jun  8 2009 - Rogério Carvalho Schneider <stockrt@gmail.com> - 0.20.0-1
- Initial packing for Hadoop-0.20.0 release
