class Main:
    def __init__(self):
        self.the_lobby = "/home/user/altitude-files/maps/lobby_sta.altx"
        self.the_lobby2 = "/home/user/altitude/altitude-mod/files/maps/lobby/lobby_sta.altx"
        self.gamejar = "/home/user/altitude-files/game.jar"
        self.gamejar2 = "/home/user/altitude/altitude-mod/files/game.jar"
        self.server_config = "/home/user/altitude-files/servers/launcher_config.xml"
        self.server_config2 = "/home/user/altitude/altitude-mod/files/launcher_config.xml"
        self.custom_commands = "/home/user/altitude-files/servers/custom_json_commands.txt"
        self.custom_commands2 = "/home/user/altitude/altitude-mod/files/custom_json_commands.txt"


    def lobby(self):
        with open(self.the_lobby, "wb") as the_lobby:
            with open(self.the_lobby2, "rb") as the_lobby2:
                the_lobby.write(the_lobby2.read())
        print("Lobby has been updated")


    def game(self):
        with open(self.gamejar, "wb") as game:
            with open(self.gamejar2, "rb") as game2:
                game.write(game2.read())
        print("Game.jar has been updated")



    def config(self):
        with open(self.server_config, "w") as server_config:
            with open(self.server_config2) as server_config2:
                server_config.write(server_config2.read())
        print("Config has been updated")


    def commands(self):
        with open(self.custom_commands, "w") as commands:
            with open(self.custom_commands2) as commands2:
                commands.write(commands2.read())
        print("Custom json commands have been updated")


    def main(self):
        self.lobby()
        self.game()
        self.config()
        self.commands()



if __name__ == '__main__':
    Main().main()