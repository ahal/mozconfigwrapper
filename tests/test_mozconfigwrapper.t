  $ . $TESTDIR/setup > /dev/null

  $ mozconfig
  No mozconfig activated

  $ mkmozconfig foo
  Created: /tmp/mozconfigs/foo
  $ mozconfig
  /tmp/mozconfigs/foo

  $ mkmozconfig bar
  Created: /tmp/mozconfigs/bar
  $ mozconfig
  /tmp/mozconfigs/bar
  $ mozconfig -l
  bar*
  foo

  $ mozconfig -e
  Can't open editor, EDITOR environment variable not set
  $ export EDITOR=cat
  $ mozconfig -e
  mk_add_options MOZ_OBJDIR=@TOPSRCDIR@/bar
  
  ac_add_options --enable-application=browser


  $ rmmozconfig foo
  Removed: /tmp/mozconfigs/foo
  $ mozconfig --list
  bar*

  $ . $TESTDIR/teardown > /dev/null
