from vkbottle import BaseStateGroup


class PickingState(BaseStateGroup):
    PICKING_GROUP = 'PICKING_GROUP'

    def __repr__(self):
        return str(self.PICKING_GROUP)