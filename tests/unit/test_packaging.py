"""Tests for generated packaging files."""

import pytest
from dulwich import porcelain

from autosemver import packaging


@pytest.mark.parametrize(
    "filename, getter, creator",
    [
        ("CHANGELOG", packaging.get_changelog, packaging.create_changelog),
        ("RELEASE_NOTES", packaging.get_releasenotes, packaging.create_releasenotes),
    ],
)
def test_generated_file_uses_project_directory(
    tmp_path, monkeypatch, filename, getter, creator
):
    project = tmp_path / "project"
    project.mkdir()
    with porcelain.init(str(project)) as repo:
        (project / "example.py").write_text("# Example\n")
        porcelain.add(repo, paths=[str(project / "example.py")])
        porcelain.commit(
            repo, message=b"Initial commit", author=b"Example <example@example.org>"
        )
    expected = getter(project_dir=str(project)).encode("utf-8")
    if filename == "RELEASE_NOTES":
        expected += b"\n"

    working_directory = tmp_path / "working"
    working_directory.mkdir()
    unrelated_file = working_directory / filename
    unrelated_file.write_text("Keep this file\n")
    monkeypatch.chdir(working_directory)

    creator(project_dir=str(project))

    assert (project / filename).read_bytes() == expected
    assert unrelated_file.read_text() == "Keep this file\n"


@pytest.mark.parametrize(
    "filename, creator",
    [
        ("CHANGELOG", packaging.create_changelog),
        ("RELEASE_NOTES", packaging.create_releasenotes),
    ],
)
def test_generated_file_skips_packaged_project(
    tmp_path, monkeypatch, filename, creator
):
    project = tmp_path / "project"
    project.mkdir()
    (project / "PKG-INFO").touch()
    monkeypatch.chdir(tmp_path)

    creator(project_dir=str(project))

    assert not (project / filename).exists()
    assert not (tmp_path / filename).exists()
