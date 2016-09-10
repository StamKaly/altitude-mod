class Handler:
    def __init__(self, logger, commands_object, plane_object, players_object):
        self.logger = logger
        self.commands = commands_object
        self.planes = plane_object
        self.players = players_object
        self.pressE = "Press E when dead to edit your plane."


    def on_planeChange(self, nickname, plane):
        if plane == "Loopy":
            #self.commands.Whisper(nickname, "The Loopy is the fastest and most agile plane of all the planes!")
            return


    def on_redPerkChange(self, nickname, redPerk):
        if redPerk == "Heavy Cannon":
            #self.commands.Whisper(nickname, "Heavy Cannon, which you will also hear as sniper, is a very powerful weapon!")
            return



    def on_greenPerkChange(self, nickname, greenPerk):
        if greenPerk == "Flexible Wings":
            #self.commands.Whisper(nickname, "Flexible Wings apart from making you turn easier, it also makes you go faster!")
            return


    def on_bluePerkChange(self, nickname, bluePerk):
        if bluePerk == "Ultracapacitor":
            #self.commands.Whisper(nickname, "Ultracapacitor increases your maximum energy!")
            return


    def on_aceChange(self, nickname, ace):
        if ace == 1:
            self.commands.Multiple_Whispers(nickname, ["You have now become ace Rank 1! Congratulations!",
                                                       "Make sure you start playing ladder now that you are pro",
                                                       "Just go and read the rules at planeball.com/ranked/about"])


    def on_levelChange(self, nickname, level, ace):
        # Special thanks to Nick for letting me know when do you unlock each perk/plane
        # and of course Xalri for making level changes tracking possible!
        if ace == 0:
            # Green perks
            if level == 2:
                self.commands.Multiple_Whispers(nickname, ["You now have Rubberized Hull, or rubber for short,",
                                                           "it increases your acceleration as well as it makes it",
                                                           "easier for you to recover from Stalls!"])
            elif level == 13:
                self.commands.Multiple_Whispers(nickname, ["It's time for you to take rid of that rubber and equip",
                                                           "your vehicle with Heavy Armour! It protects you from",
                                                           "most damage taken. Simply press E once dead and click ",
                                                           "your plane to edit it!"])
            elif level == 30:
                self.commands.Multiple_Whispers(nickname, ["You've just unlocked Repair Drone. Don't get too excited",
                                                           "though, it's mostly useful only for Bomber!",
                                                           "{}".format(self.pressE)])
            elif level == 50:
                self.commands.Multiple_Whispers(nickname, ["You now have Flexible Wings, an",
                                                           "easy-to-use-hard-to-master perk. Makes you go faster",
                                                           "and turn easier, but it's also easier to crash!",
                                                           "{}".format(self.pressE)])

            # Blue perks
            elif level == 8:
                self.commands.Multiple_Whispers(nickname, ["You've unlocked your first and most useful Blue Perk!",
                                                           "Turbo Charger increases your energy regeneration rate",
                                                           "by 20%. {}".format(self.pressE)])

            elif level == 18:
                self.commands.Multiple_Whispers(nickname, ["You just unlocked Ultra Capacitor! Mostly recommended",
                                                           "for the last plane, miranda. It increases your maximum",
                                                           "energy by 35%. {}".format(self.pressE)])

            elif level == 41:
                self.commands.Multiple_Whispers(nickname, ["You now have Reverse Thrust. It lets you go backwards,",
                                                           "but be careful with crashing! Hold Break button to use it.",
                                                           "{}".format(self.pressE)])

            elif level == 60:
                self.commands.Multiple_Whispers(nickname, ["You've unlocked Ace Instincts! You now are probably really",
                                                           "excited to see what that last perk is, it increases the",
                                                           "effects of the Veteran Bars by 50%. For Veteran Bars",
                                                           "explanation use the command /veteranBars"])


            # Red perks and planes

            # Loopy
            elif level == 24:
                self.commands.Multiple_Whispers(nickname, ["You now have Double Fire for Loopy! You can go and take",
                                                           "that from selecting the Loopy from the second line.",
                                                           "The second line of planes allows you to have more setups"])

            elif level == 44:
                self.commands.Multiple_Whispers(nickname, ["You've unlocked Acid Bomb for Loopy! It replaces EMP",
                                                           "and the affected plane will temporarily continue to lose",
                                                           "small amounts of health!"])


            # Bomber
            elif level == 6:
                self.commands.Multiple_Whispers(nickname, ["You've unlocked Bomber! The Bomber is one of the two",
                                                           "'heavy'-class planes and is a key instrument in",
                                                           "maintaining map control!"])

            elif level == 27:
                self.commands.Multiple_Whispers(nickname, ["You unlocked Bombs for Bomber! It replaces Tail Gun",
                                                           "with Bombs that can be used above the enemy for an",
                                                           "easy kill! {}".format(self.pressE)])


            elif level == 47:
                self.commands.Multiple_Whispers(nickname, ["You have unlocked Flak Tail Gun for Bomber! It",
                                                           "is a tail cannon that does a great deal of damage to",
                                                           "your opponent."])



            # Explodet
            elif level == 11:
                self.commands.Multiple_Whispers(nickname, ["You just unlocked Explodet! Also known as whale.",
                                                           "It has the most health of any plane and both it's",
                                                           "primary and secondary weapons cause explosive damage."])

            elif level == 32:
                self.commands.Multiple_Whispers(nickname, ["Congratulations! You have unlocked Thermobarics for",
                                                           "Explodet! It replaces the normal rocket and it lets",
                                                           "you change the direction of the opponent's plane to",
                                                           "wherever you detonate the thermobaric rocket!"])

            elif level == 53:
                self.commands.Multiple_Whispers(nickname, ["You have unlocked Remote Mine for Explodet! It",
                                                           "replaces the normal mine with a remote one and",
                                                           "let's you detonate it whenever you want!"])



            # Biplane
            elif level == 16:
                self.commands.Multiple_Whispers(nickname, ["You unlocked Biplane! It is perfect for an instant",
                                                           "kill with its two weapons being fired simultaneously!",
                                                           "{}".format(self.pressE)])

            elif level == 35:
                self.commands.Multiple_Whispers(nickname, ["You have unlocked Recoilless Gun for Biplane! It",
                                                           "allows you to fire without losing speed as well as",
                                                           "your bullets make more damage to the enemy!"])

            elif level == 56:
                self.commands.Multiple_Whispers(nickname, ["Congratulations! You have unlocked Heavy Cannon for",
                                                           "Biplane. It is also known as sniper since it can make",
                                                           "a huge damaga to 1-3 planes at a time!"])


            # Miranda
            elif level == 21:
                self.commands.Multiple_Whispers(nickname, ["You now have Miranda! Also known as randa. A hard to",
                                                           "master plane with its masters being the most powerful",
                                                           "among the planes! {}".format(self.pressE)])


            elif level == 38:
                self.commands.Multiple_Whispers(nickname, ["You have unlocked Lazer for Miranda! In order to use",
                                                           "it, you need to full charge the primary weapon."
                                                           "{}".format(self.pressE)])

            elif level == 58:
                self.commands.Multiple_Whispers(nickname, ["Congratulations! You have unlocked Time Anchor for",
                                                           "Miranda! It replaces its secondary ability to turn back",
                                                           "with the ability to go your plane back to a position",
                                                           "you've gone through!"])







    def on_setup_change(self, nickname, plane, redPerk, greenPerk, bluePerk, ace, level, plane_name, redPerk_name,
                        greenPerk_name, bluePerk_name, ace_number, level_number):
        if plane is True and redPerk_name != "Config Random Red" and redPerk_name != "Random Red":
            self.on_planeChange(nickname, plane_name)
        if redPerk is True and redPerk_name != "Config Random Red" and redPerk_name != "Random Red":
            self.on_redPerkChange(nickname, redPerk_name)
        if greenPerk is True and greenPerk_name != "Config Random Green" and greenPerk_name != "Random Green":
            self.on_greenPerkChange(nickname, greenPerk_name)
        if bluePerk is True and bluePerk_name != "Config Random Blue" and bluePerk_name != "Random Blue":
            self.on_bluePerkChange(nickname, bluePerk_name)
        if ace is True:
            self.on_aceChange(nickname, ace_number)
        if level is True:
            self.on_levelChange(nickname, level_number, ace_number)
        self.logger.info("{}'s player info changes are parsed".format(nickname))







    def parse(self, decoded):
        nickname = self.players.nickname_from_id(decoded['player'])
        plane = decoded['plane']
        redPerk = decoded['perkRed']
        greenPerk = decoded['perkGreen']
        bluePerk = decoded['perkBlue']
        ace = decoded['aceRank']
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