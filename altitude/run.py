import logging
from . import commands, log, player, playerinfo_handler, game, start, permissions
from .players_database import database_handler

class Run:
    def __init__(self, port, commands_file, logs_file, old_logs, logs_archive, server_mode):
        self.logs_file = logs_file
        self.old_logs = old_logs
        self.logs_archive = logs_archive
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s   -   %(levelname)s   -   %(message)s", "%d-%m-%Y, %H:%M:%S")
        fh = logging.FileHandler('mod_debug_logs.txt')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)
        database_handler.Reader(self.logger).reset_values()  # Just resetting goals, bases and kills
        self.database = database_handler.Reader(self.logger)
        self.planes = player.Plane(self.logger)
        self.plane_positions = player.PlanePosition(self.logger)
        self.players = player.Player(self.logger, self.planes)
        self.planes.get_players_object(self.players)
        self.command = commands.Commands(self.logger, self.players, port, commands_file)
        self.teachers = permissions.Permissions(self.logger, self.command, self.players, server_mode)
        self.players.get_commands_object(self.command)
        self.start_map = start.Map(self.logger, self.command)
        self.planes.get_commands_object(self.command)
        self.playerInfoHandler = playerinfo_handler.Handler(self.logger, self.command, self.planes, self.players)
        self.game_info = game.Game(self.logger, self.players, self.planes, self.plane_positions, self.command, self.database)
        self.logs = log.Log(self.logger, logs_file, old_logs, logs_archive, self.start_map, self.command, self.database,
                       self.players, self.plane_positions, self.planes, self.playerInfoHandler, self.game_info, self.teachers)
        self.game_info.get_logs_object(self.logs)
        self.players.get_game_object(self.game_info)
        self.logger.info('Mod started')


    def on_message(self):
        if self.logs.decoded['message'] == "hello":
            self.command.Message("Hello there, I am the server!")
        elif self.logs.decoded['message'] == "soo server whats my plane?":
            self.command.Message(self.players.get_planes(self.players.nickname_from_id(self.logs.decoded['player'])))
        self.logger.info('Chat message "{}" was parsed'.format(self.logs.decoded['message']))


    def on_command(self):
        sender = self.logs.decoded['source']
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
        elif command == "sta_setServerMode":
            self.teachers.setServerMode(sender, argument)
        elif command == "sta_addTeacher":
            self.teachers.addTeacher(sender, argument)
        elif command == "sta_addTeacherWithVapor":
            self.teachers.addTeacherWithVapor(sender, argument)
        elif command == "sta_removeTeacher":
            self.teachers.removeTeacher(sender, argument)
        elif command == "sta_removeTeacherWithNickname":
            self.teachers.removeTeacherWithNickname(sender, argument)
        elif command == "sta_listTeachers":
            self.teachers.listTeachers(sender)
        elif command == "sta_removeBan":
            self.teachers.removeBan(sender, argument)
        elif command == "sta_removeBanWithNickname":
            self.teachers.removeBanWithNickname(sender, argument)
        elif command == "sta_addBan":
            self.teachers.addBan(sender, argument)
        elif command == "sta_addBanWithVapor":
            self.teachers.addBanWithVapor(sender, argument)
        elif command == "sta_listBans":
            self.teachers.listBans(sender)
        elif command == "sta_listUnbanned":
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



    def on_clientAdd(self):
        nickname = self.logs.decoded['nickname']
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
                                                         'start a vote for a new match! (Enter to open the chat)'])
        self.logger.info("{} is welcomed!".format(nickname))



    def run(self):
        self.logs = log.Log(self.logger, self.logs_file, self.old_logs, self.logs_archive, self.start_map, self.command, self.database,
                            self.players, self.plane_positions, self.planes, self.playerInfoHandler, self.game_info,
                            self.teachers)
        self.game_info.get_logs_object(self.logs)
        self.players.get_game_object(self.game_info)
        self.logger.info('Mod started')
        self.logs.get_run_object(self)
        self.logs.Main()
