# -*- coding: utf-8 -*-
#
# This file is part of autosemver.
# Copyright (C) 2016 David Caro.
#
# autosemver is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# autosemver is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with autosemver; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
import pytest

from autosemver import packaging


def test_current_version_falls_back_to_installed_metadata(monkeypatch, tmpdir):
    class FakeMetadata:
        @staticmethod
        def version(project_name):
            assert project_name == "sample-project"
            return "1.2.3"

    def fail_current_version(repo_path):
        raise RuntimeError("not a git repository")

    monkeypatch.setattr(packaging, "importlib_metadata", FakeMetadata)
    monkeypatch.setattr(packaging.api, "get_current_version", fail_current_version)

    assert (
        packaging.get_current_version(
            project_name="sample-project",
            project_dir=str(tmpdir),
        )
        == "1.2.3"
    )


def test_installed_version_requires_metadata_module(monkeypatch):
    monkeypatch.setattr(packaging, "importlib_metadata", None)

    with pytest.raises(ImportError, match="importlib.metadata is unavailable"):
        packaging._get_installed_version("sample-project")
