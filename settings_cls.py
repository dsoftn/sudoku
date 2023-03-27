class Setting():
    """Loads the game settings from the 'settings.txt' file.
    """
    def __init__(self):
        """Sudoku settings:
            _win_size = Window size
            _block_size = Number of elements in block (4, 6, 9)
            _game_size = Number of blocks in game (1, 2, 4, 6, 9)            
        """
        # Internal variables 
        self._allowed_block_size = [6, 9]
        self._allowed_game_size = [6, 9]
        self._game_surface_padding_top = 150
        self._game_surface_padding_bottom = 50
        self._game_surface_zoom_level = 0  # Zoom 0-5  0=max zoom (default)
        self._game_surface_min_height = 200
        # All available settings
        self._win_size = (0,0)
        self._win_color = "#000000"
        self._block_size = 4
        self._game_size = 2
        self._lang_dict = {}  # Language items  key=item : value=[english,srpski]
        self._lang = 0  # Language 0=english, 1=srpski
        self._board_font_name = "Arial"  # Font for numbers on board
        self._board_font_size = 12  # Font size for numbers on board
        self._board_font_color = "#000000" # Font color for numbers on board
        self._selection_pos_x = 0  # Position of selected element (x)
        self._selection_pos_y = 0  # Position of selected element (Y)
        self._game_level = 1  # Level of game (1 - easy ... 5 - Very Hard)
        self._level_points = 12  # Percent of empty cells, lvl*points = 1x12 = 12% of empty cells  (5-16)
        # Try to load the data, if the file does not exist, load the default data.
        result = self.load_data_from_file()
        if not result:
            self.load_default_settings()
        self._load_language()

    def lang(self, key_value: str) -> str:
        if key_value in self._lang_dict.keys():
            return self._lang_dict[key_value][self._lang]
        else:
            return "Error."

    def _load_language(self) -> bool:
        try:
            # Load from file and return True
            with open("settings.txt", "r", encoding="utf-8") as file:
                text = file.read()
                lines = text.split("\n")
                for line in lines:
                    if line[:11] == "[language] ":
                        lang_line = line[11:]
                        spliter = lang_line.find("=")
                        if spliter:
                            lang_item = lang_line[:spliter]
                            lang_values = lang_line[spliter + 1:]
                            lang_value = lang_values.split("|")
                            lang_en = lang_value[0]
                            lang_ser = lang_value[1]
                            self._lang_dict[lang_item] = [lang_en, lang_ser]
            return True
        except FileNotFoundError:
            return False
    
    def save_data_to_file(self) -> str:
        """Saves setting to 'settings.txt' file.
        """
        # Add to data string all settings
        data = ""
        data += f"_win_size={self._win_size[0]},{self._win_size[1]}\n"
        data += f"_block_size={self._block_size}\n"
        data += f"_game_size={self._game_size}\n"
        data += f"_win_color={self._win_color}\n"
        data += f"_lang={self._lang}\n"
        data += f"_game_surface_zoom_level={self._game_surface_zoom_level}\n"
        data += f"_board_font_name={self._board_font_name}\n"
        data += f"_board_font_color={self._board_font_color}\n"
        data += f"_game_level={self._game_level}\n"
        data += f"_level_points={self._level_points}\n"
        # Load to lines_to_write all language records from settings.txt
        lines_to_write = ""
        try:
            with open("settings.txt", "r", encoding="utf-8") as file:
                text = file.read()
                lines = text.split("\n")
                for line in lines:
                    if line[:11] == "[language] ":
                        lines_to_write += line + "\n"
        except FileNotFoundError:
            lines_to_write = ""
        # Concatenate data and lines_to_write
        data += lines_to_write
        # Wite file settings.txt
        with open("settings.txt", "w", encoding="utf-8") as file:
            file.write(data)
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
                    self.load_default_settings(var)
            return True
        except FileNotFoundError:
            return False
    
    def _parse_data(self, data_string: str) -> str:
        """If all properties are found in data_string:
            Returns ""
        If some properties are missing:
            Returns "Missing:prop1:prop2:prop3 ..."
        """
        # First append in data list all commands and values
        lines = [line.strip() for line in data_string.split("\n") if line != ""]
        data = []
        for line in lines:
            # If language - skip entry
            if line[:11] == "[language] ":
                continue
            # Split line on property and value
            split_line = line.split("=")
            # Find property name
            property_name = split_line[0].strip()
            # Find value
            value = split_line[1].strip()
            # Add property name and value to data list
            data.append([property_name, value])
        # Then update variables if found in data list
        # If variable not found in data list append (:var_name) in missing string
        missing = ""
        # Setup _win_size
        index_list = [idx for idx, value in enumerate(data) if value[0] == "_win_size"]
        if index_list:
            index = index_list[0]
            _win_size = [x.strip() for x in data[index][1].split(",") if x != ""]
            if len(_win_size) != 2:
                missing = missing + ":_win_size"
            else:
                if not _win_size[0].isdigit() or not _win_size[1].isdigit():
                    missing = missing + ":_win_size"
                else:
                    if int(_win_size[0]) < 50 or int(_win_size[1]) < 50:
                        missing = missing + ":_win_size"
                    else:
                        self._win_size = (int(_win_size[0]), int(_win_size[1]))
        else:
            missing = missing + ":_win_size"
        # Setup _block_size
        index_list = [idx for idx, value in enumerate(data) if value[0] == "_block_size"]
        if index_list:
            index = index_list[0]
            _block_size = data[index][1]
            if not _block_size.isdigit():
                missing = missing + ":_block_size"
            else:
                if int(_block_size) not in self._allowed_block_size:
                    missing = missing + ":_block_size"
                else:
                    self._block_size = int(_block_size)
        else:
            missing = missing + ":_block_size"
        # Setup _game_size
        index_list = [idx for idx, value in enumerate(data) if value[0] == "_game_size"]
        if index_list:
            index = index_list[0]
            _game_size = data[index][1]
            if not _game_size.isdigit():
                missing = missing + ":_game_size"
            else:
                if int(_game_size) not in self._allowed_game_size:
                    missing = missing + ":_game_size"
                else:
                    self._game_size = int(_game_size)
        else:
            missing = missing + ":_game_size"
        # Setup _win_color
        index_list = [idx for idx, value in enumerate(data) if value[0] == "_win_color"]
        if index_list:
            index = index_list[0]
            _win_color = self._valid_color(data[index][1])
            if _win_color:
                self._win_color = _win_color
            else:
                missing = missing + ":_win_color"
        else:
            missing = missing + ":_win_color"
        # Setup language _lang
        index_list = [idx for idx, value in enumerate(data) if value[0] == "_lang"]
        if index_list:
            index = index_list[0]
            _lang = data[index][1]
            if not _lang.isdigit():
                missing = missing + ":_lang"
            else:
                self._lang = int(_lang)
        else:
            missing = missing + ":_lang"
        # Setup _game_surface_zoom_level
        index_list = [idx for idx, value in enumerate(data) if value[0] == "_game_surface_zoom_level"]
        if index_list:
            index = index_list[0]
            _game_surface_zoom_level = data[index][1]
            if not _game_surface_zoom_level.isdigit():
                missing = missing + ":_game_surface_zoom_level"
            else:
                if int(_game_surface_zoom_level) < 0 or int(_game_surface_zoom_level) > 5:
                    missing = missing +":_game_surface_zoom_level"
                else:
                    self._game_surface_zoom_level = int(_game_surface_zoom_level)
        else:
            missing = missing + ":_game_surface_zoom_level"
        # Setup _board_font_name
        index_list = [idx for idx, value in enumerate(data) if value[0] == "_board_font_name"]
        if index_list:
            index = index_list[0]
            _board_font_name = data[index][1].strip()
            if _board_font_name:
                self._board_font_name = _board_font_name
            else:
                missing = missing + "_board_font_name"
        else:
            missing = missing + "_board_font_name"
        # Setup _board_font_color
        index_list = [idx for idx, value in enumerate(data) if value[0] == "_board_font_color"]
        if index_list:
            index = index_list[0]
            _board_font_color = self._valid_color(data[index][1])
            if _board_font_color:
                self._board_font_color = _board_font_color
            else:
                missing = missing + ":_board_font_color"
        else:
            missing = missing + ":_board_font_color"
        # Setup _game_level  1-5
        index_list = [idx for idx, value in enumerate(data) if value[0] == "_game_level"]
        if index_list:
            index = index_list[0]
            _game_level = data[index][1]
            if not _game_level.isdigit():
                missing = missing + ":_game_level"
            else:
                if int(_game_level) < 1 or int(_game_level) > 5:
                    missing = missing +":_game_level"
                else:
                    self._game_level = int(_game_level)
        else:
            missing = missing + ":_game_level"
        # Setup _level_points  5-16
        index_list = [idx for idx, value in enumerate(data) if value[0] == "_level_points"]
        if index_list:
            index = index_list[0]
            _level_points = data[index][1]
            if not _level_points.isdigit():
                missing = missing + ":_level_points"
            else:
                if int(_level_points) < 5 or int(_level_points) > 16:
                    missing = missing +":_level_points"
                else:
                    self._level_points = int(_level_points)
        else:
            missing = missing + ":_level_points"

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
        self._game_size = value

    @property
    def game_size(self) -> int:
        return self._game_size

    @game_size.setter
    def game_size(self, value: int):
        if not isinstance(value, int):
            raise TypeError("Game size must be integer")
        if value not in self._allowed_game_size:
            raise ValueError(f"Game size can only be values {self._allowed_game_size}")
        self._game_size = value
        self._block_size = value

    @property
    def win_color(self) -> str:
        return self._win_color

    @win_color.setter
    def win_color(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Color value must be string in HEX format (#XXXXXX) or RGB(XXX,XXX,XXX)")

        color = self._valid_color(value)
        if color:
            self._win_color = color
        else:
            raise ValueError("Color must have a value in HEX format (#XXXXXX) or RGB(XXX,XXX,XXX)")

    @property
    def elements_in_block_x(self) -> int:
        elements = 0
        if self._block_size == 4:
            elements = 2
        elif self._block_size == 6:
            elements = 3
        elif self._block_size == 9:
            elements = 3
        return elements

    @property
    def elements_in_block_y(self) -> int:
        elements = 0
        if self._block_size == 4:
            elements = 2
        elif self._block_size == 6:
            elements = 2
        elif self._block_size == 9:
            elements = 3
        return elements

    @property
    def blocks_in_game_x(self) -> int:
        blocks = 0
        if self._game_size == 1:
            blocks = 1
        elif self._game_size == 2:
            blocks = 2
        elif self._game_size == 4:
            blocks = 2
        elif self._game_size == 6:
            blocks = 2
        elif self._game_size == 9:
            blocks = 3
        return blocks

    @property
    def blocks_in_game_y(self) -> int:
        blocks = 0
        if self._game_size == 1:
            blocks = 1
        elif self._game_size == 2:
            blocks = 1
        elif self._game_size == 4:
            blocks = 2
        elif self._game_size == 6:
            blocks = 3
        elif self._game_size == 9:
            blocks = 3
        return blocks

    @property
    def elements_in_game_x(self) -> int:
        elements = self.elements_in_block_x * self.blocks_in_game_x
        return elements

    @property
    def elements_in_game_y(self) -> int:
        elements = self.elements_in_block_y * self.blocks_in_game_y
        return elements

    @property
    def game_surface_height(self) -> int:
        padd = self._game_surface_padding_top + self._game_surface_padding_bottom
        surf = self._win_size[1] - padd
        area =surf - self._game_surface_min_height
        step = area / 6
        height = surf - step * self._game_surface_zoom_level
        return int(height)

    @property
    def game_surface_width(self) -> int:
        padd = self._game_surface_padding_top + self._game_surface_padding_bottom
        surf = self._win_size[1] - padd
        area =surf - self._game_surface_min_height
        step = area / 6
        height = surf - step * self._game_surface_zoom_level
        return int(height)

    @property
    def game_surface_pos_x(self) -> int:
        x = (self._win_size[0] - self.game_surface_width) / 2
        return x

    @property
    def game_surface_pos_y(self) -> int:
        area = self._win_size[1] - self._game_surface_padding_top - self._game_surface_padding_bottom
        area_padd_top = (area - self.game_surface_height) / 2
        y = self._game_surface_padding_top + area_padd_top
        return y

    @property
    def board_surface_width(self):
        result = self.elements_in_game_x * self.element_width
        return result

    @property
    def board_surface_height(self):
        result = self.elements_in_game_y * self.element_height
        return result

    @property
    def board_surface_pos_x(self):
        result = self.game_surface_pos_x + (self.game_surface_width - self.board_surface_width) / 2
        return result

    @property
    def board_surface_pos_y(self):
        result = self.game_surface_pos_y + (self.game_surface_height - self.board_surface_height) / 2
        return result

    @property
    def element_height(self) -> int:
        value = self.game_surface_height / self.elements_in_game_x
        return value

    @property
    def element_width(self) -> int:
        value = self.game_surface_height / self.elements_in_game_x
        return value
    
    @property
    def board_font_name(self) -> str:
        value = self._board_font_name
        return value

    @property
    def board_font_size(self) -> int:
        value = self._board_font_size
        return value

    @board_font_size.setter
    def board_font_size(self, value: int):
        self._board_font_size = value

    @property
    def board_font_color(self) -> str:
        value = self._board_font_color
        return value

    @property
    def selection_x(self) -> int:
        value = self._selection_pos_x
        return value
    
    @selection_x.setter
    def selection_x(self, value: int):
        if value > self.elements_in_game_x - 1:
            value = self.elements_in_game_x -1 
        elif value < 0:
            value = 0
        self._selection_pos_x = value

    @property
    def selection_y(self) -> int:
        value = self._selection_pos_y
        return value
    
    @selection_y.setter
    def selection_y(self, value: int):
        if value > self.elements_in_game_y - 1:
            value = self.elements_in_game_y - 1
        elif value < 0:
            value = 0
        self._selection_pos_y = value

    @property
    def game_surface_zoom_level(self) -> int:
        value = self._game_surface_zoom_level
        return value
    
    @game_surface_zoom_level.setter
    def game_surface_zoom_level(self, value: int):
        if value < 0 or value > 5:
            value = 0
        self._game_surface_zoom_level = value

    @property
    def game_level(self) -> int:
        value = self._game_level
        return value

    @game_level.setter
    def game_level(self, value: int):
        if value < 1 or value > 5:
            value = 1
        self._game_level = value

    @property
    def level_points(self) -> int:
        value = self._level_points
        return value

    @level_points.setter
    def level_points(self, value: int):
        if value < 5 or value > 16:
            value = 12
        self._level_points = value




