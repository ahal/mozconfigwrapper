import os
import pytest
import subprocess

@pytest.fixture
def sh(mozconfigwrapper_sh, env):

    def inner(cmd, custom_env=None):
        result = subprocess.run(
            ["bash", "-c", f". {mozconfigwrapper_sh}\n{cmd}"],
            capture_output=True,
            text=True,
            env=custom_env or env,
        )
        return result.stdout.strip()

    return inner


def test_buildwith(home, sh):
    output = sh("mkmozconfig foo && buildwith foo")
    assert output.splitlines()[-1] == os.path.join(home, "foo")


def test_buildwith_sets_mozconfig(home, sh):
    output = sh(
        "mkmozconfig foo > /dev/null 2>&1 && mkmozconfig bar > /dev/null 2>&1"
        " && buildwith foo silent && echo $MOZCONFIG")
    assert output == os.path.join(home, "foo")


def test_buildwith_custom_command(home, env, sh):
    env["BUILDWITH_COMMAND"] = "export MOZCONFIG=#1 && echo Now building with:"
    output = sh("mkmozconfig bar > /dev/null 2>&1 && buildwith bar", env)
    assert output == f"Now building with:\n{os.path.join(home, 'bar')}"


def test_rmmozconfig(home, sh):
    output = sh("mkmozconfig foo > /dev/null 2>&1 && rmmozconfig foo")
    assert output == f"Removed: {os.path.join(home, 'foo')}"
    assert not os.path.exists(os.path.join(home, "foo"))
