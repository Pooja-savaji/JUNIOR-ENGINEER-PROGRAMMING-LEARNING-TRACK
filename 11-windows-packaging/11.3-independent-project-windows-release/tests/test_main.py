
from src.main import main
def test_main(capsys):
    main()
    output = capsys.readouterr()
    assert "Windows Release Application is running!" in output.out
