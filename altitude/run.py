import logging
from . import commands, log, player


def on_message(commands_object, players_object, decoded):
    if decoded['message'] == "hello":
        commands_object.Message("Hello there, I am the server!")
    if decoded['message'] == "soo server whats my plane?":
        commands_object.Message(players_object.get_planes(players_object.nickname_from_id(decoded['player'])))




def add_player(player_object, nickname, vaporId, playerId, IP):
    player_object.add(nickname, vaporId, playerId, IP)



def remove_player(player_object, nickname):
    player_object.remove(nickname)



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
    players = player.Player(logger, planes)
    command = commands.Commands(port, commands_file)
    logs = log.Log(logger, logs_file, old_logs, logs_archive, command, players, planes)
    logger.info('Mod started')
    logs.Main()