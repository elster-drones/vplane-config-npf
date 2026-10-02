#!/usr/bin/env python3

import importlib.util
import io
import json
import logging
import sys
import types
from contextlib import redirect_stdout
from pathlib import Path


def load_module():
    systemd = types.ModuleType("systemd")
    systemd.journal = types.ModuleType("systemd.journal")
    systemd.journal.JournalHandler = object
    sys.modules.setdefault("systemd", systemd)
    sys.modules.setdefault("systemd.journal", systemd.journal)

    vplaned = types.ModuleType("vplaned")
    vplaned.Controller = object
    vplaned.ControllerException = Exception
    sys.modules.setdefault("vplaned", vplaned)

    provisioner = types.ModuleType("vyatta.res_grp.res_grp_provisioner")
    provisioner.Provisioner = object
    sys.modules.setdefault("vyatta", types.ModuleType("vyatta"))
    sys.modules.setdefault("vyatta.res_grp", types.ModuleType("vyatta.res_grp"))
    sys.modules.setdefault("vyatta.res_grp.res_grp_provisioner", provisioner)

    path = Path(__file__).parents[1] / "lib/python3/res_grp_vci.py"
    spec = importlib.util.spec_from_file_location("res_grp_vci", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_get_config_emits_json():
    module = load_module()
    module.LOG = logging.getLogger(__name__)
    expected = {"resources": {"group": {"dscp-group": [{"dscp": [46]}]}}}
    module.get_saved_config = lambda: expected
    output = io.StringIO()

    with redirect_stdout(output):
        assert module.get_config() == 0

    assert json.loads(output.getvalue()) == expected
