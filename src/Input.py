import keyboard

class Input:
    """
    Controlled character input by keyboard

    Methods:
        public:
            integer (static)
            string (static)
    """
    
    @classmethod
    def integer(cls, message: str, max_digits: int, min_digits = 1, has_sign = False) -> int:
        """
        Positive and negative numbers entry

        Args:
            message (str): _description_ String to print before to input numbers
            max_digits (int): _description_ Number of maximum digits to enter
            min_digits (int, optional): _description_. Defaults to 1. Number of minimum digits to enter
            has_sign (bool, optional): _description_. Defaults to False. Enables or disables negative sign input

        Returns:
            int: _description_ Number entered by keyboard
        """
        print(message, end='', flush=True)

        has_pressed_enter = False
        value = str()
        key_press = str()

        while not has_pressed_enter or len(value) < min_digits:
            key_press = str(keyboard.read_key(suppress=True))
            keyboard.read_key(suppress=True)

            if key_press.isdigit() and len(value) < max_digits:
                value += key_press
                print(key_press, end='', flush=True)
            elif key_press == '-' and len(value) == 0 and has_sign:
                max_digits += 1
                min_digits += 1
                value += key_press
                print(key_press, end='', flush=True)
            elif key_press == 'backspace' and len(value) > 0:
                if value[-1] == '-':
                    max_digits -= 1
                    min_digits -= 1
                value = value[:-1]
                print('\b \b', end='', flush=True)

            has_pressed_enter = key_press == 'enter'

        print(flush=True)

        return int(value)
    
    @classmethod
    def floating(cls, message: str, max_digits: int, max_decimals: int, min_digits = 1, min_decimals = 1, has_sign = False) -> float:
        """
        Positive and negative numbers entry

        Args:
            message (str): _description_ String to print before to input numbers
            max_digits (int): _description_ Number of maximum digits to enter
            min_digits (int, optional): _description_. Defaults to 1. Number of minimum digits to enter
            has_sign (bool, optional): _description_. Defaults to False. Enables or disables negative sign input

        Returns:
            int: _description_ Number entered by keyboard
        """
        print(message, end='', flush=True)

        has_pressed_enter = False
        value = str()
        key_press = str()

        while not has_pressed_enter or len(value) <= min_digits + min_decimals:
            key_press = str(keyboard.read_key(suppress=True))
            keyboard.read_key(suppress=True)

            if key_press.isdigit() and ((len(value) < max_digits and '.' not in value) or len(value) - value.index('.') <= max_decimals and '.' in value):
                value += key_press
                print(key_press, end='', flush=True)
            elif key_press == '-' and len(value) == 0 and has_sign:
                max_digits += 1
                min_digits += 1
                value += key_press
                print(key_press, end='', flush=True)
            elif key_press == '.' and '.' not in value and min_decimals > 0:
                value += key_press
                print(key_press, end='', flush=True)
            elif key_press == 'backspace' and len(value) > 0:
                if value[-1] == '-':
                    max_digits -= 1
                    min_digits -= 1

                value = value[:-1]

                print('\b \b', end='', flush=True)

            has_pressed_enter = key_press == 'enter'

        print(flush=True)

        return float(value)
    
    @classmethod
    def string(cls, message: str, is_char_allowed, max_chars: int, min_chars = 1) -> str:
        """
        Developer-specified character input

        Args:
            message (str): _description_ String to print before input characters
            max_chars (int): _description_ Number of maximum characters to enter
            is_char_allowed (bool): _description_ Function pointer specifying the allowed characters.
                Example (lowercase):
                is_char_allowed = lambda char: char >= 'a' and char <= 'z'
            min_chars (int, optional): _description_. Defaults to 1. Number of minimum characters to enter

        Returns:
            str: _description_ Characters entered by keyboard
        """
        print(message, end='', flush=True)

        has_pressed_enter = False
        string = str()
        key_press = str()

        while not has_pressed_enter or len(string) < min_chars:
            key_press = str(keyboard.read_key(suppress=True))
            keyboard.read_key(suppress=True)

            if key_press == 'space':
                key_press = ' '

            if is_char_allowed(key_press) and len(string) < max_chars:
                print(key_press, end='', flush=True)
                string += key_press
            elif key_press == 'backspace' and len(string) > 0:
                string = string[:-1]
                print('\b \b', end='', flush=True)

            has_pressed_enter = key_press == 'enter'

        print(flush=True)

        return string