import json
from . import run

class Log:
    def __init__(self, log_file_location, logs_archive_location, commands_object, players_object, planes_object):
        self.log_file = log_file_location
        self.logs_archive = logs_archive_location
        self.commands = commands_object
        self.players = players_object
        self.planes = planes_object


    def do_with_logs(self, decoded):
        try:
            try:
                type = decoded['type']
                if type == "chat":
                    run.on_message(self.commands, self.players, decoded)
                if type == "clientAdd":
                    self.players.add(decoded['nickname'], decoded['vaporId'], decoded['player'], decoded['ip'],
                                     decoded['aceRank'], decoded['level'])
                if type == "clientRemove":
                    self.players.remove(decoded['nickname'])
                if type == "playerInfoEv":
                    self.planes.add_or_check(decoded['player'], decoded['plane'], decoded['perkRed'], decoded['perkGreen'],
                                             decoded['perkBlue'], decoded['ace'], decoded['level'])
            except KeyError:
                return
        finally:
            with open(self.log_file, "w"):
                pass


    def Main(self):
        while True:
            with open(self.log_file) as log:
                logs = log.readlines()
                archive = log.read()
            for line in logs:
                try:
                    decoded = json.loads(line)
                    self.do_with_logs(decoded)
                except json.decoder.JSONDecodeError:
                    continue
            with open(self.logs_archive, "a") as log:
                log.write(archive)