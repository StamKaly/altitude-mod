class Commands:
    def __init__(self, port, commands_file_location):
        self.commands_file = commands_file_location
        self.console = "{},console,".format(port)


    def write_command(self, cmd):
        with open(self.commands_file, "a") as commands:
            commands.write(cmd)


    def StartTournament(self):
        cmd = '{}startTournament'.format(self.console)
        self.write_command(cmd)


    def StopTournament(self):
        cmd = '{}stopTournament'.format(self.console)
        self.write_command(cmd)


    def Whisper(self, playerName, message):
        cmd = '{}serverWhisper "{}" "{}"\n'.format(self.console, playerName, message)
        self.write_command(cmd)


    def Multiple_Whispers(self, playerName, messages):
        for arg in messages:
            cmd = '{}serverWhisper "{}" "{}"\n'.format(self.console, playerName, arg)
            self.write_command(cmd)


    def Message(self, message):
        cmd = '{}serverMessage "{}"\n'.format(self.console, message)
        self.write_command(cmd)


    def Multiple_Messages(self, messages):
        for arg in messages:
            cmd = '{}serverMessage "{}"\n'.format(self.console, arg)
            self.write_command(cmd)


    def ChangeMap(self, mapName):
        cmd = '{}changeMap {}\n'.format(self.console, mapName)
        self.write_command(cmd)



    def CameraScale(self, camera):
        cmd = '{}testCameraViewScale {}\n'.format(self.console, camera)
        self.write_command(cmd)



    def PlaneScale(self, scale):
        cmd = '{}testPlaneScale {}\n'.format(self.console, scale)
        self.write_command(cmd)



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



    def HealthModifier(self, health):
        cmd = '{}testHealthModifier {}'.format(self.console, health)
        self.write_command(cmd)




    def get_team(self, team):
        if team == "left":
            return "0"
        if team == "right":
            return "1"
        if team == "spec":
            return "-1"


    def AssignTeam(self, playerName, team):
        cmd = '{}assignTeam "{}" {}\n'.format(self.console, playerName, self.get_team(team))
        self.write_command(cmd)


    def ModifyTournament(self, playerName, team):
        cmd = '{}modifyTournament "{}" {}\n'.format(self.console, playerName, self.get_team(team))
        self.write_command(cmd)


    def AssignEveryone(self, playerNames, team):
        team = self.get_team(team)
        for arg in playerNames:
            cmd = '{}assignTeam "{}" {}\n'.format(self.console, arg, team)
            self.write_command(cmd)


    def ModifyEveryone(self, playerNames, team):
        team = self.get_team(team)
        for arg in playerNames:
            cmd = '{}modifyTournament "{}" {}\n'.format(self.console, arg, team)
            self.write_command(cmd)