from hashlib import sha256

class Main:
    def __init__(self):
        self.the_lobby = "/home/user/altitude-files/maps/lobby_sta.altx"
        self.the_lobby2 = "/home/user/altitude/altitude-mod/files/lobby_sta.altx"
        self.gamejar = "/home/user/altitude-files/game.jar"
        self.gamejar2 = "/home/user/altitude/altitude-mod/files/game.jar"
        self.server_config = "/home/user/altitude-files/servers/launcher_config.xml"
        self.server_config2 = "/home/user/altitude/altitude-mod/files/launcher_config.xml"
        self.custom_commands = "/home/user/altitude-files/servers/custom_json_commands.txt"
        self.custom_commands2 = "/home/user/altitude/altitude-mod/files/custom_json_commands.txt"


    def lobby(self):
        hasher = sha256()
        BLOCKSIZE = 10485760
        with open(self.the_lobby, "rb") as the_lobby:
            buf = the_lobby.read(BLOCKSIZE)
            while len(buf) > 0:
                hasher.update(buf)
                buf = the_lobby.read(BLOCKSIZE)
            the_lobby_hash = hasher.hexdigest()

        hasher2 = sha256()
        with open(self.the_lobby2, "rb") as the_lobby2:
            buf2 = the_lobby2.read(BLOCKSIZE)
            while len(buf2) > 0:
                hasher2.update(buf2)
                buf2 = the_lobby2.read(BLOCKSIZE)
            the_lobby2_hash = hasher.hexdigest()
            if the_lobby_hash != the_lobby2_hash:
                with open(self.the_lobby, "wb") as the_lobby:
                    the_lobby.write(the_lobby2.read())
                print("Lobby is now updated!")
            else:
                print("Lobby is already up-to-date")


    def game(self):
        hasher = sha256()
        BLOCKSIZE = 10485760
        with open(self.gamejar, "rb") as gamejar:
            buf = gamejar.read(BLOCKSIZE)
            while len(buf) > 0:
                hasher.update(buf)
                buf = gamejar.read(BLOCKSIZE)
            gamejar_hash = hasher.hexdigest()

        hasher2 = sha256()
        with open(self.gamejar2, "rb") as gamejar2:
            buf2 = gamejar2.read(BLOCKSIZE)
            while len(buf2) > 0:
                hasher2.update(buf2)
                buf2 = gamejar2.read(BLOCKSIZE)
            gamejar2_hash = hasher.hexdigest()
            if gamejar_hash != gamejar2_hash:
                with open(self.gamejar, "wb") as gamejar:
                    gamejar.write(gamejar2.read())
                print("Game.jar is now updated!")
            else:
                print("Game.jar is already up-to-date")



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