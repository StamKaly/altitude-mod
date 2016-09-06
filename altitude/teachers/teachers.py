import sqlite3

class Handler:
    def __init__(self, logger):
        self.logger = logger
        self.connection = sqlite3.connect("./altitude/teachers/teachers.database")
        self.cursor = self.connection.cursor()

    def banned_check_existence(self, vaporId):
        for row in self.cursor.execute("SELECT 1 FROM Banned WHERE vaporId = ?", (vaporId,)):
            if row == (1,):
                return True
        return False


    def unbanned_check_existence(self, vaporId):
        for row in self.cursor.execute("SELECT 1 FROM Unbanned WHERE vaporId = ?", (vaporId,)):
            if row == (1,):
                return True
        return False


    def teachers_check_existence(self, vaporId):
        for row in self.cursor.execute("SELECT 1 FROM Teachers WHERE vaporId = ?", (vaporId,)):
            if row == (1,):
                return True
        return False


    def update(self, nickname, vaporId):
        if self.unbanned_check_existence(vaporId) is True:
            self.cursor.execute("UPDATE Unbanned SET nickname = ? WHERE vaporId = ?", (nickname, vaporId,))
            permission = "unbanned"
        elif self.banned_check_existence(vaporId) is True:
            self.cursor.execute("UPDATE Banned SET nickname = ? WHERE vaporId = ?", (nickname, vaporId,))
            permission = "banned"
        elif self.teachers_check_existence(vaporId) is True:
            self.cursor.execute("UPDATE Teachers SET nickname = ? WHERE vaporId = ?", (nickname, vaporId,))
            permission = "teacher"
        else:
            permission = None
        self.connection.commit()
        return permission


    def write_unbanned(self, nickname, vaporId):
        unbanned = self.unbanned_check_existence(vaporId)
        banned = self.banned_check_existence(vaporId)
        if unbanned is True and banned is False:
            return "exists"
        elif unbanned is True and banned is True:
            self.remove_banned(vaporId)
            self.logger.warn("Possible bug, {} was both in banned and in unbanned table in teachers.database, "
                             "he is removed from banned now though to avoid any conflicts".format(nickname))
            return "conflict"
        elif unbanned is False and banned is False:
            self.cursor.execute("INSERT INTO Unbanned VALUES(?, ?)", (nickname, vaporId,))
            self.connection.commit()


    def remove_unbanned(self, vaporId):
        unbanned = self.unbanned_check_existence(vaporId)
        if unbanned is False:
            return "not found"
        else:
            self.cursor.execute("SELECT nickname FROM Unbanned WHERE vaporId = ?", (vaporId,))
            (nickname,), = self.cursor.fetchone()
            self.cursor.execute("DELETE FROM Unbanned WHERE vaporId = ?", (vaporId,))
            self.connection.commit()
            return nickname



    def add_teacher(self, vaporId, nickname = None):
        if self.teachers_check_existence(vaporId) is True:
            return "exists"
        else:
            if self.banned_check_existence(vaporId) is True:
                self.remove_banned(vaporId)
            if self.unbanned_check_existence(vaporId) is True:
                self.remove_unbanned(vaporId)
            if nickname is None:
                self.cursor.execute("INSERT INTO Teachers VALUES(NULL, ?)", (vaporId,))
            else:
                self.cursor.execute("INSERT INTO Teachers VALUES(?, ?)", (nickname, vaporId,))
            self.connection.commit()
            return "added"



    def remove_teacher(self, vaporId):
        if self.teachers_check_existence(vaporId) is False:
            return "not found"
        else:
            self.cursor.execute("DELETE FROM Teachers WHERE vaporId = ?", (vaporId,))
            self.connection.commit()
            return "deleted"



    def add_banned(self, nickname, vaporId):
        if self.banned_check_existence(vaporId) is True:
            return "exists"
        else:
            self.cursor.execute("INSERT INTO Banned VALUES(?, ?)", (nickname, vaporId,))
            self.connection.commit()
            return "added"


    def remove_banned(self, vaporId):
        if self.banned_check_existence(vaporId) is False:
            return "not found"
        else:
            self.cursor.execute("DELETE FROM Banned WHERE vaporId = ?", (vaporId,))
            self.connection.commit()
            return "deleted"


    def get_teachers(self):
        self.cursor.execute("SELECT nickname FROM Teachers")
        teachers = self.cursor.fetchall()
        if len(teachers) == 0:
            return None
        messages = []
        number = 1
        for row in teachers:
            if row[0] != None:
                messages.append('{}) {}'.format(number, row[0]))
                number += 1
            else:
                continue
        if len(messages) == 0:
            return None
        return number, messages


    def get_unbanned(self):
        self.cursor.execute("SELECT nickname FROM Unbanned")
        unbanned = self.cursor.fetchall()
        if len(unbanned) == 0:
            return None
        messages = []
        number = 1
        for row in unbanned:
            if row[0] != None:
                messages.append('{}) {}'.format(number, row[0]))
                number += 1
            else:
                continue
        if len(messages) == 0:
            return None
        return number, messages



    def get_banned(self):
        self.cursor.execute("SELECT nickname FROM Banned")
        banned = self.cursor.fetchall()
        if len(banned) == 0:
            return None
        messages = []
        number = 1
        for row in banned:
            if row[0] != None:
                messages.append('{}) {}'.format(number, row[0]))
                number += 1
            else:
                continue
        if len(messages) == 0:
            return None
        return number, messages


    def get_vapor_from_teachers(self, nickname):
        matches = []
        self.cursor.execute("SELECT nickname, vaporId FROM Teachers")
        players = self.cursor.fetchall()
        for row in players:
            try:
                if nickname in row[0]:
                    matches.append([row[0], row[1]])
            except TypeError:
                continue
        if len(matches) == 0:
            return "not found"
        elif len(matches) == 1:
            return matches[0]
        else:
            return "found {} matches".format(len(matches))


    def get_vapor_from_banned(self, nickname):
        matches = []
        self.cursor.execute("SELECT nickname, vaporId FROM Banned")
        players = self.cursor.fetchall()
        for row in players:
            try:
                if nickname in row[0]:
                    matches.append([row[0], row[1]])
            except TypeError:
                continue
        if len(matches) == 0:
            return "not found"
        elif len(matches) == 1:
            return matches[0]
        else:
            return "found {} matches".format(len(matches))