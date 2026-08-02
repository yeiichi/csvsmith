import pytest

from csvsmith.cli import main
from csvsmith.tools.strip_bom import UTF8_BOM, default_output_path, strip_utf8_bom


def test_strip_utf8_bom_writes_default_output_without_bom(tmp_path):
    source = tmp_path / "input.csv"
    source.write_bytes(UTF8_BOM + b"id,name\r\n1,Alice\r\n")

    result = strip_utf8_bom(source)

    assert result.output_path == tmp_path / "input.no-bom.csv"
    assert result.removed is True
    assert result.output_path.read_bytes() == b"id,name\r\n1,Alice\r\n"
    assert source.read_bytes().startswith(UTF8_BOM)


def test_strip_utf8_bom_preserves_file_without_bom(tmp_path):
    source = tmp_path / "input.csv"
    output = tmp_path / "output.csv"
    source.write_bytes(b"id,name\n1,Alice\n")

    result = strip_utf8_bom(source, output)

    assert result.output_path == output
    assert result.removed is False
    assert output.read_bytes() == b"id,name\n1,Alice\n"


def test_strip_utf8_bom_can_rewrite_in_place(tmp_path):
    source = tmp_path / "input.csv"
    source.write_bytes(UTF8_BOM + b"id,name\n1,Alice\n")

    result = strip_utf8_bom(source, in_place=True)

    assert result.output_path == source
    assert result.removed is True
    assert source.read_bytes() == b"id,name\n1,Alice\n"


def test_strip_utf8_bom_rejects_in_place_with_output(tmp_path):
    source = tmp_path / "input.csv"
    source.write_bytes(UTF8_BOM + b"id,name\n")

    with pytest.raises(ValueError, match="--in-place"):
        strip_utf8_bom(source, tmp_path / "output.csv", in_place=True)


def test_default_output_path_handles_multi_dot_names():
    assert default_output_path("report.final.csv").name == "report.final.no-bom.csv"


def test_strip_bom_cli_writes_requested_output(tmp_path, capsys):
    source = tmp_path / "input.csv"
    output = tmp_path / "clean.csv"
    source.write_bytes(UTF8_BOM + b"id,name\n1,Alice\n")

    exit_code = main(["strip-bom", str(source), "-o", str(output)])

    assert exit_code == 0
    assert output.read_bytes() == b"id,name\n1,Alice\n"
    assert "removed BOM" in capsys.readouterr().out
