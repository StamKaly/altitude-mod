import sqlite3


class Reader:
    def __init__(self, logger):
        self.connection = sqlite3.connect('./altitude/players_database/players.database')
        self.cursor = self.connection.cursor()
        self.logger = logger
        self.best_in_ball = []
        self.best_in_football = []
        self.best_in_1dm = []
        self.best_in_tbd = []
        self.most_goals = 0
        self.most_f_goals = 0
        self.most_kills = 0
        self.most_bases_destroyed = 0



    def get_existence(self, vaporId):
        for row in self.cursor.execute("SELECT 1 FROM Players WHERE vaporId = ?", (vaporId,)):
            if row == (1,):
                return True
        return False


    def get_troller(self, IP):
        self.cursor.execute("SELECT 1 FROM Players WHERE IP = ?", (IP,))
        if len(self.cursor.fetchall()) > 1:
            return True
        return False


    def get_vapor_from_ip(self, IP):
        ip = IP.split(":")[0]
        self.cursor.execute("SELECT vaporId FROM Players WHERE ip = ?", (ip,))
        (vaporId,) = self.cursor.fetchone()
        return vaporId


    def add_or_check(self, nickname, vaporId, IP, check):
        ip = IP.split(":")[0]
        if self.get_existence(vaporId) is True:
            if check is True and self.get_troller(ip) is True:
                return "troll"
            self.cursor.execute("UPDATE Players SET nickname = ? WHERE vaporId = ?", (nickname, vaporId,))
            self.connection.commit()
            self.logger.info("{}'s nickname is updated in the database".format(nickname))
            return "updated"
        else:
            self.cursor.execute("INSERT INTO Players VALUES(?, ?, ?, 0, 0, 0, 0)", (nickname, vaporId, ip,))
            self.connection.commit()
            self.logger.info("{} is added to the database".format(nickname))
            if check is True and self.get_troller(ip) is True:
                return "troll"
            return "added"



    def on_nickname_change(self, oldNickname, newNickname):
        self.cursor.execute("UPDATE Players SET nickname = ? WHERE nickname = ?", (newNickname, oldNickname,))
        self.connection.commit()
        self.logger.info("{}'s nickname is changed to {} in the database".format(oldNickname, newNickname))



    def reset_values(self):
        self.cursor.execute("UPDATE Players SET goals = 0")
        self.cursor.execute("UPDATE Players SET f_goals = 0")
        self.cursor.execute("UPDATE Players SET kills = 0")
        self.cursor.execute("UPDATE Players SET bases = 0")
        self.connection.commit()
        self.best_in_ball = []
        self.best_in_football = []
        self.best_in_1dm = []
        self.best_in_tbd = []
        self.logger.info("Goals, kills and bases scores are reset in the database")


    def add_kill(self, vaporId):
        self.logger.info("Database   -   Selecting kills from players where vaporId is {}".format(vaporId))
        self.cursor.execute("SELECT kills FROM Players WHERE vaporId = ?", (vaporId,))
        (kills,) = self.cursor.fetchone()
        kills += 1
        self.cursor.execute("UPDATE Players SET kills = ? WHERE vaporId = ?", (kills, vaporId,))
        self.connection.commit()



    def add_base(self, vaporId):
        self.logger.info("Database   -   Selecting bases from players where vaporId is {}".format(vaporId))
        self.cursor.execute("SELECT bases FROM Players WHERE vaporId = ?", (vaporId,))
        (bases,) = self.cursor.fetchone()
        bases += 1
        self.cursor.execute("UPDATE Players SET bases = ? WHERE vaporId = ?", (bases, vaporId))
        self.connection.commit()
        self.logger.info("Someone destroyed another one of those bases and his score is added to the database")



    def add_goal(self, vaporId):
        self.logger.info("Database   -   Selecting goals from players where vaporId is {}".format(vaporId))
        self.cursor.execute("SELECT goals FROM Players WHERE vaporId = ?", (vaporId,))
        (goals,) = self.cursor.fetchone()
        goals += 1
        self.cursor.execute("UPDATE Players SET goals = ? WHERE vaporId = ?", (goals, vaporId,))
        self.connection.commit()
        self.logger.info("Someone scored another goal and his score is added to the database")


    def add_f_goal(self, vaporId):
        self.logger.info("Database   -   Selecting f_goals from players where vaporId is {}".format(vaporId))
        self.cursor.execute("SELECT f_goals FROM Players WHERE vaporId = ?", (vaporId,))
        (f_goals,) = self.cursor.fetchone()
        f_goals += 1
        self.cursor.execute("UPDATE Players SET f_goals = ? WHERE vaporId = ?", (f_goals, vaporId,))
        self.connection.commit()
        self.logger.info("Someone scored another goal in football and his score is added to the database")


    def get_most_goals(self):
        try:
            self.cursor.execute("SELECT nickname, goals FROM Players")
            players = []
            for row in self.cursor.fetchall():
                players.append([row[0], row[1]])
            goals = [arg[1] for arg in players]
            most_goals = max(goals)
            if most_goals != 0:
                self.best_in_ball = []
                for sublist in players:
                    if most_goals == sublist[1]:
                        self.best_in_ball.append(sublist[0])
                self.logger.info("{} has/have scored the most goals = {}".format(self.best_in_ball, most_goals))
                self.most_goals = most_goals
            return self.best_in_ball
        except ValueError:
            return []




    def get_most_f_goals(self):
        try:
            self.cursor.execute("SELECT nickname, f_goals FROM Players")
            players = []
            for row in self.cursor.fetchall():
                players.append([row[0], row[1]])
            f_goals = [arg[1] for arg in players]
            most_f_goals = max(f_goals)
            if most_f_goals != 0:
                self.best_in_football = []
                for sublist in players:
                    if most_f_goals == sublist[1]:
                        self.best_in_football.append(sublist[0])
                self.logger.info("{} has/have scored the most goals in football = {}".format(self.best_in_ball, most_f_goals))
                self.most_f_goals = most_f_goals
            return self.best_in_football
        except ValueError:
            return []




    def get_most_kills(self):
        try:
            self.cursor.execute("SELECT nickname, kills FROM Players")
            players = []
            for row in self.cursor.fetchall():
                players.append([row[0], row[1]])
            kills = [arg[1] for arg in players]
            most_kills = max(kills)
            if most_kills != 0:
                self.best_in_1dm = []
                for sublist in players:
                    if most_kills == sublist[1]:
                        self.best_in_1dm.append(sublist[0])
                self.logger.info("{} has/have killed the most = {}".format(self.best_in_1dm, most_kills))
                self.most_kills = most_kills
            return self.best_in_1dm
        except ValueError:
            return []



    def get_demolition_expert(self):
        try:
            self.cursor.execute("SELECT nickname, bases FROM Players")
            players = []
            for row in self.cursor.fetchall():
                players.append([row[0], row[1]])
            bases = [arg[1] for arg in players]
            most_bases_destroyed = max(bases)
            if most_bases_destroyed != 0:
                self.best_in_tbd = []
                for sublist in players:
                    if most_bases_destroyed == sublist[1]:
                        self.best_in_tbd.append(sublist[0])
                self.logger.info("{} has/have destroyed the most bases = {}".format(self.best_in_tbd, most_bases_destroyed))
                self.most_bases_destroyed = most_bases_destroyed
            return self.best_in_tbd
        except ValueError:
            return []



    def myStats(self, vaporId, mode):
        if mode == "Ball":
            self.cursor.execute("SELECT goals FROM Players WHERE vaporId = ?", (vaporId,))
            (goals,) = self.cursor.fetchone()
            if goals == 0:
                return "You haven't scored any goals in Ball today."
            else:
                return "You have scored {} goals in Ball today!".format(goals)
        elif mode == "Football":
            self.cursor.execute("SELECT f_goals FROM Players WHERE vaporId = ?", (vaporId,))
            (f_goals,) = self.cursor.fetchone()
            if f_goals == 0:
                return "You haven't scored any goals in Football today."
            else:
                return "You have scored {} goals in Football today!".format(f_goals)
        elif mode == "1dm":
            self.cursor.execute("SELECT kills FROM Players WHERE vaporId = ?", (vaporId,))
            (kills,) = self.cursor.fetchone()
            if kills == 0:
                return "You haven't killed anyone in 1dm today."
            else:
                return "You have killed {} planes in 1dm today!".format(kills)
        elif mode == "TBD":
            self.cursor.execute("SELECT bases FROM Players WHERE vaporId = ?", (vaporId,))
            (bases,) = self.cursor.fetchone()
            if bases == 0:
                return "You haven't destroyed any bases in TBD today."
            else:
                return "You have destroyed {} bases in TBD today!".format(bases)