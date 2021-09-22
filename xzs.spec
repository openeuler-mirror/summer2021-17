%define __jar_repack %{nil}

%global debug_package %{nil}

Name:           xzs
Version:        3.3.0
Release:        2
Summary:        The xzs is an examination system 
License:        AGPL-3.0
URL:            https://github.com/mindskip
Source0:        %{name}-mysql-t%{version}.tar.gz

BuildRequires:  java-1.8.0-openjdk-devel maven nodejs
Requires:       java-1.8.0-openjdk mysql redis

%description
The open source examination system of Xuezhisi is a java + vue examination system with separated front and back ends. The main advantages are simple and quick development and deployment, friendly interface design, and clear code structure. It supports web and WeChat applets, and can cover PCs and mobile phones and other devices. Support multiple deployment methods: integrated deployment, front-end and back-end separate deployment, docker deployment

%prep
%autosetup -p1 -n %{name}-mysql-t%{version}
%build
# 前端admin编译
npm config set sass_binary_site https://npm.taobao.org/mirrors/node-sass/
pushd source/vue/xzs-admin/
npm install --registry https://registry.npm.taobao.org  
npm run build
popd
# 前端student编译
pushd source/vue/xzs-student/
npm install --registry https://registry.npm.taobao.org  
npm run build
popd
# 后端编译
# 源码版本号错误
sed -i 's/3.2.0/3.3.0/' source/xzs/pom.xml
# 使用源码编译的前端
rm -rf source/xzs/src/main/resources/static
cp -a source/vue/xzs-admin/admin source/xzs/src/main/resources/static/ 
cp -a source/vue/xzs-student/student source/xzs/src/main/resources/static/ 
pushd source/xzs
mvn package -Dmaven.repo.remote=http://maven.aliyun.com/nexus/content/groups/public/
popd

%install
mkdir -p %{buildroot}/%{_datarootdir}/xzs
cp -rf source/xzs/target/xzs-%{version}.jar %{buildroot}/%{_datarootdir}/xzs/


%files
%{_datarootdir}/xzs/
%license LICENSE

%changelog
* Wed Sep 22 2021 SnorKeling <1870104920@qq.com> - 3.3.0-2
- Update source0
- optimization spec

* Thu Aug 05 2021 SnorKeling <1870104920@qq.com> - 3.3.0-1
- xzs to rpm
