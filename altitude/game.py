class Game:
    def __init__(self, logger, players_object, planes_object, plane_positions_object, commands_object):
        self.logger = logger
        self.players = players_object
        self.planes = planes_object
        self.planePositions = plane_positions_object
        self.commands = commands_object
        self.current_mode = ""
        self.current_map = ""


    def get_logs_object(self, logs_object):
        self.log = logs_object




    def on_position(self):
        if self.current_map == "asteroids":
            for sublist in self.planePositions.plane_positions:
                x, y = sublist[1]
                if 1780 < x < 1820 and 641 < y < 681:
                    self.commands.Whisper(self.players.nickname_from_id(sublist[0]), "Works so nice!!!")
                    self.log.getPositions = False




    def on_mode_change(self):
        if self.current_mode == "ball":
            self.planes.messagesToSend = ["Shoot the Ball into the goal to score and don't forget to pass!",
                                          "Press S or the middle mouse button in order to use the ball or any other powerup."]


    def on_map_change(self):
        if self.current_map == "asteroids":
            #self.log.getPositions = True
            self.planes.messagesToSend.append("This is the most common and loved map in Altitude!")


    def check_current_mode_and_map(self, full_map):
        mode, mapName = full_map.split("_")
        if mode != self.current_mode:
            self.current_mode = mode
            self.on_mode_change()
        if mapName != self.current_map:
            self.current_map = mapName
            self.on_map_change()