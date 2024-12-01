"""
Module: config.py
Purpose: To store all the configurations for the application.
"""

import os
from typing import Any, Generator, Mapping


class Configuration:
    def __init__(self):
        pass

    def __repr__(self) -> str:
        items = []
        for key, value in self.__dict__.items():
            key = "".join(_ for _ in key.split("_")).upper()
            items.append(f"{key}={value}")
        out_s = "\n```toml\n"
        out_e = "\n```"
        return out_s + "\n".join(items) + out_e

    def __str__(self) -> str:
        return self.__repr__()

    def __getitem__(self, key: str) -> str:
        try:
            return os.environ[key]
        except KeyError:
            return self.__dict__.get(key, "")

    def __setitem__(self, key: str, value: str) -> None:
        try:
            os.environ[key] = value
        except KeyError:
            pass
        except Exception as e:
            print(
                "Encountered an error while setting the environment variable.",
                e
            )
        finally:
            self.__dict__[key] = value

    def __delitem__(self, key: str) -> None:
        try:
            del os.environ[key]
        except KeyError:
            pass
        except Exception as e:
            print(
                "Encountered an error while deleting \
                    the environment variable.",
                e
            )
        finally:
            del self.__dict__[key]

    def __contains__(self, key: str) -> bool:
        try:
            return True if os.environ[key] else False
        except KeyError:
            return True if self.__dict__.get(key) else False

    def __iter__(self) -> Generator[tuple[str, Any], None, None]:
        _items = self.__dict__.items()
        for item in _items:
            yield item

    def __len__(self) -> int:
        return len(self.__dict__)

    def __bool__(self) -> NotImplementedError:
        return NotImplementedError("This method is not implemented.")

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Configuration):
            return False
        if not self.__hash__() == other.__hash__():
            return False
        for key, value in self.__dict__.items():
            if not other.__dict__.get(key) == value:
                return False
        return True

    def __hash__(self) -> int:
        return hash(tuple(self.__dict__.items()))

    @classmethod
    def initialize(cls, file_path: str | None = None) -> "Configuration":
        if not file_path:
            file_path = os.path.join(os.path.dirname(
                os.path.dirname(__file__)), ".env")
        _instance = cls()
        try:
            with open(file_path, "r") as file:
                for line in file:
                    key, value = line.strip().split("=")
                    _instance.__setattr__(key, value)
        except FileNotFoundError:
            raise FileNotFoundError(
                "The configuration file is not found.", file_path)
        except Exception as e:
            print("Encountered an error while initializing \
                  the configuration.", e)
        return _instance

    @classmethod
    def initialize_from_mapping(
        cls, config: Mapping[str, str]
    ) -> "Configuration":
        _instance = cls()
        for key, value in config.items():
            _instance.__setattr__(key, value)
        return _instance

    @classmethod
    def initialize_from_env(cls) -> "Configuration":
        _instance = cls()
        for key, value in os.environ.items():
            _instance.__setattr__(key, value)
        return _instance

    def save(self, file_path: str | None = None) -> None:
        if not file_path:
            file_path = os.path.join(__file__, ".env")
        try:
            with open(file_path, "w") as file:
                for key, value in self.__dict__.items():
                    file.write(f"{key}={value}\n")
        except Exception as e:
            print("Encountered an error while saving the configuration.", e)
        return None

    @classmethod
    def from_json(
        cls,
        json_data: str | None = None,
        file_path: str | None = None
    ) -> "Configuration":
        if not json_data and not file_path:
            raise ValueError(
                "Either the JSON data or the file path must be provided.")
        if json_data and file_path:
            raise ValueError(
                "Both the JSON data and the file path cannot be provided.")
        if json_data and not file_path:
            try:
                import json
                config = json.loads(json_data)
            except Exception as e:
                print("Encountered an error while loading the JSON data.", e)
        if not json_data and file_path:
            try:
                import json
                with open(file_path, "r") as file:
                    config = json.load(file)
            except FileNotFoundError:
                raise FileNotFoundError(
                    "The configuration file is not found.", file_path)
            except Exception as e:
                print(
                    "Encountered an error while loading the configuration.",
                    e
                )
        return cls.initialize_from_mapping(config)

    def to_json(self, file_path: str | None = None) -> str | None:
        try:
            import json
            config = {key: value for key, value in self.__dict__.items()}
            if not file_path:
                return json.dumps(config)
            with open(file_path, "w") as file:
                json.dump(config, file)
        except Exception as e:
            print("Encountered an error while saving the configuration.", e)
        return None

    def to_dict(self) -> dict[str, Any]:
        return {key: value for key, value in self.__dict__.items()}

    def to_mapping(self) -> Mapping[str, Any]:
        return {key: value for key, value in self.__dict__.items()}

    def to_env(self) -> None:
        for key, value in self.__dict__.items():
            os.environ[key] = value
        return None

    def clear(self) -> None:
        for key in self.__dict__.keys():
            self.__delitem__(key)
        return None

    def copy(self) -> "Configuration":
        return self.initialize_from_mapping(self.to_mapping())

    def update(self, config: Mapping[str, str]) -> None:
        for key, value in config.items():
            self.__setattr__(key, value)
        return None

    def from_yaml(
        cls,
            yaml_data: str | None = None,
            file_path: str | None = None
    ) -> "Configuration":
        if not yaml_data and not file_path:
            raise ValueError(
                "Either the YAML data or the file path must be provided.")
        if yaml_data and file_path:
            raise ValueError(
                "Both the YAML data and the file path cannot be provided.")
        if yaml_data and not file_path:
            try:
                import yaml
                config = yaml.safe_load(yaml_data)
            except Exception as e:
                print("Encountered an error while loading the YAML data.", e)
        if not yaml_data and file_path:
            try:
                import yaml
                with open(file_path, "r") as file:
                    config = yaml.safe_load(file)
            except FileNotFoundError:
                raise FileNotFoundError(
                    "The configuration file is not found.", file_path)
            except Exception as e:
                print(
                    "Encountered an error while loading the configuration.",
                    e
                )
        return cls.initialize_from_mapping(config)

    def to_yaml(self, file_path: str | None = None) -> str | None:
        try:
            import yaml
            config = {key: value for key, value in self.__dict__.items()}

            # Format the config keys for yaml output
            config = {key.replace("_", " "): value for key,
                      value in config.items()}

            # make all keys lowercase
            config = {key.lower(): value for key, value in config.items()}

            if not file_path:
                return yaml.dump(config)
            with open(file_path, "w") as file:
                yaml.dump(config, file)
        except ImportError:
            raise ImportError(
                "The PyYAML package is not installed.\
                Please install it using 'pip install pyyaml'.")
        except yaml.YAMLError as e:
            print("Encountered an error while saving the configuration.", e)
        except Exception as e:
            print("Encountered an error while saving the configuration.", e)
        return None


if __name__ == '__main__':
    config = Configuration.initialize()
    print(config)
    config.to_yaml("config.yaml")
    # print(config["SECRET_KEY"])
    # config["SECRET_KEY"] = "new_secret_key"
