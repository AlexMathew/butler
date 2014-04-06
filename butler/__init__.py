__version__ = "0.8a"
__author__ = "Anoop Thomas Mathew"
__license__ = "BSD"
__contact__ = "atmb4u at gmail dot com"


class Butler(object):
    def __init__(self, obj):
        """
        Initiates with the list or dict object obj
        """
        self.obj = obj

    def get(self, path):
        """
        Grab values inside nested dict and list if available, else returns None
        Returns None if looking up in string.
        keys: A list of names or ids
        >>> data1 = Butler({"key": "value"})
        >>> data1.get(["key"])
        'value'
        >>> data2 = Butler([1, 2, 4, 5, [10, 20, 30, 40, 50]])
        >>> data2.get([4, 3])
        40
        >>> data2.get([4, 9])

        >>> data3 = Butler("Hello world")
        >>> data3.get([6])

        Usage:

        """
        return_obj = self.obj
        for key in path:
            try:
                if type(return_obj) in [list, dict]:
                    return_obj = return_obj[key]
                else:
                    return None
            except LookupError:
                return None
        return return_obj

    def path_exists(self, path):
        """

        >>> data = {'a':1, 'b':2, 'c': {'d': 4, 'e': 5, 'f': [6, 7, 8], 'g':[{'h': 8, 'i': 9, 'j': 10}, {'a':11,
        ... 'b': 12, 'c': 13}]}, 'n': [14, 15, 16, 17, 18]}

        >>> quick = Butler(data)

        >>> quick.path_exists(['c','g',0,'k'])
        False
        >>> quick.path_exists(['c','g',0,'j'])
        True
        """
        if self.get(path):
            return True
        else:
            return False

    def flatten(self, sub_dict=None, output=None):
        """
        Flattens the sub_dict argument.
        Internal API used with find and findall functions.
        >>> data = {'a':10, 'b':[{'c':11, 'd': 13}, {'d':14, 'e':15}]}

        >>> quick = Butler(data)

        >>> quick.flatten(data)
        [('a', 10), ('c', 11), ('d', 13), ('e', 15), ('d', 14), ('b', [{'c': 11, 'd': 13}, {'e': 15, 'd': 14}])]
        """
        if not sub_dict:
            sub_dict = self.obj
        if not output:
            output = []
        for key in sub_dict:
            if isinstance(sub_dict[key], dict):
                self.flatten(sub_dict[key], output)
            if isinstance(sub_dict[key], list):
                for sub_dic in sub_dict[key]:
                    if isinstance(sub_dic, dict):
                        self.flatten(sub_dic, output)
            output.append((key, sub_dict[key],))
        return output

    def findall(self, key, find=False):
        """
        >>> data = {'a':1, 'b':2, 'c': {'d': 4, 'e': 5, 'f': [6, 7, 8], 'g':[{'h': 8, 'i': 9, 'j': 10}, {'a':11,
        ... 'b': 12, 'c': 13}]}, 'n': [14, 15, 16, 17, 18]}

        >>> quick = Butler(data)

        >>> quick.findall('a')
        [1, 11]
        >>> new_list = [1, 2, 3, 4, [1,2,3,4], 5]

        >>> quick1 = Butler(new_list)

        >>> quick1.findall(4)
        [1, 2, 3, 4]
        """
        return_list = []
        if isinstance(self.obj, dict):
            flat_list = self.flatten(self.obj)
            for item_key, data in flat_list:
                if item_key == key:
                    if find:  # API for find() to return the first result
                        return data
                    return_list.append(data)
        elif isinstance(self.obj, list):  # kept this to keep the API consistent across list and dict
            if len(self.obj) - 1 > key:
                return self.obj[key]
        else:
            print("findall can be used only with dict or list objects")
        return return_list

    def find(self, key):
        """
        Works only with dict,
        Input
        key: The key to be searched for

        >>> data = {'a':1, 'b':2, 'c': {'d': 4, 'e': 5, 'f': [6, 7, 8], 'g':[{'h': 8, 'i': 9, 'j': 10}, {'a':11,
        ... 'b': 12, 'c': 13}]}, 'n': [14, 15, 16, 17, 18]}

        >>> quick = Butler(data)

        >>> quick.find('a')
        1
        >>> quick.find('e')
        5
        >>> quick.find('w')

        >>> new_list = [1, 2, 3, 4, 5]

        >>> quick1 = Butler(new_list)

        >>> quick1.find(2)
        3

        """
        data = self.findall(key, find=True)
        if data:
            return data
        return None

    def key_exists(self, key):
        """
        Uses find function to see if the requested key is in the dictionary
        Returns: True or False

        >>> data = {'a':1, 'b':2, 'c': {'d': 4, 'e': 5, 'f': [6, 7, 8], 'g':[{'h': 8, 'i': 9, 'j': 10}, {'a':11,
        ... 'b': 12, 'c': 13}]}, 'n': [14, 15, 16, 17, 18]}

        >>> quick = Butler(data)

        >>> quick.key_exists('a')
        True
        >>> quick.key_exists('w')
        False
        """
        if self.find(key):
            return True
        else:
            return False