class ConfigAttributeDoesNotExist(Exception):
    def __init__(self, config_item: str ):
        super().__init__(f"{config_item} not present. This item is required!")