import json
from os import remove
from os.path import isfile, getsize
import time





class Log:
    def __init__(self, logger, log_file_location, old_logs_location, logs_archive_location, start_object, commands_object,
                 database_object, players_object, planesPositions_object, planes_object, playerInfo_handler, game, permissions):
        self.logger = logger
        self.current_line = 0
        self.log_file = log_file_location
        self.logs_archive = logs_archive_location
        self.old_logs = old_logs_location
        self.start = start_object
        self.commands = commands_object
        self.players = players_object
        self.database = database_object
        self.planesPositions = planesPositions_object
        self.planes = planes_object
        self.playerInfoHandler = playerInfo_handler
        self.game = game
        self.permissions = permissions
        self.getPositions = False
        self.newDay = False


    def get_run_object(self, run):
        self.run = run


    def do_with_logs(self):
        try:
            type = self.decoded['type']
            if type == "chat":
                self.logger.info("Parsing chat message: {}".format(self.decoded['message']))
                self.run.on_message()



            elif type == "mapChange":
                self.getPositions = False
                self.game.check_current_mode_and_map(self.decoded['map'])
                self.planes.on_changeMap()
                self.run.save_log("Map: {}".format(self.decoded['map']))

            elif type == "logPlanePositions":
                self.planesPositions.add_or_check(self.decoded)
                self.game.on_position()



            # Scores
            elif type == "goal":
                self.game.on_goal(self.decoded['player'], self.decoded['assister'], self.decoded['secondaryAssister'])

            elif type == "structureDestroy" and self.decoded['target'] == 'base':
                self.game.on_base_destroy(self.decoded['player'])

            elif type == "kill" and self.decoded['source'] == 'plane':
                self.game.on_kill(self.decoded['player'])

            elif type == "roundEnd":
                self.game.on_roundEnd()



            # On command
            elif type == "consoleCommandExecute":
                if self.decoded['source'] != "00000000-0000-0000-0000-000000000000":
                    self.run.on_command()





            # Players
            elif type == "clientAdd":
                self.permissions.on_clientAdd(self.decoded['nickname'], self.decoded['vaporId'], self.decoded['level'], self.decoded['aceRank'])
                check = self.database.add_or_check(self.decoded['nickname'], self.decoded['vaporId'], self.decoded['ip'].split(":")[0], True)
                if check == "troll":
                    perm_check = self.permissions.get_permission(self.database.get_vapor_from_ip(self.decoded['ip'].split(":")[0]))
                    if perm_check != "teacher" and perm_check != "unbanned":
                        self.commands.ChangeServer(self.decoded['nickname'], "91.121.160.173:27276", "x")
                        self.commands.AddBan(self.decoded['ip'], 20, "forever", "No trolls are allowed in this server, if you got bored you better stop playing rather than trolling. :)")
                        return
                self.logger.info("Adding {}'s client to players and planes list".format(self.decoded['nickname']))
                self.players.add(self.decoded['nickname'], self.decoded['vaporId'], self.decoded['player'], self.decoded['ip'].split(":")[0])
                self.run.on_clientAdd()
            elif type == "logServerStatus":
                self.logger.info("Adding all clients in server to players list")
                self.players.get_all_players(self.decoded['nicknames'], self.decoded['vaporIds'], self.decoded['playerIds'],
                                             self.decoded['ips'])
                self.commands.AssignEveryone("spec")
            elif type == "clientRemove":
                self.logger.info("Removing {}'s client from players and planes list".format(self.decoded['nickname']))
                self.players.remove(self.decoded['nickname'])
                self.run.save_log("{} has left the game.".format(self.commands.aquote(self.decoded['nickname'])))
            elif type == "clientNicknameChange":
                self.logger.info("Changing {}'s nickname in players and planes list".format(self.decoded['oldNickname']))
                self.players.nickname_change(self.decoded['oldNickname'], self.decoded['newNickname'])
                self.database.on_nickname_change(self.decoded['oldNickname'], self.decoded['newNickname'])
                self.permissions.on_nicknameChange(self.decoded['newNickname'])
                self.run.save_log("[Nickname Changed] {} is now {}".format(self.commands.aquote(self.decoded['oldNickname']),
                                                                           self.commands.aquote(self.decoded['newNickname'])))
            elif type == "playerInfoEv":
                try:
                    self.playerInfoHandler.parse(self.decoded)
                except TypeError:
                    return
            elif type == "spawn":
                self.permissions.on_spawn(self.decoded['player'])










        except KeyError:
            self.logger.debug("Could not handle line {}: {}\nmaybe add functionality for it?\n".format(self.current_line+1, self.decoded))





    def Main(self):
        if getsize(self.log_file) != 0:
            self.logger.info("Logs file is not empty; appending its content to the archive logs")
            with open(self.log_file) as log:
                logs = log.read()
                with open(self.logs_archive, "a") as archive:
                    archive.write(logs)
            with open(self.log_file, "w"):
                pass
        while True:
            GMT_time = time.gmtime()
            if GMT_time.tm_hour == 0 and GMT_time.tm_min == 0 and self.newDay is False:
                self.newDay = True
                self.game.reset_scores()
                self.run.empty_today_logs()
            elif GMT_time.tm_hour == 0 and GMT_time.tm_min == 1 and self.newDay is True:
                self.newDay = False
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
