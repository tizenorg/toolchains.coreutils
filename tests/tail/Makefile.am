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
x = tail
explicit =
maint_gen = obs-plus-c1.I obs-plus-c1.X obs-plus-c2.I obs-plus-c2.X obs-c3.I \
obs-c3.X obs-c4.I obs-c4.X obs-c5.I obs-c5.X obs-l1.I obs-l1.X obs-l2.I \
obs-l2.X obs-l3.I obs-l3.X obs-plus-l4.I obs-plus-l4.X obs-plus-l5.I \
obs-plus-l5.X obs-1.I obs-1.X obs-2.I obs-2.X obs-3.I obs-3.X obs-plus-4.I \
obs-plus-4.X obs-plus-5.I obs-plus-5.X obs-plus-x1.I obs-plus-x1.X \
obs-plus-x2.I obs-plus-x2.X obs-l.I obs-l.X obs-b.I obs-b.X err-1.I err-1.X \
err-2.I err-2.X err-3.I err-3.X err-4.I err-4.X err-5.I err-5.X err-6.I \
err-6.X minus-1.I minus-1.X minus-2.I minus-2.X c-2.I c-2.X c-2-minus.I \
c-2-minus.X c2.I c2.X c2-minus.I c2-minus.X n-1.I n-1.X n-2.I n-2.X n-3.I \
n-3.X n-4.I n-4.X n-4a.I n-4a.X n-5.I n-5.X n-5a.I n-5a.X n-5b.I n-5b.X \
f-pipe-1.I f-pipe-1.X
run_gen = obs-plus-c1.O obs-plus-c1.E obs-plus-c2.O obs-plus-c2.E obs-c3.O \
obs-c3.E obs-c4.O obs-c4.E obs-c5.O obs-c5.E obs-l1.O obs-l1.E obs-l2.O \
obs-l2.E obs-l3.O obs-l3.E obs-plus-l4.O obs-plus-l4.E obs-plus-l5.O \
obs-plus-l5.E obs-1.O obs-1.E obs-2.O obs-2.E obs-3.O obs-3.E obs-plus-4.O \
obs-plus-4.E obs-plus-5.O obs-plus-5.E obs-plus-x1.O obs-plus-x1.E \
obs-plus-x2.O obs-plus-x2.E obs-l.O obs-l.E obs-b.O obs-b.E err-1.O err-1.E \
err-2.O err-2.E err-3.O err-3.E err-4.O err-4.E err-5.O err-5.E err-6.O \
err-6.E minus-1.O minus-1.E minus-2.O minus-2.E c-2.O c-2.E c-2-minus.O \
c-2-minus.E c2.O c2.E c2-minus.O c2-minus.E n-1.O n-1.E n-2.O n-2.E n-3.O \
n-3.E n-4.O n-4.E n-4a.O n-4a.E n-5.O n-5.E n-5a.O n-5a.E n-5b.O n-5b.E \
f-pipe-1.O f-pipe-1.E
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
