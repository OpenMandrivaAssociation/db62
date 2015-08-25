%define sname	db
%define version 6.1.26
%define api %(echo %{version}|cut -d. -f1,2)
%define shortapi %(echo %{version}|cut -d. -f1,1)
%define binext	%(echo %{api} | sed -e 's|\\.||g')

%define libname		%mklibname %{sname} %{api}
%define devname		%mklibname %{sname} %{api} -d
%define statname	%mklibname %{sname} %{api} -s -d

%define libdbcxx	%mklibname %{sname}cxx %{api}
%define libdbsql	%mklibname %{sname}sql %{api}
%define libdbtcl	%mklibname %{sname}tcl %{api}
%define libdbjava	%mklibname %{sname}java %{api}

%define libdbnss	%mklibname %{sname}nss %{api}
%define devdbnss	%mklibname %{sname}nss %{api} -d

%ifnarch %[mips} %{arm} aarch64
%bcond_with java
%define gcj_support 0
%endif

%bcond_without sql
%bcond_with tcl
%bcond_without db1
# Define to build a stripped down version to use for nss libraries
%bcond_with	 nss

# Define to rename utilities and allow parallel installation
%bcond_without parallel

# mutexes defaults to POSIX/pthreads/library
%bcond_with asmmutex

Summary:	The Berkeley DB database library for C
Name:		%{sname}%{binext}
Version:	6.1.26
Release:	2
License:	BSD
Group:		System/Libraries
Url:		http://www.oracle.com/technology/software/products/berkeley-db/
Source0:	http://download.oracle.com/berkeley-db/db-%{version}.tar.gz
# statically link db1 library
Patch0:		db-5.1.19-db185.patch
Patch1:		db-5.1.25-sql_flags.patch
Patch2:		db-5.1.19-tcl-link.patch
Patch3:		arm-thumb-mutex_db5.patch
# fedora patches
Patch101:	db-4.7.25-jni-include-dir.patch
# ubuntu patches
Patch102:	006-mutex_alignment.patch

BuildRequires:	ed
BuildRequires:	libtool
%if %{with sql}
BuildRequires:	pkgconfig(sqlite3)
%endif
%if %{with tcl}
BuildRequires:	pkgconfig(tcl)
%endif
%if %{with db1}
BuildRequires:	db1-devel
%endif
%if %{with java}
BuildRequires:	java-rpmbuild
BuildRequires:	java-devel
BuildRequires:	sharutils
# required for jni.h
BuildRequires:	gcj-devel
#(proyvind): try workaround issue preventng build
BuildRequires:	gcc-java
%if %{gcj_support}
BuildRequires:	java-gcj-compat-devel
%endif
%endif

%description
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
Berkeley DB is used by many applications, including Python and Perl, so this
should be installed on all systems.

%package -n	%{libname}
Summary:	The Berkeley DB database library for C
Group:		System/Libraries

%description -n	%{libname}
This package contains the shared library required by Berkeley DB.

%package -n	%{libdbcxx}
Summary:	The Berkeley DB database library for C++
Group:		System/Libraries

%description -n	%{libdbcxx}
This package contains the files needed to build C++ programs which use
Berkeley DB.

%if %{with sql}
%package -n	%{libdbsql}
Summary:	The Berkeley DB database library for SQL
Group:		System/Libraries

%description -n	%{libdbsql}
This package contains the files needed to build SQL programs which use
Berkeley DB.
%endif

%if %{with java}
%package -n	%{libdbjava}
Summary:	The Berkeley DB database library for C++
Group:		System/Libraries

%description -n	%{libdbjava}
This package contains the files needed to build Java programs which use
Berkeley DB.

%package -n	%{libdbjava}-javadoc
Summary:	Javadoc for %{name}
Group:		Development/Java

%description -n %{libdbjava}-javadoc
Javadoc for %{name}.
%endif

%if %{with tcl}
%package -n	%{libdbtcl}
Summary:	The Berkeley DB database library for TCL
Group:		System/Libraries

%description -n	%{libdbtcl}
This package contains the header files, libraries, and documentation for
building tcl programs which use Berkeley DB.
%endif

%package utils
Summary:	Command line tools for managing Berkeley DB databases
Group:		Databases
%if !%{with parallel}
Conflicts:	db-utils < %{api}
%endif
Requires:	%{name}_recover = %{EVRD}

%description	utils
This package contains command line tools for managing Berkeley DB databases.

%package -n	%{name}_recover
Summary:	Minimal package with '%{name}_recover' only
Group:		Databases

%description -n	%{name}_recover
This is a minimal package that ships with '%{name}_recover' only as it's
required for using "RPM ACID".

