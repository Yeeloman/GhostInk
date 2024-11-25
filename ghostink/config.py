from pathlib import Path
import typer
from typing import Optional
import os


class AppConfig:
    """Centralized configuration manager for GhostInk."""

    def __init__(self, app_name: str = "ghosty"):
        """
        Initializes the AppConfig instance.

        Parameters:
        - app_name (str): The name of the application (default: "ghosty").
        """
        self.app_name = app_name
        self.app_dir = Path(typer.get_app_dir(app_name))
        self.app_dir.mkdir(exist_ok=True)
        self.config_file = self.app_dir / ".ghostink_config"

    def load_project_path(self) -> Optional[Path]:
        """
        Load the project path from the GHOSTINK environment variable or config file.

        Returns:
        - Optional[Path]: The project path, or None if not found.
        """
        if os.getenv("GHOSTINK"):
            return Path(os.getenv("GHOSTINK"))
        elif self.config_file.exists():
            with open(self.config_file, "r") as file:
                line = file.read().strip()
                if line.startswith("GHOSTINK="):
                    path = line.split("=", 1)[1].strip().strip('"').strip("'")
                    return Path(path)
        return None

    def save_project_path(self, path: Path):
        """
        Save the project path to the config file.

        Parameters:
        - path (Path): The project path to save.
        """
        with self.config_file.open("w") as file:
            file.write(f"GHOSTINK='{path}'")

    def get_app_dir(self) -> Path:
        """
        Get the application directory.

        Returns:
        - Path: The path to the application directory.
        """
        return self.app_dir

    def get_config_file(self) -> Path:
        """
        Get the path to the configuration file.

        Returns:
        - Path: The path to the configuration file.
        """
        return self.config_file
