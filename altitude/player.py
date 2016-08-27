class Plane:
    def __init__(self, logger):
        self.logger = logger
        self.planes = []


    def add_or_check(self, nickname, plane, red_perk, green_perk, blue_perk, ace, level):
        for sublist in self.planes:
            if nickname is None:
                return
            if nickname != sublist[0]:
                continue
            if nickname == sublist[0]:
                self.logger.info("Tracking changes for {}'s player info".format(nickname))
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
                changes = "plane_change={},red_perk_change={},green_perk_change={},blue_perk_change={},ace_change={},level_change={}".format(plane_change, red_perk_change, green_perk_change, blue_perk_change, ace_change, level_change)
                self.logger.info("Changes for {}'s player info are tracked: {}".format(nickname, changes))
                return changes
        self.planes.append([nickname, plane, red_perk, green_perk, blue_perk, ace, level])
        self.logger.info("{}'s player info are added to plane's list".format(nickname))

    def remove(self, nickname):
        for sublist in self.planes:
            if nickname == sublist[0]:
                self.planes.remove(sublist)
                self.logger.info("{}'s player info are removed from planes list".format(nickname))
                break

    def nickname_change(self, oldNickname, newNickname):
        for sublist in self.planes:
            if oldNickname == sublist[0]:
                sublist[0] = newNickname
                self.logger.info("{}'s nickname changed to {} in planes list".format(oldNickname, newNickname))
                break

    def get(self, nickname):
        for sublist in self.planes:
            if nickname == sublist[0]:
                plane = sublist[1]
                red_perk = sublist[2]
                green_perk = sublist[3]
                blue_perk = sublist[4]
                self.logger.info("Got and returning {}'s player info:\nPlane = {}, Red perk = {}, Green perk: {}, Blue perk: {}".format(nickname, plane, red_perk, green_perk, blue_perk))
                return plane, red_perk, green_perk, blue_perk





class Player:
    def __init__(self, logger, plane_object):
        self.logger = logger
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
        self.logger.info("All players in server added to players list")



    def add(self, nickname, vaporId, playerId, IP):
        self.players.append([nickname, vaporId, playerId, IP])
        self.logger.info("{} is added to players list".format(nickname))


    def remove(self, nickname):
        for sublist in self.players:
            if nickname == sublist[0]:
                self.players.remove(sublist)
                self.logger.info("{} is removed from players list".format(nickname))
                self.plane_object.remove(nickname)
                break


    def nickname_change(self, oldNickname, newNickname):
        for sublist in self.players:
            if oldNickname == sublist[0]:
                sublist[0] = newNickname
                self.logger.info("{}'s nickname changed to {} in players list".format(oldNickname, newNickname))
                self.plane_object.nickname_change(oldNickname, newNickname)
                break


    def nickname_from_vapor(self, vaporId):
        for sublist in self.players:
            if vaporId == sublist[1]:
                return sublist[0]


    def id_from_vapor(self, vaporId):
        for sublist in self.players:
            if vaporId == sublist[1]:
                return sublist[2]


    def nickname_from_id(self, playerId):
        for sublist in self.players:
            if playerId == sublist[2]:
                return sublist[0]

    def return_all_nicknames(self):
        nicknames = [player[0] for player in self.players]
        return nicknames


    def get_planes(self, nickname):
        plane, red_perk, green_perk, blue_perk = self.plane_object.get(nickname)
        return "You are using a nice {} with {}, {} and ofc {}".format(plane, red_perk, green_perk, blue_perk)