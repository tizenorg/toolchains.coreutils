%define nopam 1
%define mktemp_version 1.7

Name:           coreutils
Version:        6.9
Release:        9
License:        GPL-2.0+
Summary:        The GNU core utilities: a set of tools commonly used in shell scripts
Url:            http://www.gnu.org/software/coreutils/
Group:          System Environment/Base
Source0:        ftp://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.bz2
Source1:        mktemp-%{mktemp_version}.tar.gz
Source101:      coreutils-DIR_COLORS
Source102:      coreutils-DIR_COLORS.xterm
Source105:      coreutils-colorls.sh
Source106:      coreutils-colorls.csh
Source200:      coreutils-su.pamd
Source202:      coreutils-su-l.pamd
# FIXME
Epoch: 1

# From upstream
Patch1:         coreutils-futimens.patch
Patch2:         coreutils-ls-x.patch
Patch3:         coreutils-6.9-cp-i-u.patch

# Our patches
Patch100:       coreutils-chgrp.patch

# sh-utils
Patch703:       sh-utils-2.0.11-dateman.patch
Patch704:       sh-utils-1.16-paths.patch
# RMS will never accept the PAM patch because it removes his historical
# rant about Twenex and the wheel group, so we'll continue to maintain
# it here indefinitely.
Patch706:       coreutils-pam.patch
Patch713:       coreutils-4.5.3-langinfo.patch
Patch715:       coreutils-4.5.3-sysinfo.patch

# (sb) lin18nux/lsb compliance
Patch800:       coreutils-i18n.patch

Patch900:       coreutils-setsid.patch
Patch907:       coreutils-5.2.1-runuser.patch
Patch908:       coreutils-getgrouplist.patch
Patch912:       coreutils-overflow.patch
Patch915:       coreutils-split-pam.patch
Patch916:       coreutils-getfacl-exit-code.patch

Patch1001:      mktemp-%{mktemp_version}-build.patch

BuildRequires:  autoconf >= 2.58
BuildRequires:  automake >= 1.10
BuildRequires:  bison
BuildRequires:  libacl-devel
%{?!nopam:BuildRequires: pam-devel}

%{?!nopam:Requires: pam >= 0.66-12}

Provides:       mktemp
Provides:       coreutils-su

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
make
popd

export CFLAGS="%{optflags} -fpic"
%{expand:%%global optflags %{optflags} -D_GNU_SOURCE=1}
%configure %{?!nopam:--enable-pam} \
            --disable-nls \
           DEFAULT_POSIX2_VERSION=200112 alternative=199209 || :
make all \
         %{?!nopam:CPPFLAGS="-DUSE_PAM"} \
         su_LDFLAGS="-pie %{?!nopam:-lpam -lpam_misc}"

# XXX docs should say /var/run/[uw]tmp not /etc/[uw]tmp
sed -i -e 's,/etc/utmp,/var/run/utmp,g;s,/etc/wtmp,/var/run/wtmp,g' doc/coreutils.texi


%check
#make check

%install

pushd ../mktemp-%{mktemp_version}
make bindir=%{buildroot}/bin mandir=%{buildroot}%{_mandir} install
popd



%make_install

# man pages are not installed with make install
make mandir=%{buildroot}%{_mandir} install-man

# fix japanese catalog file
if [ -d %{buildroot}%{_datadir}/locale/ja_JP.EUC/LC_MESSAGES ]; then
   mkdir -p %{buildroot}%{_datadir}/locale/ja/LC_MESSAGES
   mv %{buildroot}%{_datadir}/locale/ja_JP.EUC/LC_MESSAGES/*mo \
      %{buildroot}%{_datadir}/locale/ja/LC_MESSAGES
   rm -rf %{buildroot}%{_datadir}/locale/ja_JP.EUC
fi

bzip2 -9f ChangeLog

# let be compatible with old fileutils, sh-utils and textutils packages :
mkdir -p %{buildroot}{/bin,%{_bindir},%{_sbindir},/sbin}
%{?!nopam:mkdir -p %{buildroot}%{_sysconfdir}/pam.d}
for f in basename cat chgrp chmod chown cp cut date dd df echo env false link ln ls mkdir mknod mv nice pwd rm rmdir sleep sort stty sync touch true uname unlink
do
    mv %{buildroot}{%{_bindir},/bin}/$f
done

# chroot was in /usr/sbin :
mv %{buildroot}{%{_bindir},%{_sbindir}}/chroot
# {cat,sort,cut} were previously moved from bin to /usr/bin and linked into
for i in env cut; do ln -sf ../../bin/$i %{buildroot}%{_prefix}/bin; done

mkdir -p %{buildroot}%{_sysconfdir}/profile.d
install -p -c -m644 %{S:101} %{buildroot}%{_sysconfdir}/DIR_COLORS
install -p -c -m644 %{S:102} %{buildroot}%{_sysconfdir}/DIR_COLORS.xterm
install -p -c -m644 %{S:105} %{buildroot}%{_sysconfdir}/profile.d/colorls.sh
install -p -c -m644 %{S:106} %{buildroot}%{_sysconfdir}/profile.d/colorls.csh

# su
install -m 4755 src/su %{buildroot}/bin
#install -m 755 src/runuser %{buildroot}/sbin

# These come from util-linux and/or procps.
for i in hostname uptime kill ; do
    rm %{buildroot}{%{_bindir}/$i,%{_mandir}/man1/$i.1}
done

%{?!nopam:install -p -m 644 %{S:200} %{buildroot}%{_sysconfdir}/pam.d/su}
%{?!nopam:install -p -m 644 %{S:202} %{buildroot}%{_sysconfdir}/pam.d/su-l}


# Use hard links instead of symbolic links for LC_TIME files (bug #246729).
find %{buildroot}%{_datadir}/locale -type l | \
(while read link
 do
   target=$(readlink "$link")
   rm -f "$link"
   ln "$(dirname "$link")/$target" "$link"
 done)



%remove_docs

%files
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
/bin/sync
/bin/touch
/bin/true
/bin/uname
/bin/unlink
/bin/mktemp
%{_bindir}/*
%{_sbindir}/chroot
%attr(4755,root,root) /bin/su
