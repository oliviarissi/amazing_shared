
from pydantic import ValidationError
from enum import Enum
from typing import Any
from maze.structs import MazeSpecs

class Configs(Enum):
    WIDTH="WIDTH"
    HEIGHT="HEIGHT"
    ENTRY="ENTRY"
    EXIT="EXIT"
    OUTPUT_FILE="OUTPUT_FILE"
    PERFECT="PERFECT"


class ConfigError(Exception):
    """for custom parser error messages"""
    pass


class ConfigParser():

    def read_txt(self, file_name: str) -> dict[str, Any]:
        """
        Function that reads a file from file_name (e.g. 'config.txt')
        looking for KEY=VALUE lines in the file, it creates & returns
        a dict of {KEY: VALUE} to be validated.
        """

        txt_config: dict[str, Any] = {}
        try:
            with open(file_name) as f:
                for line in f:
                    if not (line.startswith("#") or line.isspace()):
                        key, value = line.split("=", 1)
                        txt_config.update({key.strip(): value.strip()})
                return txt_config
        except FileNotFoundError:
            raise ConfigError(f"Error locating file '{file_name}'")
        except Exception as e:
            raise ConfigError(f"Unknown error reading the file - {e}")

    

    def validate_config(self, txt_config: dict[str, Any]) -> MazeSpecs:
        """
        Takes raw dict from read_text and validates the data
        against BaseModel. 
        If validation successful, maze specs are returned
        Else, informative error message.
        """

        required: set[str] = {e.value for e in Configs}
        provided: set[str] = set(txt_config.keys())

        if not required.issubset(provided):
            missing: set[str] = required - provided
            raise ConfigError(f"Mandatory keys missing - {", ".join(missing)}")
        else:
            try:
                valid_config = MazeSpecs(**txt_config)
                return valid_config
            except ValidationError as e:
                error_msgs = [err['msg'] for err in e.errors()]
                complete_err = "\n".join(error_msgs)
                raise ConfigError(f"Validation failed - {complete_err}")
        

# if __name__ == "__main__":
#     file_name = "sample_config.txt"
#     my_test = ConfigParser.read_txt(file_name)
#     print(my_test)
#     new_config = ConfigParser.validate_config(my_test)
#     print(type(new_config))
#     print(new_config)

