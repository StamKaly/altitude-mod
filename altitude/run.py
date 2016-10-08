import logging
from ast import literal_eval
from time import sleep
from random import choice
from . import commands, log, player, playerinfo_handler, game, start, permissions
from .players_database import database_handler
from .config import change


class Run:
    def __init__(self, port, commands_file, logs_file, old_logs, logs_archive, chat_logs_location, server_mode):
        self.logs_file = logs_file
        self.old_logs = old_logs
        self.logs_archive = logs_archive
        self.chat_logs = chat_logs_location
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s   -   %(levelname)s   -   %(message)s", "%d-%m-%Y, %H:%M:%S")
        fh = logging.FileHandler('mod_debug_logs.txt')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)
        self.database = database_handler.Reader(self.logger)
        self.database.reset_values() # Just resetting goals, bases and kills
        self.planes = player.Plane(self.logger)
        self.plane_positions = player.PlanePosition(self.logger)
        self.players = player.Player(self.logger, self.planes)
        self.planes.get_players_object(self.players)
        self.command = commands.Commands(self.logger, self.players, port, commands_file)
        self.server_handler = change.Change(self.logger, self.command)
        self.teachers = permissions.Permissions(self.logger, self.command, self.players, server_mode)
        self.players.get_perm_object(self.teachers)
        self.players.get_commands_object(self.command)
        self.start_map = start.Map(self.logger, self.command)
        self.planes.get_commands_object(self.command)
        self.playerInfoHandler = playerinfo_handler.Handler(self.logger, self.command, self.planes, self.players)
        self.game_info = game.Game(self.logger, self.players, self.planes, self.plane_positions, self.command, self.database)
        self.logs = log.Log(self.logger, logs_file, old_logs, logs_archive, self.start_map, self.command, self.database,
                       self.players, self.plane_positions, self.planes, self.playerInfoHandler, self.game_info, self.teachers)
        self.game_info.get_logs_object(self.logs)
        self.players.get_game_object(self.game_info)
        self.extraMessage = None
        self.started_match = False
        self.logger.info('Mod started')


    def save_log(self, log):
        with open("./files/chat_logs.txt", "a") as today_logs:
            today_logs.write("{}\n".format(log))
        with open(self.chat_logs, "a") as chat_logs:
            chat_logs.write("{}\n".format(log))

    def empty_today_logs(self):
        with open("./files/chat_logs.txt", "w") as logs:
            logs.write("New Day\n")


    def get_today_logs(self, requester):
        with open("./files/chat_logs.txt") as today_logs:
            for log in today_logs.readlines():
                self.command.Whisper(requester, log.replace("\n", ""))



    def on_message(self):
        nickname = self.players.nickname_from_id(self.logs.decoded['player'])
        message = self.logs.decoded['message']
        server = self.logs.decoded['server']
        teamChat = self.logs.decoded['team']
        if server is False and teamChat is False:
            self.save_log("{}: {}".format(self.command.aquote(nickname), message))
        elif server is False and teamChat is True:
            self.save_log("[Team] {}: {}".format(self.command.aquote(nickname), message))
        self.logger.info('Chat message "{}" was parsed'.format(self.logs.decoded['message']))


    def on_command(self):
        sender = self.logs.decoded['source']
        sender_nickname = self.players.nickname_from_vapor(sender)
        command = self.logs.decoded['command']
        try:
            argument = self.logs.decoded['arguments'][0]
        except IndexError:
            argument = None
        if command == "match":
            if self.players.get_number_of_players() >= 2:
                if argument == "Ball":
                    self.start_map.ball()
                elif argument == "TBD":
                    self.start_map.tbd()
                elif argument == "1dm":
                    self.start_map.onedm()
                elif argument == "Football":
                    self.start_map.football()
            else:
                self.command.Message("2 or more players must be here to start a match!")
        elif command == "matchWithMap":
            if self.players.get_number_of_players() >= 2:
                self.command.ChangeMap(argument)
            else:
                self.command.Message("2 or more players must be here to start a match!")
        elif command == "sSM": # sta_setServerMode
            self.teachers.setServerMode(sender, argument)
        elif command == "aT": # sta_addTeacher
            self.teachers.addTeacher(sender, argument)
        elif command == "aTWV": # sta_addTeacherWithVapor
            self.teachers.addTeacherWithVapor(sender, argument)
        elif command == "rT": # sta_removeTeacher
            self.teachers.removeTeacher(sender, argument)
        elif command == "rTWN": # sta_removeTeacherWithNickname
            self.teachers.removeTeacherWithNickname(sender, argument)
        elif command == "lT": # sta_listTeachers
            self.teachers.listTeachers(sender)
        elif command == "rB": # sta_removeBan
            self.teachers.removeBan(sender, argument)
        elif command == "rBWN": # sta_removeBanWithNickname
            self.teachers.removeBanWithNickname(sender, argument)
        elif command == "aB": # sta_addBan
            self.teachers.addBan(sender, argument)
        elif command == "aBWV": # sta_addBanWithVapor
            self.teachers.addBanWithVapor(sender, argument)
        elif command == "lB": # sta_listBans
            self.teachers.listBans(sender)
        elif command == "lU": # sta_listUnbanned
            self.teachers.listUnbanned(sender)
        elif command == "goInsane":
            if argument == "True":
                self.command.CameraScale(40)
                self.command.PlaneScale(40)
                self.command.Gravity("everything")
                self.command.Message("Insane mode activated!")
            elif argument == "False":
                self.command.CameraScale(100)
                self.command.PlaneScale(100)
                self.command.Gravity("nothing")
                self.command.Message("Insane mode deactivated")
        elif command == "myStats":
            self.command.Whisper(sender_nickname, self.database.myStats(sender, argument))
        elif command == "rS": # restartServer
            self.server_handler.handle(True)
        elif command == "cSN": # changeServerName
            self.server_handler.handle(False, name = argument)
        elif command == "cSP": # changeServerPassword
            if argument == "None":
                self.server_handler.handle(False)
            else:
                self.server_handler.handle(False, password = argument)
        elif command == "aM": # addMap
            self.server_handler.addMap(sender_nickname, argument)
        elif command == "rM": # removeMap
            self.server_handler.removeMap(sender_nickname, argument)
        elif command == "aA": # addAdmin
            self.server_handler.addAdmin(sender_nickname, argument)
        elif command == "rA": # removeAdmin
            self.server_handler.removeAdmin(sender_nickname, argument)
        elif command == "eM": # extraMessage
            if argument == "None":
                self.extraMessage = None
                self.command.Whisper(sender_nickname, "There are now no extra messages!")
            else:
                try:
                    self.extraMessage = literal_eval(argument)
                    self.command.Whisper(sender_nickname, "Extra message(s) are added!")
                except ValueError:
                    self.command.Whisper(sender_nickname, "Invalid list syntax, try again!")
        elif command == "vCL": # viewChatLogs
            self.get_today_logs(sender_nickname)
        elif command == "veteranBars":
            self.command.Multiple_Whispers(sender_nickname, ["These are bars that are displayed next to your plane that",
                                                   "not only are a badge of honor but increase your plane's",
                                                   "health, speed, turning, damage and energy. Each time you",
                                                   "successfully earn 10 experience without dying you will",
                                                   "earn one bar next to your plane. Each bar is equivalent to",
                                                   "an increase of 2% of the previous mentioned categories."])


    def on_clientAdd(self):
        nickname = self.logs.decoded['nickname']
        self.save_log("{} has joined the game.".format(self.command.aquote(nickname)))
        self.command.Whisper(nickname, "Welcome to STA! The place where you have real fun!")
        if self.game_info.current_mode == "ball":
            self.command.Whisper(nickname, "Press S to use the Ball or any other powerup.")
            if self.game_info.current_map != "football":
                if len(self.game_info.message_for_best_in_ball) != 0:
                    self.command.Multiple_Whispers(nickname, self.game_info.message_for_best_in_ball)
                else:
                    self.command.Multiple_Whispers(nickname, ['There is no best player of the day in Ball yet.',
                                                                 'Be the first one!'])
            else:
                if len(self.game_info.message_for_best_in_football) != 0:
                    self.command.Multiple_Whispers(nickname, self.game_info.message_for_best_in_football)
                else:
                    self.command.Multiple_Whispers(nickname, ['There is no best player of the day in Ball yet.',
                                                                 'Be the first one!'])
        elif self.game_info.current_mode == "tbd":
            self.command.Whisper(nickname, 'Destroy the base with the bomb, press S to use the bomb.')
            if len(self.game_info.message_for_best_in_tbd) != 0:
                self.command.Multiple_Whispers(nickname, self.game_info.message_for_best_in_tbd)
            else:
                self.command.Multiple_Whispers(nickname, ['There is no best player of the day in TBD yet.',
                                                             'Be the first one!'])
        elif self.game_info.current_mode == "1dm":
            self.command.Whisper(nickname, "Kill as many planes as you can and try not to die.")
            if len(self.game_info.message_for_best_in_1dm) != 0:
                self.command.Multiple_Whispers(nickname, self.game_info.message_for_best_in_1dm)
            else:
                self.command.Multiple_Whispers(nickname, ['There is no best player of the day in 1dm yet.',
                                                             'Be the first one!'])
        elif self.game_info.current_mode == "lobby":
            self.command.Multiple_Whispers(nickname, ['This is the lobby, when there are 2 or more players here,',
                                                      'use the command \\\"/match <gameMode>\\\" in the chat to',
                                                      'start a new match! (Press Enter to open the chat)'])
        if self.extraMessage is not None:
            self.command.Multiple_Whispers(nickname, self.extraMessage)
        if self.logs.decoded['aceRank'] == 0 and self.logs.decoded['level'] <= 59:
            if self.started_match is False and self.game_info.current_mode == "lobby":
                self.command.Message("Starting match...")
                sleep(2)
                choice([self.start_map.ball, self.start_map.tbd])()
            elif self.started_match is False:
                self.started_match = True
        self.logger.info("{} is welcomed!".format(nickname))



    def run(self):
        self.logs = log.Log(self.logger, self.logs_file, self.old_logs, self.logs_archive, self.start_map, self.command, self.database,
                            self.players, self.plane_positions, self.planes, self.playerInfoHandler, self.game_info,
                            self.teachers)
        self.game_info.get_logs_object(self.logs)
        self.players.get_game_object(self.game_info)
        self.players.get_run_object(self)
        self.logger.info('Mod started')
        self.logs.get_run_object(self)
        self.logs.Main()
