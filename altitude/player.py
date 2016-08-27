class Plane:
    def __init__(self):
        self.planes = []


    def add_or_check(self, playerId, plane, red_perk, green_perk, blue_perk, ace, level):
        for sublist in self.planes:
            if playerId != sublist[0]:
                continue
            if playerId == sublist[0]:
                if plane != sublist[1]:
                    plane_change = True
                    sublist[1] = plane
                else:
                    plane_change = False
                if red_perk != sublist[2]:
                    red_perk_change = True
                    sublist[2] = red_perk
                else:
                    red_perk_change = False
                if green_perk != sublist[3]:
                    green_perk_change = True
                    sublist[3] = green_perk
                else:
                    green_perk_change = False
                if blue_perk != sublist[4]:
                    blue_perk_change = True
                    sublist[4] = blue_perk
                else:
                    blue_perk_change = False
                if ace != sublist[5]:
                    ace_change = True
                    sublist[5] = ace
                else:
                    ace_change = False
                if level != sublist[6]:
                    level_change = True
                    sublist[6] = level
                else:
                    level_change = False
                return "plane_change={},red_perk_change={},green_perk_change={},blue_perk_change={},ace_change={},level_change={}".format(plane_change, red_perk_change, green_perk_change, blue_perk_change, ace_change, level_change)
        self.planes.append([playerId, plane, red_perk, green_perk, blue_perk, ace, level])

    def remove(self, playerId):
        for sublist in self.planes:
            if playerId == sublist[0]:
                self.planes.remove(sublist)
                break


    def get(self, playerId):
        for sublist in self.planes:
            if playerId == sublist[0]:
                plane = sublist[1]
                red_perk = sublist[2]
                green_perk = sublist[3]
                blue_perk = sublist[4]
                return plane, red_perk, green_perk, blue_perk





class Player:
    def __init__(self, plane_object):
        self.players = []
        self.plane_object = plane_object

    def get_all_players(self, nicknames, vapors, playerIds, IPs):
        player_list = [nicknames, vapors, playerIds, IPs]
        count = 0
        for _ in range(len(nicknames)):
            player = [player[count] for player in player_list]
            for sublist in self.players:
                if player[1] == sublist[1]:
                    break
                if player[1] != sublist[1]:
                    self.players.append(player)
                    break
            count += 1


    def ace_level(self, playerId, ace, level):
        for sublist in self.players:
            if sublist[2] == playerId:
                if len(sublist) == 6:
                    sublist[-1] = level
                    sublist[-2] = ace
                if len(sublist) == 4:
                    sublist.append(ace)
                    sublist.append(level)
                break


    def add(self, nickname, vaporId, playerId, IP, ace, level):
        self.players.append([nickname, vaporId, playerId, IP, ace, level])


    def remove(self, nickname):
        for sublist in self.players:
            if nickname == sublist[0]:
                self.players.remove(sublist)
                self.remove_from_planes(sublist[2])
                break

    def remove_from_planes(self, playerId):
        for sublist in self.players:
            if playerId == sublist[2]:
                self.plane_object.remove(playerId)
                break

    def nickname_from_vapor(self, vaporId):
        for sublist in self.players:
            if vaporId == sublist[1]:
                return sublist[0]


    def id_from_vapor(self, vaporId):
        for sublist in self.players:
            if vaporId == sublist[1]:
                return sublist[2]


    def return_all_nicknames(self):
        nicknames = [player[0] for player in self.players]
        return nicknames


    def get_planes(self, playerId):
        plane, red_perk, green_perk, blue_perk = self.plane_object.get(playerId)
        return "You are using a nice {} with {}, {} and ofc {}".format(plane, red_perk, green_perk, blue_perk)