import json
from os import remove
from os.path import isfile, getsize
from . import run






class Log:
    def __init__(self, logger, log_file_location, old_logs_location, logs_archive_location, commands_object,
                 players_object, planesPositions_object, planes_object, playerInfo_handler, game):
        self.logger = logger
        self.current_line = 0
        self.log_file = log_file_location
        self.logs_archive = logs_archive_location
        self.old_logs = old_logs_location
        self.commands = commands_object
        self.players = players_object
        self.planesPositions = planesPositions_object
        self.planes = planes_object
        self.playerInfoHandler = playerInfo_handler
        self.game = game
        self.getPositions = False


    def do_with_logs(self):
        try:
            type = self.decoded['type']
            if type == "chat":
                self.logger.info("Parsing chat message: {}".format(self.decoded['message']))
                run.on_message(self.logger, self.commands, self.players, self.decoded)



            if type == "mapChange":
                self.getPositions = False
                self.game.check_current_mode_and_map(self.decoded['map'])
                self.planes.on_changeMap()




            if type == "logPlanePositions":
                self.planesPositions.add_or_check(self.decoded)
                self.game.on_position()


            # Players
            elif type == "clientAdd":
                self.logger.info("Adding {}'s client to players and planes list".format(self.decoded['nickname']))
                self.players.add(self.decoded['nickname'], self.decoded['vaporId'], self.decoded['player'], self.decoded['ip'])
                run.on_clientAdd(self.logger, self.commands, self.decoded['nickname'])
            elif type == "logServerStatus":
                self.logger.info("Adding all clients in server to players list")
                self.players.get_all_players(self.decoded['nicknames'], self.decoded['vaporIds'], self.decoded['playerIds'],
                                             self.decoded['ips'])
                self.commands.AssignEveryone("spec")
            elif type == "clientRemove":
                self.logger.info("Removing {}'s client from players and planes list".format(self.decoded['nickname']))
                self.players.remove(self.decoded['nickname'])
            elif type == "clientNicknameChange":
                self.logger.info("Changing {}'s nickname in players and planes list".format(self.decoded['oldNickname']))
                self.players.nickname_change(self.decoded['oldNickname'], self.decoded['newNickname'])
            elif type == "playerInfoEv":
                self.playerInfoHandler.parse(self.decoded)










        except KeyError:
            self.logger.debug("Could not handle line {}: {}\nmaybe add functionality for it?\n".format(self.current_line+1, self.decoded))
            pass





    def Main(self):
        if getsize(self.log_file) != 0:
            self.logger.info("Logs file is not empty; appending its content to the archive logs")
            with open(self.log_file) as log:
                logs = log.read()
                with open(self.logs_archive, "a") as archive:
                    archive.write(logs)
            with open(self.log_file, "w"):
                pass
        self.commands.LogServerStatus()
        while True:
            if self.getPositions is True:
                self.commands.LogPlanePositions()
            with open(self.log_file) as log:
                logs = log.readlines()[self.current_line:]
            for line in logs:
                if 'port' in line:
                    try:
                        self.decoded = json.loads(line)
                        self.do_with_logs()
                    except json.decoder.JSONDecodeError:
                        self.logger.warn("Could not parse line {}: {}".format(self.current_line+1, line))
                        continue
                    finally:
                        self.current_line += 1
                        if isfile(self.old_logs) is True:
                            self.logger.info("Old logs file found; copying it into an archive logs file, deleting it and starting parsing new logs file!")
                            self.current_line = 0
                            with open(self.old_logs) as old_log:
                                old_logs = old_log.read()
                                with open(self.logs_archive, "a") as archive:
                                    archive.write(old_logs)
                            remove(self.old_logs)
                            self.logger.info("Started parsing new logs file")