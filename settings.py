class Setting():
    """Loads the game settings from the 'settings.txt' file.
    """
    def __init__(self):
        """Sudoku settings:
            _win_size = Window size
            _block_size = Number of elements in block (4, 6, 9)
            _game_size = Number of blocks in game (2, 4, 6, 9)            
        """
        self._allowed_block_size = [4, 6, 9]
        self._allowed_game_size = [2, 4, 6, 9]
        # Try to load the data, if the file does not exist, load the default data.
        result = self.load_data_from_file()
        if not result:
            self.load_default_settings()

    def save_data_to_file(self) -> str:
        """Saves setting to 'settings.txt' file.
        """
        data = ""
        data += f"_win_size={self._win_size[0]},{self._win_size[1]}\n"
        data += f"_block_size={self._block_size}\n"
        data += f"_game_size={self._game_size}\n"
        data += f"_win_color={self._win_color}\n"
        try:
            with open("settings.txt", "w", encoding="utf-8") as file:
                file.write(data)
        except Exception as e:
            return e
        return ""

    def load_data_from_file(self) -> bool:
        """Loading setting data from 'settings.txt' file in app folder.
        """
        try:
            # Load from file and return True
            with open("settings.txt", "r", encoding="utf-8") as file:
                setting_data = file.read()
            result = self._parse_data(setting_data)
            # If some data is missing, load default values
            if result:
                missing_var = result.split(":")
                missing_var.pop(0)
                for var in missing_var:
                    self.load_data_from_file(var)
            return True
        except FileNotFoundError:
            return False
    
    def _parse_data(self, data_string: str) -> str:
        """If all properties are found in data_string:
            Returns ""
        If some properties are missing:
            Returns "Missing:prop1:prop2:prop3 ..."
        """
        lines = [line.strip() for line in data_string.split("\n") if line != ""]
        data = []
        for line in lines:
            # Split line on property and value
            split_line = line.split("=")
            # Find property name
            property_name = split_line[0].strip()
            # Clean up value
            value = split_line[1].strip()
            allowed_chars = "0123456789,."
            if property_name.find("color") >= 0:
                allowed_chars += "#abcdef"
            for char in split_line[1]:
                if char not in allowed_chars:
                    value.replace("char", "")
            # Add property name and value to data list
            data.append([property_name, value])

        missing = ""
        # Setup _win_size
        index_list = [idx for idx, value in enumerate(data) if value[0] == "_win_size"]
        if index_list:
            index = index_list[0]
            win_size = [x.strip() for x in data[index][1].split(",") if x != ""]
            if len(win_size) < 2:
                missing = missing + ":_win_size"
            else:
                if not win_size[0].isdigit() or not win_size[1].isdigit():
                    missing = missing + ":_win_size"
                else:
                    if int(win_size[0]) < 50 or int(win_size[1]) < 50:
                        missing = missing + ":_win_size"
                    else:
                        self._win_size = (int(win_size[0]), int(win_size[1]))
        else:
            missing = missing + ":_win_size"
        # Setup _block_size
        index_list = [idx for idx, value in enumerate(data) if value[0] == "_block_size"]
        if index_list:
            index = index_list[0]
            block_size = data[index][1]
            if not block_size.isdigit():
                missing = missing + ":_block_size"
            else:
                if int(block_size) not in self._allowed_block_size:
                    missing = missing + ":_block_size"
                else:
                    self._block_size = int(block_size)
        else:
            missing = missing + ":_block_size"
        # Setup _game_size
        index_list = [idx for idx, value in enumerate(data) if value[0] == "_game_size"]
        if index_list:
            index = index_list[0]
            game_size = data[index][1]
            if not game_size.isdigit():
                missing = missing + ":_game_size"
            else:
                if int(game_size) not in self._allowed_game_size:
                    missing = missing + ":_game_size"
                else:
                    self._game_size = int(game_size)
        else:
            missing = missing + ":_game_size"
        # Setup _win_color
        index_list = [idx for idx, value in enumerate(data) if value[0] == "_win_color"]
        if index_list:
            index = index_list[0]
            win_color = self._valid_color(data[index][1])
            if win_color:
                self._win_color = win_color
            else:
                missing = missing + ":_win_color"
        else:
            missing = missing + ":_win_color"

        if missing:
            missing = "Missing" + missing
        
        return missing

    def _valid_color(self, color_value_string: str) -> str:
        """Checks if color string is valid.
        Args:
            color_value_string (str): Color in HEX or RGB format (#000000 or rgb(0,0,0))
        Returns: valid color in hex form
            str: HEX color name or empty string if color is invalid
        """
        color = ""
        is_valid = False
        c_str = color_value_string.strip()
        # Case when a hex value is passed
        if "#" in c_str:
            c_str = c_str.replace("#", "")
            try:
                # Checking if the HEX number is in the range #000000 to #ffffff
                c_int = int(c_str, 16)
                if c_int < 256**3:
                    # Convert c_int back to a hex value and add zeros to the left to make it 6 digits
                    color = hex(c_int)[2:].zfill(6)
                    color = "#" + color
                    is_valid = True
            except (ValueError, TypeError):
                    is_valid = False
        # Case when an rgb value is passed
        if "(" in c_str and ")" in c_str:
            start_pos = c_str.find("(")
            end_pos = c_str.find(")")
            # There must be at least two characters between the brackets (,,) = (0,0,0)
            if (end_pos - start_pos) < 3:
                is_valid = False
            else:
                # c_str = content between brackets
                c_str = c_str[start_pos + 1:end_pos]
                # Separate each number between the brackets separated by a comma, if there is no number, put 0
                values = [x if x != "" else "0" for x in c_str.split(",")]
                # There must be exactly 3 values ​​between the brackets
                if len(values) == 3:
                    # Check if all values ​​are numbers
                    if values[0].isdigit() and values[1].isdigit() and values[2].isdigit():
                        red = int(values[0])
                        green = int(values[1])
                        blue = int(values[2])
                        # Check that all values ​​are in the range 0-255
                        if red in range(0, 256) and green in range(0, 256) and blue in range(0, 256):
                            # Convert each value to a HEX number and pad the left side with zeros to make the number of characters exactly 2
                            red_hex = hex(red)[2:].zfill(2)
                            green_hex = hex(green)[2:].zfill(2)
                            blue_hex = hex(blue)[2:].zfill(2)
                            # Finally, concatenate all HEX values ​​and add # to the beginning
                            color = "#" + red_hex + green_hex + blue_hex
                            is_valid = True
        if is_valid:
            return color
        else:
            return ""

    def load_default_settings(self, property_: str = ""):
        """Sets 'property' variable to default value.
        If 'property' is omitted, sets all variables to default values.
        """
        if property_ == "_win_size" or property_ == "":
            self._win_size = (800, 800)
        if property_ == "_block_size" or property_ == "":
            self._block_size = 4
        if property_ == "_game_size" or property_ == "":
            self._game_size = 4
        if property_ == "_win_color" or property_ == "":
            self._win_color = "#000000"

    @property
    def win_size(self) -> tuple:
        return self._win_size
    
    @win_size.setter
    def win_size(self, value: tuple):
        if not isinstance(value, tuple) or not isinstance(value, list):
            raise TypeError("Window size must be tuple or list with exactly 2 elements")
        if len(value) != 2:
            raise ValueError("Window size: Tuple or list must have exactly 2 elements")
        if value[0] < 50 or value[1] < 50:
            raise ValueError("Window size: Width or height cannot be less than 50")
        self._win_size = value

    @property
    def block_size(self) -> int:
        return self._block_size

    @block_size.setter
    def block_size(self, value: int):
        if not isinstance(value, int):
            raise TypeError("Block size must be integer")
        if value not in self._allowed_block_size:
            raise ValueError(f"Block size can be only values {self._allowed_block_size}")
        self._block_size = value

    @property
    def game_size(self) -> int:
        return self._game_size

    @game_size.setter
    def game_size(self, value: int):
        if not isinstance(value, int):
            raise TypeError("Game size must be integer")
        if value not in self._allowed_game_size:
            raise ValueError(f"Game size can be only values {self._allowed_game_size}")
        self._game_size = value

    @property
    def win_color(self) -> str:
        return self._win_color

    @win_color.setter
    def win_color(self, value: str):
        color = self._valid_color(value)
        if isinstance(value, str):
            if color:
                self._win_color = color
            else:
                raise ValueError("Color must have a value in HEX format (#XXXXXX) or RGB(XXX,XXX,XXX)")
        else:
            raise TypeError("Color value must be string in HEX format (#XXXXXX) or RGB(XXX,XXX,XXX)")

