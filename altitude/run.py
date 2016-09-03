import logging
from . import commands, log, player, playerinfo_handler, game, start
from .players_database import database_handler


def on_message(logger, commands_object, players_object, decoded):
    if decoded['message'] == "hello":
        commands_object.Message("Hello there, I am the server!")
    elif decoded['message'] == "soo server whats my plane?":
        commands_object.Message(players_object.get_planes(players_object.nickname_from_id(decoded['player'])))
    logger.info('Chat message "{}" was parsed'.format(decoded['message']))




def on_command(commands_object, start_object, players_object, decoded):
    command = decoded['command']
    if command == "match":
        if players_object.get_number_of_players() >= 2:
            argument = decoded['arguments'][0]
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



def on_clientAdd(logger, commands_object, game_object, nickname):
    commands_object.Whisper(nickname, "Welcome to STA! The place where you have real fun!")
    if game_object.current_mode == "ball":
        commands_object.Whisper(nickname, "Press S to use the Ball or any other powerup.")
        if len(game_object.message_for_best_in_ball) != 0:
            commands_object.Multiple_Whispers(nickname, game_object.message_for_best_in_ball)
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


def run(port, commands_file, logs_file, old_logs, logs_archive):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s   -   %(levelname)s   -   %(message)s", "%d-%m-%Y, %H:%M:%S")
    fh = logging.FileHandler('mod_debug_logs.txt')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    database_handler.Reader(logger).reset_values() # Just resetting goals, bases and kills
    database = database_handler.Reader(logger)
    planes = player.Plane(logger)
    plane_positions = player.PlanePosition(logger)
    players = player.Player(logger, planes)
    planes.get_players_object(players)
    command = commands.Commands(logger, players, port, commands_file)
    players.get_commands_object(command)
    start_map = start.Map(logger, command)
    planes.get_commands_object(command)
    playerInfoHandler = playerinfo_handler.Handler(logger, command, planes, players)
    game_info = game.Game(logger, players, planes, plane_positions, command, database)
    logs = log.Log(logger, logs_file, old_logs, logs_archive, start_map, command, database, players, plane_positions, planes, playerInfoHandler, game_info)
    game_info.get_logs_object(logs)
    players.get_game_object(game_info)
    logger.info('Mod started')
    logs.Main()