import json
import tkinter.messagebox
from .stone import MagicStone
import os


class JsonManager:
    """
    Class for loading and changing json object
    """

    def __init__(self, path):
        self.stones = []
        self.path_to_file = path

    def open_json(self) -> bool:
        """
        Opens json, if success return True
        :return:
        """
        success = False
        try:
            with open(self.path_to_file, 'r') as f:
                self.json = json.load(f)
                success = True
        except:
            pass
        return success

    def save_json(self, stones) -> None:
        """
        Saves changes to json_file
        :param stones: new stones
        :return:
        """
        self.replace_values(stones)
        try:
            with open(self.path_to_file, 'w') as f:
                json.dump(self.json, f, indent=4)
                tkinter.messagebox.showinfo('Success!', 'Successfully saved the file.')
        except:
            pass

    def replace_values(self, stones) -> None:
        """
        Replace values in json by stones
            'I used stones to replace the stones'
        :param stones: new stones
        :return:
        """
        self.stones = stones
        for stone in self.stones:
            attrs = stone.get_path()
            self.json[attrs[0]][attrs[1]][attrs[2]] = attrs[3]

    def get_stones(self) -> list:
        """
        Gets all stones (MAGIC STONES) from json file
        :return:
        """
        for task, algorithms in self.json.items():
            for algorithm, attributes in algorithms.items():
                for attribute, value in attributes.items():
                    try:
                        stone = MagicStone(task, algorithm, attribute, float(value))
                        self.stones.append(stone)
                    except:
                        pass
        return self.stones

    @staticmethod
    def create_file(PATH) -> None:
        """
        Create 'temp.json'
        :param PATH: path to 'temp.json
        :return:
        """
        with open(PATH, 'w+') as f:
            f.write('')

    @staticmethod
    def remove_file(PATH) -> None:
        """
        Removes file at the end of program work
        :param PATH: path to 'temp.json'
        :return:
        """
        os.remove(PATH)
