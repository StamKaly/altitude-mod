from requests import get
from os import chdir
from subprocess import call
from time import sleep

class Change:
    def __init__(self, logger, commands):
        self.logger = logger
        self.commands = commands
        self.admins = "./altitude/config/admins.txt"
        self.maps = "./altitude/config/maps.txt"
        self.config = "./files/launcher_config.xml"


    def quoteName(self, name):
        return name.replace('"', "&quot;")


    def addMap(self, sender, _map_):
        if _map_.startwith("http") is True and _map_.endswith(".altx") is True:
            response = get(_map_)
            name = _map_.split("/", _map_.count("/"))[_map_.count("/")]
            name_without_extension, _ = name.split(".")
            with open(self.maps) as maps_file:
                for map in maps_file.readlines():
                    if name_without_extension == map:
                        return self.commands.Whisper(sender, "{} already exists!".format(name_without_extension))
            with open("/home/user/altitude-files/maps/{}".format(name), "wb") as _map_:
                for data in response.iter_content(1024):
                    _map_.write(data)
            with open(self.maps, "a") as maps_file:
                maps_file.write("{}\n".format(name_without_extension))
            self.commands.Whisper(sender, "{} has been downloaded!".format(name_without_extension))
            self.logger.info("{} has downloaded {}".format(sender, name_without_extension))
            self.handle(False)
        elif _map_.startwith("|") is True and _map_.endswith("|") is True:
            with open(self.maps) as maps_file:
                for map in maps_file.readlines():
                    if _map_ == map:
                        return self.commands.Whisper(sender, "{} already exists!".format(_map_))
            with open(self.maps, "a") as maps_file:
                maps_file.write(_map_)
            self.commands.Whisper(sender, "{} mode has been added!".format(_map_.replace("|", "")))
            self.logger.info("{} has added {}".format(sender, _map_))
            self.handle(False)
        else:
            self.commands.Whisper(sender, "No Map or Game mode was recognised in what you put!")





    def removeMap(self, sender, _map_):
        mapFound = False
        newMaps = ""
        with open(self.maps) as maps_file:
            for map in maps_file.readlines():
                if _map_ in map and mapFound is False:
                    removedMap = map
                    mapFound = True
                    continue
                elif _map_ in map and mapFound is True:
                    return self.commands.Whisper(sender, "More than 1 result came in for {}. Be more specific!".format(_map_))
                newMaps += "{}\n".format(map)
        if mapFound is False:
            self.commands.Whisper(sender, "No maps matched with {}".format(_map_))
        elif mapFound is True:
            with open(self.maps, "w") as maps:
                maps.write(newMaps)
            self.commands.Whisper("{} has been removed!".format(removedMap))
            self.logger.info("{} removed {}".format(sender, removedMap))
            self.handle(False)



    def addAdmin(self, sender, vaporId):
        if len(vaporId) != 36:
            return self.commands.Whisper(sender, "The vapor ID you entered is invalid")
        else:
            with open(self.admins) as admins_file:
                for admin in admins_file:
                    if vaporId == admin:
                        return self.commands.Whisper(sender, "The guy you tried to add is already an admin!")
            with open(self.admins, "a") as admins_file:
                admins_file.write("{}\n".format(vaporId))
            self.commands.Whisper("The guy has been added as an admin!")
            self.handle(False)



    def removeAdmin(self, sender, vaporId):
        if len(vaporId) != 36:
            return self.commands.Whisper(sender, "The vapor ID you entered is invalid")
        else:
            adminFound = False
            newAdmins = ""
            with open(self.admins) as admins_file:
                for admin in admins_file:
                    if admin == vaporId and adminFound is False:
                        adminFound = True
                        continue
                    newAdmins += "{}\n".format(admin)
            if adminFound is False:
                self.commands.Whisper(sender, "The guy you tried to remove is not an admin!")
            else:
                with open(self.admins, "w") as admins_file:
                    admins_file.write(newAdmins)
                self.commands.Whisper("The guy has been added as an admin!")
                self.handle(False)




    def handle(self, restart, name = None, password = None):
        if name is None:
            name = "{New Players ST Academy}"
        if password is None:
            password = ""
        start = '<?xml version="1.0" encoding="UTF-8"?>\n<ServerLauncherConfig ip="" upnpEnabled="true" updatePort="27275">\n  <servers>\n    <AltitudeServerConfig port="27279" downloadMaxKilobytesPerSecond="500" downloadHttpSource="" serverName="{}" maxPlayerCount="30" hardcore="true" autoBalanceTeams="false" preventTeamSwitching="true" disableBalanceTeamsPopup="true" lanServer="false" callEndOfRoundVote="true" disallowDemoUsers="false" rconEnabled="false" rconPassword="staftw" maxPing="1000" minLevel="0" maxLevel="0" secretCode="{}" cameraViewScalePercent="100">\n      <adminsByVaporID>\n'.format(self.quoteName(name), self.quoteName(password))
        admins = ""
        maps = ""
        with open(self.admins) as admins:
            admin_vapors = admins.readlines()
        with open(self.maps) as maps:
            map_names = maps.readlines()
        for admin in admin_vapors:
            admins += '        <UUID UUID="{}" />\n'.format(admin)
        for _map_ in map_names:
            maps += '        <String value="{}" />\n'.format(_map_)
        end = '      </mapList>\n      <mapRotationList>\n        <String value="lobby_sta" />\n      </mapRotationList>\n      <BotConfig numberOfBots="0" botDifficulty="MEDIUM" botsBalanceTeams="false" botSpectateThreshold="6" />\n      <disallowedPlaneRandomTypes />\n      <FreeForAllGameMode scoreLimit="0" RoundLimit="1" roundTimeSeconds="420" warmupTimeSeconds="10" />\n      <BaseDestroyGameMode RoundLimit="1" roundTimeSeconds="0" warmupTimeSeconds="10" />\n      <ObjectiveGameMode gamesPerRound="9" gamesPerSwitchSides="2" gameWinMargin="1" betweenGameTimeSeconds="6" RoundLimit="1" roundTimeSeconds="0" warmupTimeSeconds="10" />\n      <PlaneBallGameMode goalsPerRound="11" RoundLimit="1" roundTimeSeconds="0" warmupTimeSeconds="10" />\n      <TeamDeathmatchGameMode scoreLimit="0" RoundLimit="1" roundTimeSeconds="600" warmupTimeSeconds="10" />\n      <customCommands />\n      <consoleCommandPermissions>\n        <AltitudeServerConsoleCommandPermissions ConsoleCommand="balanceTeams">\n          <AllowedGroups>\n            <AltitudeConsoleGroup Group="Administrator" />\n          </AllowedGroups>\n        </AltitudeServerConsoleCommandPermissions>\n        <AltitudeServerConsoleCommandPermissions ConsoleCommand="changeMap">\n          <AllowedGroups>\n            <AltitudeConsoleGroup Group="Administrator" />\n          </AllowedGroups>\n        </AltitudeServerConsoleCommandPermissions>\n        <AltitudeServerConsoleCommandPermissions ConsoleCommand="custom">\n          <AllowedGroups>\n            <AltitudeConsoleGroup Group="Administrator" />\n          </AllowedGroups>\n        </AltitudeServerConsoleCommandPermissions>\n        <AltitudeServerConsoleCommandPermissions ConsoleCommand="drop">\n          <AllowedGroups>\n            <AltitudeConsoleGroup Group="Administrator" />\n          </AllowedGroups>\n        </AltitudeServerConsoleCommandPermissions>\n        <AltitudeServerConsoleCommandPermissions ConsoleCommand="kick">\n          <AllowedGroups>\n            <AltitudeConsoleGroup Group="Administrator" />\n          </AllowedGroups>\n        </AltitudeServerConsoleCommandPermissions>\n        <AltitudeServerConsoleCommandPermissions ConsoleCommand="startTournament">\n          <AllowedGroups>\n            <AltitudeConsoleGroup Group="Administrator" />\n          </AllowedGroups>\n        </AltitudeServerConsoleCommandPermissions>\n        <AltitudeServerConsoleCommandPermissions ConsoleCommand="stopTournament">\n          <AllowedGroups>\n            <AltitudeConsoleGroup Group="Administrator" />\n          </AllowedGroups>\n        </AltitudeServerConsoleCommandPermissions>\n        <AltitudeServerConsoleCommandPermissions ConsoleCommand="addBan">\n          <AllowedGroups>\n            <AltitudeConsoleGroup Group="Administrator" />\n          </AllowedGroups>\n        </AltitudeServerConsoleCommandPermissions>\n        <AltitudeServerConsoleCommandPermissions ConsoleCommand="addChatBlock">\n          <AllowedGroups>\n            <AltitudeConsoleGroup Group="Administrator" />\n          </AllowedGroups>\n        </AltitudeServerConsoleCommandPermissions>\n        <AltitudeServerConsoleCommandPermissions ConsoleCommand="assignTeam">\n          <AllowedGroups>\n            <AltitudeConsoleGroup Group="Administrator" />\n          </AllowedGroups>\n        </AltitudeServerConsoleCommandPermissions>\n        <AltitudeServerConsoleCommandPermissions ConsoleCommand="ban">\n          <AllowedGroups>\n            <AltitudeConsoleGroup Group="Administrator" />\n          </AllowedGroups>\n        </AltitudeServerConsoleCommandPermissions>\n        <AltitudeServerConsoleCommandPermissions ConsoleCommand="castBallot">\n          <AllowedGroups>\n            <AltitudeConsoleGroup Group="Administrator" />\n            <AltitudeConsoleGroup Group="Anonymous" />\n          </AllowedGroups>\n        </AltitudeServerConsoleCommandPermissions>\n        <AltitudeServerConsoleCommandPermissions ConsoleCommand="chatBlock">\n          <AllowedGroups>\n            <AltitudeConsoleGroup Group="Administrator" />\n          </AllowedGroups>\n        </AltitudeServerConsoleCommandPermissions>\n        <AltitudeServerConsoleCommandPermissions ConsoleCommand="listBans">\n          <AllowedGroups>\n            <AltitudeConsoleGroup Group="Administrator" />\n          </AllowedGroups>\n        </AltitudeServerConsoleCommandPermissions>\n        <AltitudeServerConsoleCommandPermissions ConsoleCommand="listChatBlocks">\n          <AllowedGroups>\n            <AltitudeConsoleGroup Group="Administrator" />\n          </AllowedGroups>\n        </AltitudeServerConsoleCommandPermissions>\n        <AltitudeServerConsoleCommandPermissions ConsoleCommand="listMaps">\n          <AllowedGroups>\n            <AltitudeConsoleGroup Group="Administrator" />\n          </AllowedGroups>\n        </AltitudeServerConsoleCommandPermissions>\n        <AltitudeServerConsoleCommandPermissions ConsoleCommand="listPlayers">\n          <AllowedGroups>\n            <AltitudeConsoleGroup Group="Administrator" />\n          </AllowedGroups>\n        </AltitudeServerConsoleCommandPermissions>\n        <AltitudeServerConsoleCommandPermissions ConsoleCommand="logPlanePositions">\n          <AllowedGroups>\n            <AltitudeConsoleGroup Group="Administrator" />\n          </AllowedGroups>\n        </AltitudeServerConsoleCommandPermissions>\n        <AltitudeServerConsoleCommandPermissions ConsoleCommand="logServerStatus">\n          <AllowedGroups>\n            <AltitudeConsoleGroup Group="Administrator" />\n          </AllowedGroups>\n        </AltitudeServerConsoleCommandPermissions>\n        <AltitudeServerConsoleCommandPermissions ConsoleCommand="modifyTournament">\n          <AllowedGroups>\n            <AltitudeConsoleGroup Group="Administrator" />\n          </AllowedGroups>\n        </AltitudeServerConsoleCommandPermissions>\n        <AltitudeServerConsoleCommandPermissions ConsoleCommand="nextMap">\n          <AllowedGroups>\n            <AltitudeConsoleGroup Group="Administrator" />\n          </AllowedGroups>\n        </AltitudeServerConsoleCommandPermissions>\n        <AltitudeServerConsoleCommandPermissions ConsoleCommand="overrideBallScore">\n          <AllowedGroups>\n            <AltitudeConsoleGroup Group="Administrator" />\n          </AllowedGroups>\n        </AltitudeServerConsoleCommandPermissions>\n        <AltitudeServerConsoleCommandPermissions ConsoleCommand="overrideSpawnPoint">\n          <AllowedGroups>\n            <AltitudeConsoleGroup Group="Administrator" />\n          </AllowedGroups>\n        </AltitudeServerConsoleCommandPermissions>\n        <AltitudeServerConsoleCommandPermissions ConsoleCommand="rconPassword">\n          <AllowedGroups>\n            <AltitudeConsoleGroup Group="Administrator" />\n            <AltitudeConsoleGroup Group="Anonymous" />\n          </AllowedGroups>\n        </AltitudeServerConsoleCommandPermissions>\n        <AltitudeServerConsoleCommandPermissions ConsoleCommand="removeBan">\n          <AllowedGroups>\n            <AltitudeConsoleGroup Group="Administrator" />\n          </AllowedGroups>\n        </AltitudeServerConsoleCommandPermissions>\n        <AltitudeServerConsoleCommandPermissions ConsoleCommand="removeChatBlock">\n          <AllowedGroups>\n            <AltitudeConsoleGroup Group="Administrator" />\n          </AllowedGroups>\n        </AltitudeServerConsoleCommandPermissions>\n        <AltitudeServerConsoleCommandPermissions ConsoleCommand="serverMessage">\n          <AllowedGroups>\n            <AltitudeConsoleGroup Group="Administrator" />\n          </AllowedGroups>\n        </AltitudeServerConsoleCommandPermissions>\n        <AltitudeServerConsoleCommandPermissions ConsoleCommand="serverRequestPlayerChangeServer">\n          <AllowedGroups>\n            <AltitudeConsoleGroup Group="Administrator" />\n          </AllowedGroups>\n        </AltitudeServerConsoleCommandPermissions>\n        <AltitudeServerConsoleCommandPermissions ConsoleCommand="serverWhisper">\n          <AllowedGroups>\n            <AltitudeConsoleGroup Group="Administrator" />\n          </AllowedGroups>\n        </AltitudeServerConsoleCommandPermissions>\n        <AltitudeServerConsoleCommandPermissions ConsoleCommand="testCameraViewScale">\n          <AllowedGroups>\n            <AltitudeConsoleGroup Group="Administrator" />\n          </AllowedGroups>\n        </AltitudeServerConsoleCommandPermissions>\n        <AltitudeServerConsoleCommandPermissions ConsoleCommand="testDisableWeaponMode">\n          <AllowedGroups>\n            <AltitudeConsoleGroup Group="Administrator" />\n          </AllowedGroups>\n        </AltitudeServerConsoleCommandPermissions>\n        <AltitudeServerConsoleCommandPermissions ConsoleCommand="testDS">\n          <AllowedGroups>\n            <AltitudeConsoleGroup Group="Administrator" />\n          </AllowedGroups>\n        </AltitudeServerConsoleCommandPermissions>\n        <AltitudeServerConsoleCommandPermissions ConsoleCommand="testEM">\n          <AllowedGroups>\n            <AltitudeConsoleGroup Group="Administrator" />\n          </AllowedGroups>\n        </AltitudeServerConsoleCommandPermissions>\n        <AltitudeServerConsoleCommandPermissions ConsoleCommand="testGravityMode">\n          <AllowedGroups>\n            <AltitudeConsoleGroup Group="Administrator" />\n          </AllowedGroups>\n        </AltitudeServerConsoleCommandPermissions>\n        <AltitudeServerConsoleCommandPermissions ConsoleCommand="testHealthModifier">\n          <AllowedGroups>\n            <AltitudeConsoleGroup Group="Administrator" />\n          </AllowedGroups>\n        </AltitudeServerConsoleCommandPermissions>\n        <AltitudeServerConsoleCommandPermissions ConsoleCommand="testPlaneScale">\n          <AllowedGroups>\n            <AltitudeConsoleGroup Group="Administrator" />\n          </AllowedGroups>\n        </AltitudeServerConsoleCommandPermissions>\n        <AltitudeServerConsoleCommandPermissions ConsoleCommand="vote">\n          <AllowedGroups>\n            <AltitudeConsoleGroup Group="Administrator" />\n          </AllowedGroups>\n        </AltitudeServerConsoleCommandPermissions>\n      </consoleCommandPermissions>\n    </AltitudeServerConfig>\n  </servers>\n</ServerLauncherConfig>\n\n'
        config = '{}{}      <mapList>\n{}{}'.format(start, admins, maps, end)
        with open(self.config, "w") as conf:
            conf.write(config)
        if restart is False:
            self.commands.Message("Server configuration was changed and the server will be restarted!")
        else:
            self.commands.Message("Restarting server...")
        chdir("..")
        call("./start.sh", shell=True)
        sleep(1000)