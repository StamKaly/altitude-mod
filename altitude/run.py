from . import commands, log, player


def on_message(commands_object, players_object, decoded):
    if decoded['message'] == "hello":
        commands_object.Message("Hello there, I am the server!")
    if decoded['message'] == "soo server whats my plane?":
        commands_object.Message(players_object.get_planes(decoded['player']))




def add_player(player_object, nickname, vaporId, playerId, IP, ace, level):
    player_object.add(nickname, vaporId, playerId, IP, ace, level)



def remove_player(player_object, nickname):
    player_object.remove(nickname)



def run(port, commands_file, logs_file, logs_archive):
    planes = player.Plane()
    players = player.Player(planes)
    command = commands.Commands(port, commands_file)
    logs = log.Log(logs_file, logs_archive, command, players, planes)
    logs.Main()