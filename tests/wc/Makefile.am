# Make coreutils tests.					-*-Makefile-*-

# Copyright (C) 1997, 1998, 2000, 2003, 2004, 2006 Free Software
# Foundation, Inc.

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.

##test-files-begin
x = wc
explicit =
maint_gen = a0.I a0.X a1.I a1.X a2.I a2.X a3.I a3.X a4.I a4.X a5.I a5.X a6.I \
a6.X a7.I a7.X a8.I a8.X a9.I a9.X b0.I b0.X b1.I b1.X c0.I c0.X c1.I c1.X \
c2.I c2.X
run_gen = a0.O a0.E a1.O a1.E a2.O a2.E a3.O a3.E a4.O a4.E a5.O a5.E a6.O \
a6.E a7.O a7.E a8.O a8.E a9.O a9.E b0.O b0.E b1.O b1.E c0.O c0.E c1.O c1.E \
c2.O c2.E
##test-files-end

EXTRA_DIST = Test.pm $x-tests $(explicit) $(maint_gen)
noinst_SCRIPTS = $x-tests
TESTS_ENVIRONMENT = \
  CU_TEST_NAME=`basename $(abs_srcdir)`,$$tst \
  PATH="$(VG_PATH_PREFIX)`pwd`/../../src$(PATH_SEPARATOR)$$PATH"

editpl = sed -e 's,@''PERL''@,$(PERL),g' -e 's,@''srcdir''@,$(srcdir),g'

TESTS = $x-tests

mk_script = $(srcdir)/../mk-script
$(srcdir)/$x-tests: $(mk_script) Test.pm Makefile.am
	test '$x' = test && prog=../../src/$x || prog=$x; \
	$(PERL) -I$(srcdir) -w -- $(mk_script) $(srcdir) $$prog > $@.n
	mv $@.n $@
	chmod 755 $@

MAINTAINERCLEANFILES = $x-tests $(maint_gen)
CLEANFILES = $(run_gen)

check: $(maint_gen)

$(srcdir)/Makefile.am: ../Makefile.am.in Test.pm $(mk_script)
	rm -f $@ $@t
	sed -n '1,/^##test-files-begin/p' $(srcdir)/../Makefile.am.in > $@t
	tool=`echo $(subdir)|sed 's/^tests.//;s/-test//'`; \
	  echo "x = $$tool" >> $@t
	$(PERL) -I$(srcdir) -w -- $(mk_script) $(srcdir) --list >> $@t
	sed -n '/^##test-files-end/,$$p' $(srcdir)/../Makefile.am.in >> $@t
	chmod -w $@t
	mv $@t $@
