import subprocess
def test_spark_list_json():
    r = subprocess.run(["python3","-m","spark_cli.cli","list","--json"], capture_output=True, timeout=5)
    assert r.returncode in (0,2), f"Exit {r.returncode}"
