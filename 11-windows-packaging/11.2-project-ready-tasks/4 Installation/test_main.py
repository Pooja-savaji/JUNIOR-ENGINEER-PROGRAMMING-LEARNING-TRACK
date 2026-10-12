
from main import main
def test_main(capsys):
    main()
    assert "Application installed successfully!" in capsys.readouterr().out
