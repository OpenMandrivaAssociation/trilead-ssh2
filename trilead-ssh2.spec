Name:           trilead-ssh2
Version:        213
Release:        %mkrel 2.0.1
Epoch:          0
Summary:        SSH-2 protocol implementation in pure Java
Group:          Development/Java
License:        BSD
URL:            http://www.trilead.com/Products/Trilead-SSH-2-Java/
Source0:        %{name}-build%{version}.zip
Source1:	build.xml
BuildRequires:  java-rpmbuild >= 0:1.6
BuildRequires:  ant
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
Ganymed SSH-2 for Java is a library which implements the SSH-2 protocol in pure
Java (tested on J2SE 1.4.2 and 5.0). It allows one to connect to SSH servers
from within Java programs. It supports SSH sessions (remote command execution
and shell access), local and remote port forwarding, local stream forwarding,
X11 forwarding and SCP. There are no dependencies on any JCE provider, as all
crypto functionality is included.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -n %{name}-build%{version}
%{__cp} %{SOURCE1} build.xml
%remove_java_binaries

# fixing wrong-file-end-of-line-encoding warnings
%{__sed} -i 's/\r$//g' LICENSE.txt README.txt HISTORY.txt faq/FAQ.html
%{_bindir}/find examples -name \*.java | %{_bindir}/xargs -t %{__sed} -i 's/\r$//g'

%build
%ant

%install
%{__rm} -rf %{buildroot}

# jar
%{__mkdir_p} %{buildroot}%{_javadir}
%{__cp} -a dist/lib/%{name}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar

# javadoc
%{__mkdir_p} %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__cp} -a javadoc/* \
  %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__ln_s} %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}

%create_jar_links

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(0644,root,root,0755)
%doc LICENSE.txt HISTORY.txt README.txt faq examples
%{_javadir}/*

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}

