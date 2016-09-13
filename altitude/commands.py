class Commands:
    def __init__(self, logger, players_object, port, commands_file_location):
        self.logger = logger
        self.players = players_object
        self.commands_file = commands_file_location
        self.console = "{},console,".format(port)


    def write_command(self, cmd):
        with open(self.commands_file, "a") as commands:
            commands.write(cmd)


    def aquote(self, nickname):
        return nickname.replace('\\', '\\\\').replace('"', '\\"')


    def StartTournament(self):
        cmd = '{}startTournament\n'.format(self.console)
        self.write_command(cmd)
        self.logger.info("Tournament has now started")


    def StopTournament(self):
        cmd = '{}stopTournament\n'.format(self.console)
        self.write_command(cmd)
        self.logger.info("Tournament is now stopped")


    def AddBan(self, IP, duration, unit_time, reason):
        ip, _ = IP.split(":")
        cmd = '{}addBan {} {} {} "{}"\n'.format(self.console, ip, duration, unit_time, reason)
        self.write_command(cmd)


    def AddChatBlock(self, vapor, block_type, duration, unit_time, reason):
        cmd = '{}addChatBlock {} {} {} {} "{}"\n'.format(self.console, vapor, block_type, duration,
                                                  unit_time, reason)
        self.write_command(cmd)
        self.logger.info("A chat block ban has been added to {} for {} {} in {}".format(vapor, duration,
                                                                                        unit_time, block_type))

    def ChatBlock(self, nickname, block_type, duration, unit_time, reason):
        cmd = '{}chatBlock "{}" {} {} {} "{}"\n'.format(self.console, self.aquote(nickname), block_type, duration,
                                                  unit_time, reason)
        self.write_command(cmd)
        self.logger.info("A chat block ban has been added to {} for {} {} in {}".format(nickname, duration,
                                                                                        unit_time, block_type))


    def RemoveChatBlock(self, vapor, block_type):
        cmd = "{}removeChatBlock {} {}\n".format(self.console, vapor, block_type)
        self.write_command(cmd)
        self.logger.info("A chat block had been removed")


    def ChangeServer(self, nickname, IP_port, secretCode):
        cmd = '{}serverRequestPlayerChangeServer "{}" {} {}\n'.format(self.console, self.aquote(nickname), IP_port, secretCode)
        self.write_command(cmd)


    def Whisper(self, playerName, message):
        cmd = '{}serverWhisper "{}" "{}"\n'.format(self.console, self.aquote(playerName), message)
        self.write_command(cmd)


    def Multiple_Whispers(self, playerName, messages):
        for arg in messages:
            cmd = '{}serverWhisper "{}" "{}"\n'.format(self.console, self.aquote(playerName), arg)
            self.write_command(cmd)


    def Message(self, message):
        cmd = '{}serverMessage "{}"\n'.format(self.console, message)
        self.write_command(cmd)


    def Multiple_Messages(self, messages):
        for arg in messages:
            cmd = '{}serverMessage "{}"\n'.format(self.console, arg)
            self.write_command(cmd)


    def LogServerStatus(self):
        cmd = '{}logServerStatus\n'.format(self.console)
        self.write_command(cmd)


    def LogPlanePositions(self):
        cmd = '{}logPlanePositions\n'.format(self.console)
        self.write_command(cmd)


    def ChangeMap(self, mapName):
        cmd = '{}changeMap {}\n'.format(self.console, mapName)
        self.write_command(cmd)
        self.logger.info("Map is now changed to {}".format(mapName))



    def CameraScale(self, camera):
        cmd = '{}testCameraViewScale {}\n'.format(self.console, camera)
        self.write_command(cmd)
        self.logger.info("Everyone's camera has now a scale of {}%".format(camera))



    def PlaneScale(self, scale):
        cmd = '{}testPlaneScale {}\n'.format(self.console, scale)
        self.write_command(cmd)
        self.logger.info("Everyone's plane has now a scale of {}%".format(scale))



    def Gravity(self, mode):
        if mode == "nothing":
            mode = 0
        elif mode == "planes":
            mode = 1
        elif mode == "powerups":
            mode = 2
        elif mode == "everything":
            mode = 3
        cmd = '{}testGravityMode {}\n'.format(self.console, mode)
        self.write_command(cmd)
        self.logger.info("Gravity now applies to {}".format(mode))



    def HealthModifier(self, health):
        cmd = '{}testHealthModifier {}\n'.format(self.console, health)
        self.write_command(cmd)
        self.logger.info("Everyone's health is now set to {}%".format(health))




    def get_team(self, team):
        if team == "left":
            return "0"
        if team == "right":
            return "1"
        if team == "spec":
            return "-1"


    def AssignTeam(self, playerName, team):
        cmd = '{}assignTeam "{}" {}\n'.format(self.console, self.aquote(playerName), self.get_team(team))
        self.write_command(cmd)
        self.logger.info("{} is moved to {} - (Non-tournament Mode)".format(playerName, team))


    def ModifyTournament(self, playerName, team):
        cmd = '{}modifyTournament "{}" {}\n'.format(self.console, self.aquote(playerName), self.get_team(team))
        self.write_command(cmd)
        self.logger.info("{} is moved to {} - (Tournament Mode)".format(playerName, team))


    def AssignEveryone(self, team):
        team_num = self.get_team(team)
        playerNames = [player[0] for player in self.players.players]
        for arg in playerNames:
            cmd = '{}assignTeam "{}" {}\n'.format(self.console, self.aquote(arg), team_num)
            self.write_command(cmd)
        self.logger.info('Everyone in server is moved to {} - (Non-tournament Mode)'.format(team))


    def ModifyEveryone(self, team):
        team_num = self.get_team(team)
        playerNames = [player[0] for player in self.players.players]
        for arg in playerNames:
            cmd = '{}modifyTournament "{}" {}\n'.format(self.console, self.aquote(arg), team_num)
            self.write_command(cmd)
        self.logger.info('Everyone in server is moved to {} - (Tournament Mode)'.format(team))