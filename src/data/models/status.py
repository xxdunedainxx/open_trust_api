from conf.conf import RESERVED_STATUS_NAMES
from src.util.errorFactory.status_errors import StatusDoesNotExist
class status:

    def __init__(self,status_id,name,when_created,sprite):
        self.id=status_id
        self.name=name
        self.when_created=when_created
        self.sprite=sprite

    def serialize(self):
        return {
            'id' : self.id,
            'name' : self.name,
            'when_created' : self.when_created,
            'sprite' : self.sprite
        }

def serve_sprite_path(id,db):
    get_sprite=db.executeQuery("SELECT status_sprite from status WHERE status_id=%s",paramatized=(id))

    if get_sprite != None:
        return get_sprite[0][0]
    else:
        raise StatusDoesNotExist(f"{id} does not exist")


# TODO :: SCAN FILE MAKE SURE NOT MALICIOUS
# TODO :: if name is reserved, or already in use then dont allow creation
def create_new_sprite(name, sprite_file):
    pass

# TODO :: do not allow removal of sprites in range of reserved statuses
def remove_status(id,db):
    pass
