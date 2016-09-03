class Game:
    def __init__(self, logger, players_object, planes_object, plane_positions_object, commands_object, database):
        self.logger = logger
        self.players = players_object
        self.planes = planes_object
        self.planePositions = plane_positions_object
        self.commands = commands_object
        self.database = database
        self.current_mode = "lobby"
        self.current_map = "sta"
        self.best_in_ball = self.database.get_most_goals()
        self.best_in_1dm = self.database.get_most_kills()
        self.best_in_tbd = self.database.get_demolition_expert()
        self.most_goals = self.database.most_goals
        self.most_kills = self.database.most_kills
        self.most_bases_destroyed = self.database.most_bases_destroyed
        self.message_for_best_in_ball = []
        self.message_for_best_in_1dm = []
        self.message_for_best_in_tbd = []
        self.message_for_roundEnd_in_ball = []
        self.message_for_roundEnd_in_1dm = []


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
            self.planes.messagesToSend = ["Press S to use the Ball or any other powerup."]
            if len(self.message_for_best_in_ball) != 0:
                for row in self.message_for_best_in_ball:
                    self.planes.messagesToSend.append(row)
            if len(self.planes.messagesToSend) == 1:
                self.planes.messagesToSend.append('There is no player of the day in Ball yet.')
                self.planes.messagesToSend.append('Be the first one!')
        elif self.current_mode == "tbd":
            self.planes.messagesToSend = ['Destroy the base with the bomb, press S to use the bomb.']
            if len(self.message_for_best_in_tbd) != 0:
                for row in self.message_for_best_in_tbd:
                    self.planes.messagesToSend.append(row)
            if len(self.planes.messagesToSend) == 1:
                self.planes.messagesToSend.append('There is no player of the day in TBD yet.')
                self.planes.messagesToSend.append('Be the first one!')
        elif self.current_mode == "1dm":
            self.planes.messagesToSend = ["Kill as many planes as you can and try not to die."]
            if len(self.message_for_best_in_1dm) != 0:
                for row in self.message_for_best_in_1dm:
                    self.planes.messagesToSend.append(row)
            if len(self.planes.messagesToSend) == 1:
                self.planes.messagesToSend.append('There is no player of the day in 1dm yet.')
                self.planes.messagesToSend.append('Be the first one!')
        elif self.current_mode == "lobby" and self.players.lobby_loaded is False:
            self.planes.messagesToSend = ['This is the lobby, when there are 2 or more players here,',
                                          'use the command "/match <gameMode>" in the chat to',
                                          'start a vote for a new match! (Enter to open the chat)']
        else:
            self.players.lobby_loaded = False


    def on_map_change(self):
        if self.current_map == "asteroids":
            #self.log.getPositions = True
            #self.planes.messagesToSend.append("This is the most common and loved map in Altitude!")
            return


    def reset_scores(self):
        self.best_in_ball = []
        self.best_in_1dm = []
        self.best_in_tbd = []
        self.most_goals = 0
        self.most_kills = 0
        self.most_bases_destroyed = 0
        self.message_for_best_in_ball = []
        self.message_for_best_in_1dm = []
        self.message_for_best_in_tbd = []
        self.database.reset_values()



    def on_roundEnd(self):
        if self.current_mode == "ball":
            self.commands.Multiple_Messages(self.message_for_roundEnd_in_ball)
        elif self.current_mode == "1dm":
            self.commands.Multiple_Messages(self.message_for_roundEnd_in_1dm)


    def on_goal(self, playerId):
        nickname = self.players.nickname_from_id(playerId)
        self.logger.info("Player's ID who scored goal: {}, vapor: {}".format(playerId, self.players.vapor_from_id(playerId)))
        self.database.add_goal(self.players.vapor_from_id(playerId))
        database_best_in_ball = self.database.get_most_goals()
        database_most_goals = self.database.most_goals
        if len(database_best_in_ball) <= 1:
            if self.best_in_ball != database_best_in_ball:
                self.message_for_roundEnd_in_ball = ["New player of the day in Ball:", "{} - {} Goals".format(nickname,
                                                                                            database_most_goals)]
                self.message_for_best_in_ball = ['Player of the day in Ball:', '{} - {} Goals'.format(nickname,
                                                                                                      database_most_goals)]
            if self.best_in_ball == database_best_in_ball:
                if self.most_goals != database_most_goals:
                    self.message_for_roundEnd_in_ball = ["New record from {},".format(nickname), "the player of the day in Ball: {} Goals".format(
                                                                                                               database_most_goals)]
                    self.message_for_best_in_ball = ['Player of the day in Ball:', '{} - {} Goals'.format(nickname,
                                                                                                          database_most_goals)]
        elif len(database_best_in_ball) > 1:
            players = len(database_best_in_ball)
            if self.best_in_ball != database_best_in_ball:
                self.message_for_best_in_ball = []
                self.message_for_roundEnd_in_ball = []
                self.message_for_roundEnd_in_ball.append("There are now {} players of the day in Ball".format(players))
                self.message_for_roundEnd_in_ball.append("with {} Goals:".format(database_most_goals))
                self.message_for_best_in_ball.append("Players of the day in Ball with {} Goals:".format(database_most_goals))
                for number in range(players):
                    self.message_for_roundEnd_in_ball.append("{}) {}".format(number+1, database_best_in_ball[number]))
                    self.message_for_best_in_ball.append("{}) {}".format(number+1, database_best_in_ball[number]))
        self.best_in_ball = database_best_in_ball
        self.most_goals = database_most_goals
                




    def on_base_destroy(self, playerId):
        nickname = self.players.nickname_from_id(playerId)
        self.database.add_base(self.players.vapor_from_id(playerId))
        database_best_in_tbd = self.database.get_demolition_expert()
        database_most_bases_destroyed = self.database.most_bases_destroyed
        if len(database_best_in_tbd) <= 1:
            if self.best_in_tbd != database_best_in_tbd:
                self.commands.Multiple_Messages(["New player of the day in TBD:", "{} - {} Bases Destroyed".format(nickname,
                                                                                            database_most_bases_destroyed)])
                self.message_for_best_in_tbd = ['Player of the day in TBD:', '{} - {} Bases Destroyed'.format(nickname,
                                                                                                      database_most_bases_destroyed)]
            if self.best_in_tbd == database_best_in_tbd:
                if self.most_bases_destroyed != database_most_bases_destroyed:
                    self.commands.Multiple_Messages(["New record from {},".format(nickname), "the player of the day in TBD: {} Bases Destroyed".format(
                                                                                                               database_most_bases_destroyed)])
                    self.message_for_best_in_tbd = ['Player of the day in TBD:', '{} - {} Bases Destroyed'.format(nickname,
                                                                                                          database_most_bases_destroyed)]
        elif len(database_best_in_tbd) > 1:
            players = len(database_best_in_tbd)
            if self.best_in_tbd != database_best_in_tbd:
                self.message_for_best_in_tbd = []
                self.commands.Multiple_Messages(["There are now {} players of the day in TBD".format(players),
                                       "with {} Bases Destroyed:".format(database_most_bases_destroyed)])
                self.message_for_best_in_tbd.append(
                    "Players of the day in TBD with {} Bases Destroyed:".format(database_most_bases_destroyed))
                for number in range(players):
                    self.commands.Message("{}) {}".format(number + 1, database_best_in_tbd[number]))
                    self.message_for_best_in_tbd.append("{}) {}".format(number + 1, database_best_in_tbd[number]))
        self.best_in_tbd = database_best_in_tbd
        self.most_bases_destroyed = database_most_bases_destroyed






    def on_kill(self, playerId):
        if self.current_mode == "1dm" and playerId >= 0:
            nickname = self.players.nickname_from_id(playerId)
            self.database.add_kill(self.players.vapor_from_id(playerId))
            database_best_in_1dm = self.database.get_most_kills()
            database_most_kills = self.database.most_kills
            if len(database_best_in_1dm) <= 1:
                if self.best_in_1dm != database_best_in_1dm:
                    self.message_for_roundEnd_in_1dm = ["New player of the day in 1dm:", "{} - {} Kills".format(nickname,
                                                                                                              database_most_kills)]
                    self.message_for_best_in_1dm = ['Player of the day in 1dm:', '{} - {} Kills'.format(nickname,
                                                                                                          database_most_kills)]
                if self.best_in_1dm == database_best_in_1dm:
                    if self.most_kills != database_most_kills:
                        self.message_for_roundEnd_in_1dm = ["New record from {},".format(nickname),
                                                             "the player of the day in 1dm: {} Kills".format(
                                                                 database_most_kills)]
                        self.message_for_best_in_1dm = ['Player of the day in 1dm:', '{} - {} Kills'.format(nickname,
                                                                                                              database_most_kills)]
            elif len(database_best_in_1dm) > 1:
                players = len(database_best_in_1dm)
                if self.best_in_1dm != database_best_in_1dm:
                    self.message_for_best_in_1dm = []
                    self.message_for_roundEnd_in_1dm = []
                    self.message_for_roundEnd_in_1dm.append("There are now {} players of the day in 1dm".format(players))
                    self.message_for_roundEnd_in_1dm.append("with {} Kills:".format(database_most_kills))
                    self.message_for_best_in_1dm.append(
                        "Players of the day in 1dm with {} Kills:".format(database_most_kills))
                    for number in range(players):
                        self.message_for_roundEnd_in_1dm.append("{}) {}".format(number + 1, database_best_in_1dm[number]))
                        self.message_for_best_in_1dm.append("{}) {}".format(number + 1, database_best_in_1dm[number]))
            self.best_in_1dm = database_best_in_1dm
            self.most_kills = database_most_kills




    def check_current_mode_and_map(self, full_map):
        try:
            mode, mapName = full_map.split("_")
        except ValueError:
            mode, mapName1, mapName2 = full_map.split("_")
            mapName = mapName1 + mapName2
        if mode != self.current_mode:
            self.current_mode = mode
            self.on_mode_change()
        if mapName != self.current_map:
            self.current_map = mapName
            self.on_map_change()