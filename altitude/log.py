import json
from os import remove
from os.path import isfile
from . import run






class Log:
    def __init__(self, logger, log_file_location, old_logs_location, logs_archive_location, commands_object, players_object, planes_object):
        self.logger = logger
        self.log_file = log_file_location
        self.logs_archive = logs_archive_location
        self.old_logs = old_logs_location
        self.commands = commands_object
        self.players = players_object
        self.planes = planes_object


    def do_with_logs(self, decoded, current_line):
        try:
            type = decoded['type']
            if type == "chat":
                self.logger.info("Parsing chat message: {}".format(decoded['message']))
                run.on_message(self.commands, self.players, decoded)
            if type == "clientAdd":
                self.logger.info("Adding {}'s client to players and planes list".format(decoded['nickname']))
                self.players.add(decoded['nickname'], decoded['vaporId'], decoded['player'], decoded['ip'])
            if type == "clientRemove":
                self.logger.info("Removing {}'s client from players and planes list".format(decoded['nickname']))
                self.players.remove(decoded['nickname'])
            if type == "playerInfoEv":
                self.planes.add_or_check(self.players.nickname_from_id(decoded['player']), decoded['plane'], decoded['perkRed'], decoded['perkGreen'],
                                         decoded['perkBlue'], decoded['ace'], decoded['level'])
                pass
        except KeyError:
            self.logger.debug("Could not handle line {}: {}\nmaybe add functionality for it?\n".format(current_line+1, decoded))
            pass





    def Main(self):
        current_line = 0
        while True:
            with open(self.log_file) as log:
                logs = log.readlines()[current_line:]
            for line in logs:
                if 'port' in line:
                    try:
                        decoded = json.loads(line)
                        self.do_with_logs(decoded, current_line)
                    except json.decoder.JSONDecodeError:
                        self.logger.warn("Could not parse line {}: {}".format(current_line+1, line))
                        continue
                    finally:
                        current_line += 1
                        if isfile(self.old_logs) is True:
                            self.logger.info("Old logs file found; copying it into an archive logs file, deleting it and starting parsing new logs file!")
                            current_line = 0
                            with open(self.old_logs) as old_log:
                                old_logs = old_log.read()
                                with open(self.logs_archive, "a") as archive:
                                    archive.write(old_logs)
                            remove(self.old_logs)
                            self.logger.info("Started parsing new logs file")