%package -n	%{devname}
Summary:	Development libraries/header files for the Berkeley DB library
Group:		Development/Databases
Requires:	%{libname} = %{EVRD}
%if %{with sql}
Requires:	%{libdbsql} = %{EVRD}
%endif
%if %{with tcl}
Requires:	%{libdbtcl} = %{EVRD}
%endif
%if %{with java}
Requires:	%{libdbjava} = %{EVRD}
%endif
Requires:	%{libdbcxx} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}
Provides:	%{sname}-devel = %{EVRD}
# MD remove the following line if there is a newer fork of the same api
# ie: this is 6.0 and there is a fork of 6.1 or 6.2....
Provides:	%{sname}%{shortapi}-devel = %{EVRD}

%description -n	%{devname}
This package contains the header files, libraries, and documentation for
building programs which use Berkeley DB.

%package -n	%{statname}
Summary:	Development static libraries files for the Berkeley DB library
Group:		Development/Databases
Requires:	%{devname} = %{EVRD}
Provides:	%{name}-static-devel = %{EVRD}

%description -n	%{statname}
This package contains the static libraries for building programs which
use Berkeley DB.

%if %{with nss}
%package -n	%{libdbnss}
Summary:	The Berkeley DB database library for NSS modules
Group:		System/Libraries

%description -n	%{libdbnss}
This package contains the shared library required by some nss modules
that use Berkeley DB.

%package -n	%{devdbnss}
Summary:	Development libraries/header files for building nss modules with Berkeley DB
Group:		Development/Databases
Requires:	%{libdbnss} = %{EVRD}
Provides:	dbnss%{binext}-devel = %{EVRD}
Provides:	db_nss%{binext}-devel = %{EVRD}

%description -n	%{devdbnss}
This package contains the header files and libraries for building nss
modules which use Berkeley DB.
%endif

%prep
%setup -qn %{sname}-%{version}
# fix strange attribs
find . -type f -perm 0444 -exec chmod 644 {} \;
rm -r lang/sql/jdbc/doc
%apply_patches

# copy modern config.* files to target
for f in config.guess config.sub ; do
        test -f /usr/share/libtool/config/$f || continue
        find . -type f -name $f -exec cp /usr/share/libtool/config/$f \{\} \;
done


pushd dist
libtoolize --copy --force
cat %{_datadir}/aclocal/libtool.m4 >> aclocal.m4
popd

# Remove tags files which we don't need.
find . -name tags | xargs rm -f
# Define a shell function for fixing HREF references in the docs, which
# would otherwise break when we split the docs up into subpackages.
fixup_href() {
    for doc in $@ ; do
	chmod u+w ${doc}
	sed -e 's,="../api_c/,="../../%{name}-devel/api_c/,g' \
	    -e 's,="api_c/,="../%{name}-devel/api_c/,g' \
	    -e 's,="../api_cxx/,="../../%{name}-devel/api_cxx/,g' \
	    -e 's,="api_cxx/,="../%{name}-devel/api_cxx/,g' \
	    -e 's,="../api_tcl/,="../../%{name}-devel/api_tcl/,g' \
	    -e 's,="api_tcl/,="../%{name}-devel/api_tcl/,g' \
	    -e 's,="../java/,="../../%{name}-devel/java/,g' \
	    -e 's,="java/,="../%{name}-devel/java/,g' \
	    -e 's,="../examples_c/,="../../%{name}-devel/examples_c/,g' \
	    -e 's,="examples_c/,="../%{name}-devel/examples_c/,g' \
	    -e 's,="../examples_cxx/,="../../%{name}-devel/examples_cxx/,g' \
	    -e 's,="examples_cxx/,="../%{name}-devel/examples_cxx/,g' \
	    -e 's,="../ref/,="../../%{name}-devel/ref/,g' \
	    -e 's,="ref/,="../%{name}-devel/ref/,g' \
	    -e 's,="../images/,="../../%{name}-devel/images/,g' \
	    -e 's,="images/,="../%{name}-devel/images/,g' \
	    -e 's,="../utility/,="../../%{name}-utils/utility/,g' \
	    -e 's,="utility/,="../%{name}-utils/utility/,g' ${doc} > ${doc}.new
	touch -r ${doc} ${doc}.new
	cat ${doc}.new > ${doc}
	touch -r ${doc}.new ${doc}
	rm -f ${doc}.new
    done
}

set +x	# XXX painful to watch
# Fix all of the HTML files.
fixup_href `find . -name "*.html"`
set -x	# XXX painful to watch

cd dist
./s_config

%build
%ifarch ppc
CFLAGS="$CFLAGS -D_GNU_SOURCE -D_REENTRANT"
%endif
export CFLAGS

%global ldflags %{ldflags} -fuse-ld=bfd

