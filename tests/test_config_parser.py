
import pytest
from src.config_parser import ConfigError, ConfigParser
from maze.structs import MazeSpecs

@pytest.fixture
def parser():
    return ConfigParser()

@pytest.fixture
def valid_input_config():
    return {"WIDTH": "10",
            "HEIGHT": "10",
            "ENTRY": "2,9",
            "EXIT": "5,5",
            "OUTPUT_FILE": "out.txt",
            "PERFECT": True}


def test_read_txt_parsing(tmp_path, parser):
    # check parsing is done correctly
    test_dir = tmp_path / "test_dir"
    test_dir.mkdir()

    test_config = test_dir / "test_config.txt"
    test_config.write_text("#a\nHEIGHT=20\nOUTPUT_FILE=maze.txt")

    result = parser.read_txt(test_config)
    assert isinstance(result, dict)
    assert "#" not in result
    assert "HEIGHT" in result


def test_read_txt_raising(tmp_path, parser):
    # check parser error raising correctly
    with pytest.raises(ConfigError, match="locating"):
        parser.read_txt('non_existent')

    test_dir = tmp_path / "test_dir"
    test_dir.mkdir()

    test_config = test_dir / "test_config.txt"    
    test_config.write_text("#hi\nHEIGHT20\nWIDTH10\n")
    with pytest.raises(ConfigError):
        parser.read_txt(test_config)


@pytest.mark.parametrize("bad_input", ["abc", "-1", "-2,-2"])
def test_invalid_raises(parser, valid_input_config, bad_input):
    with pytest.raises(ConfigError, match='Validation'):
        valid_input_config['WIDTH'] = bad_input
        parser.validate_config(valid_input_config)



def test_validator_return(parser, valid_input_config):
    result = parser.validate_config(valid_input_config)
    assert isinstance (result, MazeSpecs)
    

def test_missing_vals(parser):
    with pytest.raises(ConfigError, match='missing'):
        parser.validate_config({"HEIGHT": 10})


@pytest.mark.parametrize("boundary", ["1", "0", "2", "-10"])
def test_boundaries(parser, valid_input_config, boundary):
    valid_input_config["WIDTH"] = boundary
    with pytest.raises(ConfigError, match='Validation'):
        parser.validate_config(valid_input_config)


@pytest.mark.parametrize("entry_exit", ["100,100"])
def test_entry_exit(parser, valid_input_config, entry_exit):
    valid_input_config["ENTRY"] = entry_exit
    with pytest.raises(ConfigError, match='bounds'):
        parser.validate_config(valid_input_config)
        

    

