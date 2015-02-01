%define nopam 1
%define mktemp_version 1.7

Summary: The GNU core utilities: a set of tools commonly used in shell scripts
Name:    coreutils
Version: 6.9
Release: 10
License: GPLv2+
Epoch: 1
Group:   System Environment/Base
Url:     http://www.gnu.org/software/coreutils/
Source0: ftp://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.bz2
Source1:  mktemp-%{mktemp_version}.tar.gz
Source101:  coreutils-DIR_COLORS
Source102:  coreutils-DIR_COLORS.xterm
Source105:  coreutils-colorls.sh
Source106:  coreutils-colorls.csh
Source200:  coreutils-su.pamd
Source202:  coreutils-su-l.pamd

# From upstream
Patch1: coreutils-futimens.patch
Patch2: coreutils-ls-x.patch
Patch3: coreutils-6.9-cp-i-u.patch

# Our patches
Patch100: coreutils-chgrp.patch

# sh-utils
Patch703: sh-utils-2.0.11-dateman.patch
Patch704: sh-utils-1.16-paths.patch
# RMS will never accept the PAM patch because it removes his historical
# rant about Twenex and the wheel group, so we'll continue to maintain
# it here indefinitely.
Patch706: coreutils-pam.patch
Patch713: coreutils-4.5.3-langinfo.patch
Patch715: coreutils-4.5.3-sysinfo.patch

# (sb) lin18nux/lsb compliance
Patch800: coreutils-i18n.patch

Patch900: coreutils-setsid.patch
Patch907: coreutils-5.2.1-runuser.patch
Patch908: coreutils-getgrouplist.patch
Patch912: coreutils-overflow.patch
Patch915: coreutils-split-pam.patch
Patch916: coreutils-getfacl-exit-code.patch

Patch1001: mktemp-%{mktemp_version}-build.patch

BuildRequires: libacl-devel
BuildRequires: bison
BuildRequires: autoconf >= 2.58
BuildRequires: automake >= 1.10
%{?!nopam:BuildRequires: pam-devel}

%{?!nopam:Requires: pam >= 0.66-12}

Provides: mktemp

%description
These are the GNU core utilities.  This package is the combination of
the old GNU fileutils, sh-utils, and textutils packages.

%prep
%setup -q -b 1

# From upstream
%patch1 -p1 -b .futimens
%patch2 -p1 -b .ls-x
%patch3 -p1 -b .cp-i-u

# Our patches
%patch100 -p1 -b .chgrp

# sh-utils
%patch703 -p1 -b .dateman
%patch704 -p1 -b .paths
%{?!nopam:%patch706 -p1 -b .pam}
%patch713 -p1 -b .langinfo
%patch715 -p1 -b .sysinfo

# li18nux/lsb
%patch800 -p1 -b .i18n

# Coreutils
#%patch900 -p1 -b .setsid
#%patch907 -p1 -b .runuser
%patch908 -p1 -b .getgrouplist
%patch912 -p1 -b .overflow
#%patch915 -p1 -b .splitl
%patch916 -p1 -b .getfacl-exit-code

sed -i -e 's/basic-1//g' tests/stty/Makefile*

chmod a+x tests/sort/sort-mb-tests
chmod a+x tests/ls/x-option

%build
pushd ../mktemp-%{mktemp_version}
patch -p1 < %{PATCH1001}
%configure
make %{?_smp_mflags}
popd

%ifarch s390 s390x
# Build at -O1 for the moment (bug #196369).
export CFLAGS="$RPM_OPT_FLAGS -fPIC -O1"
%else
export CFLAGS="$RPM_OPT_FLAGS -fpic"
%endif
%{expand:%%global optflags %{optflags} -D_GNU_SOURCE=1}
%configure %{?!nopam:--enable-pam} \
            --disable-nls \
           DEFAULT_POSIX2_VERSION=200112 alternative=199209 || :
make %{?_smp_mflags} all \
         %{?!nopam:CPPFLAGS="-DUSE_PAM"} \
         su_LDFLAGS="-pie %{?!nopam:-lpam -lpam_misc}"

# XXX docs should say /var/run/[uw]tmp not /etc/[uw]tmp
sed -i -e 's,/etc/utmp,/var/run/utmp,g;s,/etc/wtmp,/var/run/wtmp,g' doc/coreutils.texi


%install
rm -rf $RPM_BUILD_ROOT

pushd ../mktemp-%{mktemp_version}
make bindir=$RPM_BUILD_ROOT/bin mandir=$RPM_BUILD_ROOT/usr/share/man install 
popd



