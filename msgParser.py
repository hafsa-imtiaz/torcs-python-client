class MsgParser(object):
    '''
    A parser for received UDP messages and building UDP messages
    '''

    def __init__(self):
        '''Constructor'''
        pass
        
    def parse(self, str_sensors):
        '''Return a dictionary with tags and values from the UDP message'''

        # Decode bytes to string if necessary
        if isinstance(str_sensors, bytes):
            str_sensors = str_sensors.decode('utf-8').strip('\x00')

        if not isinstance(str_sensors, str):
            raise ValueError(f"Expected string but got {type(str_sensors)}: {str_sensors}")

        sensors = {}
        b_open = str_sensors.find('(')

        while b_open >= 0:
            b_close = str_sensors.find(')', b_open)
            if b_close >= 0:
                substr = str_sensors[b_open + 1 : b_close].strip()
                items = substr.split()

                if len(items) < 2:
                    print(f"Warning: Problem parsing substring: '{substr}'")
                else:
                    try:
                        # Convert numerical values to float if possible
                        value = [float(x) if x.replace('.', '', 1).isdigit() else x for x in items[1:]]
                        sensors[items[0]] = value
                    except ValueError:
                        print(f"Error: Unable to convert values in '{substr}'")
                        sensors[items[0]] = items[1:]  # Store as strings if conversion fails
                
                b_open = str_sensors.find('(', b_close)
            else:
                print(f"Error: Mismatched parentheses in sensor string: {str_sensors}")
                return None
        
        return sensors


    def stringify(self, dictionary):
        '''Build a UDP message from a dictionary'''
        if not isinstance(dictionary, dict):
            raise ValueError("Expected a dictionary for string conversion.")

        msg = ''

        for key, value in dictionary.items():
            if isinstance(value, list) and value:
                msg += f"({key} " + ' '.join(map(str, value)) + ')'
            else:
                print(f"Warning: Skipping key '{key}' due to invalid value: {value}")

        return msg
