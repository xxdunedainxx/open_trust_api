class ModelAttributeDoesNotExist(Exception):
    def __init__(self, attribute: str, obj: str):

        super().__init__(f"attribute {attribute} does not exist on object {obj}")