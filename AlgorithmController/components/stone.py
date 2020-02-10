class MagicStone:

    """
    Noone know why it's called like that
     ¯\_(ツ)_/¯
     But it is task-json communication manager
    """

    def __init__(self, task, algorithm, attribute, value):
        self.task = task
        self.algorithm = algorithm
        self.attribute = attribute
        self.value = value

    def __repr__(self) -> str:
        return str(f'<MagicStone object> {self.task}, {self.algorithm}, {self.attribute}, {self.value}')

    def get_value(self) -> float:
        return self.value

    def set_value(self, value) -> None:
        self.value = value

    def get_path(self) -> tuple:
        """
        Returns path to saving changes
        :return:
        """
        path = (self.task, self.algorithm, self.attribute, self.value)
        return path
