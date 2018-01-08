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

  $ buildwith foo
  /tmp/mozconfigs/foo
  $ echo $MOZCONFIG
  /tmp/mozconfigs/foo

  $ export BUILDWITH_COMMAND="export MOZCONFIG=#1 && echo Now building with:"
  $ buildwith bar 
  Now building with:
  /tmp/mozconfigs/bar
  $ echo $MOZCONFIG
  /tmp/mozconfigs/bar

  $ rmmozconfig foo
  Removed: /tmp/mozconfigs/foo
  $ mozconfig --list
  bar*

  $ . $TESTDIR/teardown > /dev/null
