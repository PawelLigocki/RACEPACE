from app.cli import main
import sys


def test_cli_pace(capsys):
    sys.argv = ["prog", "pace", "--distance", "10", "--time", "50"]
    main()

    captured = capsys.readouterr()
    assert "Pace" in captured.out


def test_cli_predict(capsys):
    sys.argv = ["prog", "predict", "--distance", "5", "--time", "25", "--target", "10"]
    main()

    captured = capsys.readouterr()
    assert "Predicted time" in captured.out