class Plane:
    def __init__(self, logger):
        self.logger = logger
        self.planes = []
        self.changeMap = False
        self.messagesToSend = None

    def get_players_object(self, players_object):
        self.players = players_object


    def get_commands_object(self, commands_object):
        self.commands = commands_object

    def on_changeMap(self):
        for sublist in self.planes:
            sublist[7] = True
            sublist[9] = False
        self.changeMap = True


    def check_if_all_clients_have_joined(self):
        for sublist in self.planes:
            if sublist[7] is True:
                return False
        return True





    def add_or_check(self, nickname, plane, red_perk, green_perk, blue_perk, ace, level):
        if nickname is None:
            self.logger.info("Detected and ignored NoneType nickname in planes list")
            return None
        elif self.players.check_nickname_existence(nickname) is False:
            self.logger.info("Detected and ignored unknown nickname in planes list")
            return None
        for sublist in self.planes:
            if nickname == sublist[0]:
                if self.changeMap is True and sublist[7] is True:
                    sublist[7] = False
                    self.logger.info("Ignoring {}'s perkless loopy!".format(nickname))
                    return "perkless"
                elif self.changeMap is True and sublist[7] is False and sublist[9] is False and self.messagesToSend is not None:
                    self.commands.Multiple_Whispers(nickname, self.messagesToSend)
                    sublist[9] = True
                    if self.check_if_all_clients_have_joined() is True:
                        self.changeMap = False
                        self.messagesToSend = None
                        self.logger.info("All clients are in the server after changeMap")
                elif self.changeMap is True and self.messagesToSend is None:
                    if self.check_if_all_clients_have_joined() is True:
                        self.changeMap = False
                        self.logger.info("All clients are in the server after changeMap")
                if sublist[8] is True:
                    sublist[8] = False
                    sublist[0] = nickname
                    sublist[1] = plane
                    sublist[2] = red_perk
                    sublist[3] = green_perk
                    sublist[4] = blue_perk
                    sublist[5] = ace
                    sublist[6] = level
                    return "add"
                else:
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
                    return plane_change, red_perk_change, green_perk_change, blue_perk_change, ace_change, level_change
        self.planes.append([nickname, plane, red_perk, green_perk, blue_perk, ace, level, False, True, False])
        self.logger.info("{}'s player info are added to plane's list".format(nickname))
        return "add"



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


    def get_level_and_ace(self, nickname):
        for sublist in self.planes:
            if nickname == sublist[0]:
                return sublist[6], sublist[5]


    def get(self, nickname):
        for sublist in self.planes:
            if nickname == sublist[0]:
                plane = sublist[1]
                red_perk = sublist[2]
                green_perk = sublist[3]
                blue_perk = sublist[4]
                if red_perk == "Config Random Red":
                    return "Custom Random"
                elif red_perk == "Random Red":
                    return  "Full Random"
                self.logger.info("Got and returning {}'s player info:\nPlane = {}, Red perk = {}, Green perk: {}, Blue perk: {}".format(nickname, plane, red_perk, green_perk, blue_perk))
                return plane, red_perk, green_perk, blue_perk






class PlanePosition:
    def __init__(self, logger):
        self.logger = logger
        self.plane_positions = []
        self.lobby_loaded = False


    def add_or_check(self, decoded):
        for row in decoded['positionByPlayer']:
            x, y = decoded['positionByPlayer'][row].split(',')
            for sublist in self.plane_positions:
                if row == sublist[0]:
                    sublist[1] = (int(x), int(y))
                    return
            self.plane_positions.append([int(row), (int(x), int(y))])
            break





    def remove(self, playerId):
        for sublist in self.plane_positions:
            if playerId == sublist[0]:
                self.plane_positions.remove(sublist)
                break




    def GetPosition(self, playerId):
        for sublist in self.plane_positions:
            if sublist[0] == playerId:
                self.logger.info("Position found and returned: {}".format(sublist[1]))
                return sublist[1]










class Player:
    def __init__(self, logger, plane_object):
        self.logger = logger
        self.players = []
        self.plane_object = plane_object
        self.lobby_loaded = False

    def get_game_object(self, game_object):
        self.game = game_object

    def get_commands_object(self, commands_object):
        self.commands = commands_object

    def get_perm_object(self, permissions):
        self.permissions = permissions

    def get_number_of_players(self):
        return len(self.players)


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


    def check_nickname_existence(self, nickname):
        for sublist in self.players:
            if nickname == sublist[0]:
                return True
        return False



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
        if len(self.players) == 0 and self.game.current_mode != "lobby":
            self.commands.ChangeMap("lobby_sta")
            self.lobby_loaded = True
            self.permissions.state = True
            self.logger.info("No-one is now in the server, map is changed to the lobby and mode is set to teachers and newbies only!")


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


    def vapor_from_id(self, playerId):
        for sublist in self.players:
            if playerId == sublist[2]:
                return sublist[1]


    def vapor_from_nickname(self, nickname):
        for sublist in self.players:
            if nickname == sublist[0]:
                return sublist[1]


    def return_all_nicknames(self):
        return [player[0] for player in self.players]

    def get_level_and_ace(self, playerId):
        nickname = self.nickname_from_id(playerId)
        return self.plane_object.get_level_and_ace(nickname)

    def get_planes(self, nickname):
        try:
            plane, red_perk, green_perk, blue_perk = self.plane_object.get(nickname)
            return "You are using a nice {} with {}, {} and ofc {}".format(plane, red_perk, green_perk, blue_perk)
        except ValueError:
            return "You are {}".format(self.plane_object.get(nickname))