%if %{with java}
export CLASSPATH=
export JAVAC=%{javac}
export JAR=%{jar}
export JAVA=%{java}
export JAVACFLAGS="-nowarn"
JAVA_MAKE="JAR=%{jar} JAVAC=%{javac} JAVACFLAGS="-nowarn" JAVA=%{java}"
%endif
pushd build_unix
CONFIGURE_TOP="../dist" \
%configure \
	--includedir=%{_includedir}/%{name} \
	--enable-shared \
	--enable-static \
	--enable-dbm \
	--enable-o_direct \
%if %{with sql}
	--enable-sql \
%endif
%if %{with db1}
	--enable-compat185 \
	--enable-dump185 \
%endif
%if %{with tcl}
	--enable-tcl --with-tcl=%{_libdir} --enable-test \
%endif
	--enable-cxx \
%if %{with java}
	--enable-java \
%endif
%if %{with asmmutex}
%ifarch %{ix86}
	--disable-posixmutexes \
	--with-mutex=x86/gcc-assembly
%endif
%ifarch x86_64
	--disable-posixmutexes \
	--with-mutex=x86_64/gcc-assembly
%endif
%ifarch alpha
	--disable-posixmutexes \
	--with-mutex=ALPHA/gcc-assembly
%endif
%ifarch ia64
	--disable-posixmutexes \
	--with-mutex=ia64/gcc-assembly
%endif
%ifarch ppc
	--disable-posixmutexes \
	--with-mutex=PPC/gcc-assembly
%endif
%ifarch %{sparc}
	--disable-posixmutexes \
	--with-mutex=Sparc/gcc-assembly
%endif
%ifarch %{mips}
	--disable-posixmutexes \
	--with-mutex=MIPS/gcc-assembly
%endif
%ifarch %{arm}
	--disable-posixmutexes \
	--with-mutex=ARM/gcc-assembly
%endif
%else
	--enable-posixmutexes \
	--with-mutex=POSIX/pthreads/library
%endif

%make $JAVA_MAKE
%if %{with java}
pushd ../lang/java
%{javadoc} -d ../sql/jdbc/doc `find . -name '*.java'`
popd
%endif
popd
%if %{with nss}
mkdir build_nss
pushd build_nss
CONFIGURE_TOP="../dist" \
%configure \
	--includedir=%{_includedir}/db_nss \
	--enable-shared \
	--disable-static \
	--enable-dbm \
	--enable-o_direct \
	--disable-tcl \
	--disable-cxx \
	--disable-java \
	--with-uniquename=_nss \
	--enable-compat185 \
	--disable-cryptography \
	--disable-queue \
	--disable-replication \
	--disable-verify \
%if %{with asmmutex}
%ifarch %{ix86}
	--disable-posixmutexes \
	--with-mutex=x86/gcc-assembly
%endif
%ifarch x86_64
	--disable-posixmutexes \
	--with-mutex=x86_64/gcc-assembly
%endif
%ifarch alpha
	--disable-posixmutexes \
	--with-mutex=ALPHA/gcc-assembly
%endif
%ifarch ia64
	--disable-posixmutexes \
	--with-mutex=ia64/gcc-assembly
%endif
%ifarch ppc
	--disable-posixmutexes \
	--with-mutex=PPC/gcc-assembly
%endif
%ifarch %{sparc}
	--disable-posixmutexes \
	--with-mutex=Sparc/gcc-assembly
%endif
%ifarch %{mips}
	--disable-posixmutexes \
	--with-mutex=MIPS/gcc-assembly
%endif
%ifarch %{arm}
	--disable-posixmutexes \
	--with-mutex=ARM/gcc-assembly
%endif
%else
	--enable-posixmutexes \
	--with-mutex=POSIX/pthreads/library
%endif

%make libdb_base=libdb_nss libso_target=libdb_nss-%{api}.la libdir=/%{_lib}
popd
%endif

%install
make -C build_unix install_setup install_include install_lib install_utilities \
	DESTDIR=%{buildroot} emode=755

%if %{with nss}
make -C build_nss install_include install_lib libdb_base=libdb_nss \
	DESTDIR=%{buildroot} LIB_INSTALL_FILE_LIST=""

mkdir -p %{buildroot}/%{_lib}
mv %{buildroot}/%{_libdir}/libdb_nss-%{api}.so %{buildroot}/%{_lib}
ln -s  /%{_lib}/libdb_nss-%{api}.so %{buildroot}%{_libdir}
%endif

ln -sf %{name}/db.h %{buildroot}%{_includedir}/db.h