make DESTDIR=$RPM_BUILD_ROOT install

# man pages are not installed with make install
make mandir=$RPM_BUILD_ROOT%{_mandir} install-man

# fix japanese catalog file
if [ -d $RPM_BUILD_ROOT%{_datadir}/locale/ja_JP.EUC/LC_MESSAGES ]; then
   mkdir -p $RPM_BUILD_ROOT%{_datadir}/locale/ja/LC_MESSAGES
   mv $RPM_BUILD_ROOT%{_datadir}/locale/ja_JP.EUC/LC_MESSAGES/*mo \
      $RPM_BUILD_ROOT%{_datadir}/locale/ja/LC_MESSAGES
   rm -rf $RPM_BUILD_ROOT%{_datadir}/locale/ja_JP.EUC
fi

bzip2 -9f ChangeLog

# let be compatible with old fileutils, sh-utils and textutils packages :
mkdir -p $RPM_BUILD_ROOT{/bin,%_bindir,%_sbindir,/sbin}
%{?!nopam:mkdir -p $RPM_BUILD_ROOT%_sysconfdir/pam.d}
for f in basename cat chgrp chmod chown cp cut date dd df echo env false link ln ls mkdir mknod mv nice pwd rm rmdir sleep sort stty sync touch true uname unlink
do
    mv $RPM_BUILD_ROOT{%_bindir,/bin}/$f 
done

# chroot was in /usr/sbin :
mv $RPM_BUILD_ROOT{%_bindir,%_sbindir}/chroot
# {cat,sort,cut} were previously moved from bin to /usr/bin and linked into 
for i in env cut; do ln -sf ../../bin/$i $RPM_BUILD_ROOT/usr/bin; done

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/profile.d
install -p -c -m644 %SOURCE101 $RPM_BUILD_ROOT%{_sysconfdir}/DIR_COLORS
install -p -c -m644 %SOURCE102 $RPM_BUILD_ROOT%{_sysconfdir}/DIR_COLORS.xterm
install -p -c -m644 %SOURCE105 $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/colorls.sh
install -p -c -m644 %SOURCE106 $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/colorls.csh

# su
install -m 4755 src/su $RPM_BUILD_ROOT/bin
#install -m 755 src/runuser $RPM_BUILD_ROOT/sbin

# These come from util-linux and/or procps.
for i in hostname uptime kill ; do
    rm $RPM_BUILD_ROOT{%_bindir/$i,%_mandir/man1/$i.1}
done

%{?!nopam:install -p -m 644 %SOURCE200 $RPM_BUILD_ROOT%_sysconfdir/pam.d/su}
%{?!nopam:install -p -m 644 %SOURCE202 $RPM_BUILD_ROOT%_sysconfdir/pam.d/su-l}
#%{?!nopam:install -p -m 644 %SOURCE201 $RPM_BUILD_ROOT%_sysconfdir/pam.d/runuser}
#%{?!nopam:install -p -m 644 %SOURCE203 $RPM_BUILD_ROOT%_sysconfdir/pam.d/runuser-l}

# Compress ChangeLogs from before the fileutils/textutils/etc merge
bzip2 -f9 old/*/C*

# Use hard links instead of symbolic links for LC_TIME files (bug #246729).
find %{buildroot}%{_datadir}/locale -type l | \
(while read link
 do
   target=$(readlink "$link")
   rm -f "$link"
   ln "$(dirname "$link")/$target" "$link"
 done)


# (sb) Deal with Installed (but unpackaged) file(s) found
rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%clean
rm -rf $RPM_BUILD_ROOT


%docs_package



%files 
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/DIR_COLORS*
%{_sysconfdir}/profile.d/*
%{?!nopam:%config(noreplace) %{_sysconfdir}/pam.d/su}
%{?!nopam:%config(noreplace) %{_sysconfdir}/pam.d/su-l}
%doc COPYING 
/bin/basename
/bin/cat
/bin/chgrp
/bin/chmod
/bin/chown
/bin/cp
/bin/cut
/bin/date
/bin/dd
/bin/df
/bin/echo
/bin/env
/bin/false
/bin/link
/bin/ln
/bin/ls
/bin/mkdir
/bin/mknod
/bin/mv
/bin/nice
/bin/pwd
/bin/rm
/bin/rmdir
/bin/sleep
/bin/sort
/bin/stty
%attr(4755,root,root) /bin/su
/bin/sync
/bin/touch
/bin/true
/bin/uname
/bin/unlink
/bin/mktemp
%_bindir/*
%_sbindir/chroot
#/sbin/runuser

