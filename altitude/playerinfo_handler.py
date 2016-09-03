class Handler:
    def __init__(self, logger, commands_object, plane_object, players_object):
        self.logger = logger
        self.commands = commands_object
        self.planes = plane_object
        self.players = players_object


    def on_planeChange(self, nickname, plane):
        if plane == "Loopy":
            self.commands.Whisper(nickname, "The Loopy is the fastest and most agile plane of all the planes!")


    def on_redPerkChange(self, nickname, redPerk):
        if redPerk == "Heavy Cannon":
            self.commands.Whisper(nickname, "Heavy Cannon, which you will also hear as sniper, is a very powerful weapon!")



    def on_greenPerkChange(self, nickname, greenPerk):
        if greenPerk == "Flexible Wings":
            self.commands.Whisper(nickname, "Flexible Wings apart from making you turn easier, it also makes you go faster!")


    def on_bluePerkChange(self, nickname, bluePerk):
        if bluePerk == "Ultracapacitor":
            self.commands.Whisper(nickname, "Ultracapacitor increases your maximum energy!")


    def on_aceChange(self, nickname, ace):
        if ace == 1:
            self.commands.Multiple_Whispers(nickname, ["You have now become ace Rank 1! Congratulations!",
                                                       "Make sure you start playing ladder now that you are pro",
                                                       "Just go and read the rules at planeball.com/ranked/about"])


    def on_levelChange(self, nickname, level):
        if level == 8:
            self.commands.Whisper(nickname, "You have unlocked a new blue perk called Turbo Charger, once you are dead press E to edit your plane!")



    def on_setup_change(self, nickname, plane, redPerk, greenPerk, bluePerk, ace, level, plane_name, redPerk_name,
                        greenPerk_name, bluePerk_name, ace_number, level_number):
        if plane is True:
            self.on_planeChange(nickname, plane_name)
        if redPerk is True:
            self.on_redPerkChange(nickname, redPerk_name)
        if greenPerk is True:
            self.on_greenPerkChange(nickname, greenPerk_name)
        if bluePerk is True:
            self.on_bluePerkChange(nickname, bluePerk_name)
        if ace is True:
            self.on_aceChange(nickname, ace_number)
        if level is True:
            self.on_levelChange(nickname, level_number)
        self.logger.info("{}'s player info changes are parsed".format(nickname))







    def parse(self, decoded):
        nickname = self.players.nickname_from_id(decoded['player'])
        plane = decoded['plane']
        redPerk = decoded['perkRed']
        greenPerk = decoded['perkGreen']
        bluePerk = decoded['perkBlue']
        ace = decoded['ace']
        level = decoded['level']
        add_or_check = self.planes.add_or_check(nickname, plane, redPerk, greenPerk, bluePerk, ace, level)
        if add_or_check == "add":
            return
        elif add_or_check == "perkless":
            return
        elif decoded['leaving'] is not True:
            self.logger.info("Parsing changes for {}'s player info".format(nickname))
            plane_change, red_perk_change, green_perk_change, blue_perk_change, ace_change, level_change = add_or_check
            self.on_setup_change(nickname, plane_change, red_perk_change, green_perk_change, blue_perk_change,
                                 ace_change, level_change, plane, redPerk, greenPerk, bluePerk, ace, level)
