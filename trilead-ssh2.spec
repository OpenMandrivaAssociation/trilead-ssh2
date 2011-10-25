Name:           trilead-ssh2
Version:        213
Release:        %mkrel 9
Summary:        SSH-2 protocol implementation in pure Java

Group:          Development/Java
License:        BSD
URL:            http://www.trilead.com/Products/Trilead_SSH_for_Java/
# Not working anymore...
#http://www.trilead.com/DesktopModules/Releases/download_file.aspx?ReleaseId=4102
Source0:        trilead-ssh2-build%{version}.zip
Source1:        build.xml
Source2:        http://mirrors.ibiblio.org/pub/mirrors/maven2/org/tmatesoft/svnkit/%{name}/build%{version}-svnkit-1.3-patch/%{name}-build%{version}-svnkit-1.3-patch.pom

BuildRequires:  jpackage-utils
BuildRequires:  java-devel
BuildRequires:  ant
Requires:       jpackage-utils
Requires:       java
Requires(post):   jpackage-utils
Requires(postun): jpackage-utils

BuildArch:      noarch

#Obsoletes:              ganymed-ssh2 <= 210


%description
Trilead SSH-2 for Java is a library which implements the SSH-2 protocol in pure
Java (tested on J2SE 1.4.2 and 5.0). It allows one to connect to SSH servers
from within Java programs. It supports SSH sessions (remote command execution
and shell access), local and remote port forwarding, local stream forwarding,
X11 forwarding and SCP. There are no dependencies on any JCE provider, as all
crypto functionality is included.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java 
Requires:       %{name} = %{version}-%{release}
Requires:       jpackage-utils

%description javadoc
API documentation for trilead-ssh2.

%prep
%setup -q -n %{name}-build%{version}
cp %{SOURCE1} .

# change file encoding
iconv -f ISO-8859-1 -t UTF-8 -o HISTORY.txt HISTORY.txt

# delete the jars that are in the archive
rm %{name}-build%{version}.jar

# fixing wrong-file-end-of-line-encoding warnings
sed -i 's/\r//' LICENSE.txt README.txt HISTORY.txt faq/FAQ.html
find examples -name \*.java -exec sed -i 's/\r//' {} \;

%build
ant


%install
# jar
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -m 644 %{name}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

# pom
mkdir -p %{buildroot}%{_mavenpomdir}
cp %{SOURCE2} %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom
%add_to_maven_depmap org.tmatesoft.svnkit %{name} %{version} JPP %{name}

# javadoc
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pr javadoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%post
%update_maven_depmap

%postun
%update_maven_depmap


%files
%defattr(-,root,root,-)
%{_mavenpomdir}/JPP-%{name}.pom
%{_mavendepmapfragdir}/%{name}
%{_javadir}/*
%doc LICENSE.txt HISTORY.txt README.txt faq examples


%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/%{name}


