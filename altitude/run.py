import logging
from . import commands, log, player, playerinfo_handler, game


def on_message(logger, commands_object, players_object, decoded):
    if decoded['message'] == "hello":
        commands_object.Message("Hello there, I am the server!")
    elif decoded['message'] == "soo server whats my plane?":
        commands_object.Message(players_object.get_planes(players_object.nickname_from_id(decoded['player'])))
    logger.info('Chat message "{}" was parsed'.format(decoded['message']))




def on_clientAdd(logger, commands_object, nickname):
    commands_object.Multiple_Whispers(nickname, ["Hey there, it's me!",
                                                 "-Who are you? Mandel or...",
                                                 "ITS ME, MARIO!"])
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
    planes = player.Plane(logger)
    plane_positions = player.PlanePosition(logger)
    players = player.Player(logger, planes)
    command = commands.Commands(logger, players, port, commands_file)
    planes.get_commands_object(command)
    playerInfoHandler = playerinfo_handler.Handler(logger, command, planes, players)
    game_info = game.Game(logger, players, planes, command)
    logs = log.Log(logger, logs_file, old_logs, logs_archive, command, players, plane_positions, planes, playerInfoHandler, game_info)
    logger.info('Mod started')
    logs.Main()