# XXX This is needed for parallel install with db4.2
%if %{with parallel}
for F in %{buildroot}%{_bindir}/*db_* ; do
	mv $F `echo $F | sed -e 's,db_,%{name}_,'`
done
%endif

# Move db.jar file to the correct place, and version it
%if %{with java}
mkdir -p %{buildroot}%{_jnidir}
mv %{buildroot}%{_libdir}/db.jar %{buildroot}%{_jnidir}/db%{api}-%{version}.jar
(cd %{buildroot}%{_jnidir} && for jar in *-%{version}*; do %{__ln_s} ${jar} ${jar/-%{version}/}; done)

mkdir -p %{buildroot}%{_javadocdir}/db%{api}-%{version}
cp -a lang/sql/jdbc/doc/* %{buildroot}%{_javadocdir}/db%{api}-%{version}
ln -s db%{api}-%{version} %{buildroot}%{_javadocdir}/db%{api}

%if %{gcj_support}
rm -rf aot-compile-rpm
aot-compile-rpm
%endif
%endif

rm -rf %{buildroot}%{_includedir}/db_nss/db_cxx.h

%if %{with sql}
mv %{buildroot}%{_bindir}/{dbsql,db%{api}_sql}
%endif

%if %{with java}
%post -n %{libdbjava}
%{update_gcjdb}

%postun -n %{libdbjava}
%{clean_gcjdb}
%endif

%files -n %{libname}
%doc LICENSE README
%{_libdir}/libdb-%{api}.so

%files -n %{libdbcxx}
%{_libdir}/libdb_cxx-%{api}.so

%if %{with sql}
%files -n %{libdbsql}
%{_libdir}/libdb_sql-%{api}.so
%endif

%if %{with java}
%files -n %{libdbjava}
%doc lang/sql/jdbc/doc/*
%doc examples/java/src
%{_libdir}/libdb_java-%{api}.so
%{_libdir}/libdb_java-%{api}_g.so
%{_jnidir}/db%{api}.jar
%{_jnidir}/db%{api}-%{version}.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%{_libdir}/gcj/%{name}/*
%endif

%files -n %{libdbjava}-javadoc
%doc %{_javadocdir}/db%{api}-%{version}
%doc %dir %{_javadocdir}/db%{api}
%endif

%if %{with tcl}
%files -n %{libdbtcl}
%{_libdir}/libdb_tcl-%{api}.so
%endif

%files utils
%doc docs/api_reference/C/db_archive.html
%doc docs/api_reference/C/db_checkpoint.html
%doc docs/api_reference/C/db_deadlock.html
%doc docs/api_reference/C/db_dump.html
%doc docs/api_reference/C/db_load.html
%doc docs/api_reference/C/db_printlog.html
%doc docs/api_reference/C/db_replicate.html
%doc docs/api_reference/C/db_stat.html
%doc docs/api_reference/C/db_upgrade.html
%doc docs/api_reference/C/db_verify.html
%{_bindir}/%{name}_archive
%{_bindir}/%{name}_checkpoint
%{_bindir}/%{name}_deadlock
%{_bindir}/%{name}_dump*
%{_bindir}/%{name}_hotbackup
%{_bindir}/%{name}_load
%{_bindir}/%{name}_log_verify
%{_bindir}/%{name}_printlog
%{_bindir}/%{name}_replicate
%{_bindir}/%{name}_stat
%{_bindir}/%{name}_tuner
%{_bindir}/%{name}_upgrade
%{_bindir}/%{name}_verify
%if %{with sql}
%doc docs/api_reference/C/dbsql.html
%{_bindir}/db%{api}_sql
%endif

%files -n %{name}_recover
%doc docs/api_reference/C/db_recover.html
%{_bindir}/%{name}_recover

%files -n %{devname}
%doc docs/api_reference
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/db.h
%if %{with db1}
%{_includedir}/%{name}/db_185.h
%endif
%{_includedir}/%{name}/db_cxx.h
%if %{with sql}
%{_includedir}/%{name}/dbsql.h
%endif
%{_includedir}/db.h
%{_libdir}/libdb.so
%{_libdir}/libdb-6.so
%{_libdir}/libdb_cxx.so
%{_libdir}/libdb_cxx-6.so
%if %{with sql}
%{_libdir}/libdb_sql.so
%{_libdir}/libdb_sql-6.so
%endif
%if %{with tcl}
%{_libdir}/libdb_tcl.so
%{_libdir}/libdb_tcl-6.so
%endif
%if %{with java}
%{_libdir}/libdb_java.so
%{_libdir}/libdb_java-6.so
%endif

%files -n %{statname}
%{_libdir}/*.a

%if %{with nss}
%files -n %{libdbnss}
/%{_lib}/libdb_nss-%{api}.so

%files -n %{devdbnss}
%dir %{_includedir}/db_nss
%{_includedir}/db_nss/db.h
%if %{with db1}
%{_includedir}/db_nss/db_185.h
%endif
%{_libdir}/libdb_nss.so
%{_libdir}/libdb_nss-6.so
%{_libdir}/libdb_nss-%{api}.so
%endif

