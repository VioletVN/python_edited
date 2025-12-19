class Item:
    def use(self, player):
        pass
class Coin(Item):
    def use(self, player):
        player.coins += 1
class Mushroom(Item):
    def use(self, player):
        player.lives += 1