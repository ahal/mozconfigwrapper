import importlib
import os
from unittest import mock

import pytest

# __init__.py does `from .mozconfig import *`, shadowing the submodule
# attribute with the `mozconfig` function. importlib.import_module returns
# the actual module object, bypassing that attribute lookup.
mozconfig = importlib.import_module("mozconfigwrapper.mozconfig")


@pytest.fixture(autouse=True)
def setup(home, env, monkeypatch):
    monkeypatch.setattr(mozconfig, "mozconfigdir", str(home))
    monkeypatch.setattr(os, "environ", dict(env))


def test_no_active_mozconfig(capsys):
    mozconfig.mozconfig([])
    assert capsys.readouterr().out.strip() == "No mozconfig activated"


def test_mkmozconfig_creates_file(home):
    mozconfig.mkmozconfig("foo")
    assert os.path.isfile(home / "foo")


@pytest.mark.parametrize("expected", [
    "MOZ_OBJDIR=@TOPSRCDIR@/foo",
    "ac_add_options --enable-application=browser",
])
def test_mkmozconfig_content(home, expected):
    mozconfig.mkmozconfig("foo")
    assert expected in (home / "foo").read_text()


def test_mozconfig_shows_current(home, monkeypatch, capsys):
    mozconfig.mkmozconfig("foo")
    monkeypatch.setenv("MOZCONFIG", str(home / "foo"))
    mozconfig.mozconfig([])
    assert capsys.readouterr().out.strip() == str(home / "foo")


@pytest.mark.parametrize("flag", ["-l", "--list"])
def test_mozconfig_list(home, monkeypatch, flag, capsys):
    mozconfig.mkmozconfig("foo")
    mozconfig.mkmozconfig("bar")
    monkeypatch.setenv("MOZCONFIG", str(home / "bar"))
    mozconfig.mozconfig([flag])
    assert capsys.readouterr().out.strip() == "bar*\nfoo"


def test_mozconfig_list_after_remove(home, monkeypatch, capsys):
    mozconfig.mkmozconfig("foo")
    mozconfig.mkmozconfig("bar")
    os.remove(home / "foo")
    monkeypatch.setenv("MOZCONFIG", str(home / "bar"))
    mozconfig.mozconfig(["--list"])
    assert capsys.readouterr().out.strip() == "bar*"


def test_mozconfig_edit_no_editor(home, monkeypatch, capsys):
    mozconfig.mkmozconfig("bar")
    monkeypatch.setenv("MOZCONFIG", str(home / "bar"))
    mozconfig.mozconfig(["-e"])
    assert capsys.readouterr().out.strip() == "Can't open editor, EDITOR environment variable not set"


def test_mozconfig_edit_launches_editor(home, monkeypatch):
    mozconfig.mkmozconfig("bar")
    path = str(home / "bar")
    monkeypatch.setenv("MOZCONFIG", path)
    monkeypatch.setenv("EDITOR", "cat")
    with mock.patch("subprocess.call") as mock_call:
        mozconfig.mozconfig(["-e"])
    mock_call.assert_called_once_with(["cat", path])
