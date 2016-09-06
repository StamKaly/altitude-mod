import logging
from . import commands, log, player, playerinfo_handler, game, start, permissions
from .players_database import database_handler


def on_message(logger, commands_object, players_object, decoded):
    if decoded['message'] == "hello":
        commands_object.Message("Hello there, I am the server!")
    elif decoded['message'] == "soo server whats my plane?":
        commands_object.Message(players_object.get_planes(players_object.nickname_from_id(decoded['player'])))
    logger.info('Chat message "{}" was parsed'.format(decoded['message']))




def on_command(commands_object, sender, start_object, players_object, permission, decoded):
    command = decoded['command']
    try:
        argument = decoded['arguments'][0]
    except IndexError:
        argument = None
    if command == "match":
        if players_object.get_number_of_players() >= 2:
            if argument == "Ball":
                start_object.ball()
            elif argument == "TBD":
                start_object.tbd()
            elif argument == "1dm":
                start_object.onedm()
            elif argument == "Football":
                start_object.football()
        else:
            commands_object.Message("2 or more players must be here to start a match!")
    elif command == "matchWithMap":
        if players_object.get_number_of_players() >= 2:
            commands_object.ChangeMap(argument)
        else:
            commands_object.Message("2 or more players must be here to start a match!")
    elif command == "sta_setServerMode":
        permission.setServerMode(sender, argument)
    elif command == "sta_addTeacher":
        permission.addTeacher(sender, argument)
    elif command == "sta_addTeacherWithVapor":
        permission.addTeacherWithVapor(sender, argument)
    elif command == "sta_removeTeacher":
        permission.removeTeacher(sender, argument)
    elif command == "sta_removeTeacherWithNickname":
        permission.removeTeacherWithNickname(sender, argument)
    elif command == "sta_listTeachers":
        permission.listTeachers(sender)
    elif command == "sta_removeBan":
        permission.removeBan(sender, argument)
    elif command == "sta_removeBanWithNickname":
        permission.removeBanWithNickname(sender, argument)
    elif command == "sta_addBan":
        permission.addBan(sender, argument)
    elif command == "sta_addBanWithVapor":
        permission.addBanWithVapor(sender, argument)
    elif command == "sta_listBans":
        permission.listBans(sender)
    elif command == "sta_listUnbanned":
        permission.listUnbanned(sender)
    elif command == "goInsane":
        if argument == "True":
            commands_object.CameraScale(40)
            commands_object.PlaneScale(40)
            commands_object.Gravity("everything")
            commands_object.Message("Insane mode activated!")
        elif argument == "False":
            commands_object.CameraScale(100)
            commands_object.PlaneScale(100)
            commands_object.Gravity("nothing")
            commands_object.Message("Insane mode deactivated")



def on_clientAdd(logger, commands_object, game_object, nickname):
    commands_object.Whisper(nickname, "Welcome to STA! The place where you have real fun!")
    if game_object.current_mode == "ball":
        commands_object.Whisper(nickname, "Press S to use the Ball or any other powerup.")
        if game_object.current_map != "football":
            if len(game_object.message_for_best_in_ball) != 0:
                commands_object.Multiple_Whispers(nickname, game_object.message_for_best_in_ball)
            else:
                commands_object.Multiple_Whispers(nickname, ['There is no best player of the day in Ball yet.',
                                                             'Be the first one!'])
        else:
            if len(game_object.message_for_best_in_football) != 0:
                commands_object.Multiple_Whispers(nickname, game_object.message_for_best_in_football)
            else:
                commands_object.Multiple_Whispers(nickname, ['There is no best player of the day in Ball yet.',
                                                             'Be the first one!'])
    elif game_object.current_mode == "tbd":
        commands_object.Whisper(nickname, 'Destroy the base with the bomb, press S to use the bomb.')
        if len(game_object.message_for_best_in_tbd) != 0:
            commands_object.Multiple_Whispers(nickname, game_object.message_for_best_in_tbd)
        else:
            commands_object.Multiple_Whispers(nickname, ['There is no best player of the day in TBD yet.',
                                                         'Be the first one!'])
    elif game_object.current_mode == "1dm":
        commands_object.Whisper(nickname, "Kill as many planes as you can and try not to die.")
        if len(game_object.message_for_best_in_1dm) != 0:
            commands_object.Multiple_Whispers(nickname, game_object.message_for_best_in_1dm)
        else:
            commands_object.Multiple_Whispers(nickname, ['There is no best player of the day in 1dm yet.',
                                                         'Be the first one!'])
    elif game_object.current_mode == "lobby":
        commands_object.Multiple_Whispers(nickname, ['This is the lobby, when there are 2 or more players here,',
                                                     'use the command "/match <gameMode>" in the chat to',
                                                     'start a vote for a new match! (Enter to open the chat)'])
    logger.info("{} is welcomed!".format(nickname))


def run(port, commands_file, logs_file, old_logs, logs_archive, server_mode):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s   -   %(levelname)s   -   %(message)s", "%d-%m-%Y, %H:%M:%S")
    fh = logging.FileHandler('mod_debug_logs.txt')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    database_handler.Reader(logger).reset_values() # Just resetting goals, bases and kills
    database = database_handler.Reader(logger)
    planes = player.Plane(logger)
    plane_positions = player.PlanePosition(logger)
    players = player.Player(logger, planes)
    planes.get_players_object(players)
    command = commands.Commands(logger, players, port, commands_file)
    teachers = permissions.Permissions(logger, command, players, server_mode)
    players.get_commands_object(command)
    start_map = start.Map(logger, command)
    planes.get_commands_object(command)
    playerInfoHandler = playerinfo_handler.Handler(logger, command, planes, players)
    game_info = game.Game(logger, players, planes, plane_positions, command, database)
    logs = log.Log(logger, logs_file, old_logs, logs_archive, start_map, command, database, players, plane_positions,
                   planes, playerInfoHandler, game_info, teachers)
    game_info.get_logs_object(logs)
    players.get_game_object(game_info)
    logger.info('Mod started')
    logs.Main()
