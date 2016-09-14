from .teachers import teachers

class Permissions:
    def __init__(self, logger, commands, players, state):
        self.logger = logger
        self.commands = commands
        self.players = players
        self.state = state
        self.teachers = teachers.Handler(logger)


    def get_permission(self, vaporId):
        return self.teachers.get_permission(vaporId)

    def on_spawn(self, playerId):
        if self.state is True:
            if self.teachers.teachers_check_existence(self.players.vapor_from_id(playerId)) is True:
                return
            level, ace = self.players.get_level_and_ace(playerId)
            if ace == 0 and level <= 59:
                return
            else:
                nickname = self.players.nickname_from_id(playerId)
                self.commands.AssignTeam(nickname, "spec")
                self.commands.Whisper(nickname, "Only Newbies and Teachers can spawn right now!")



    def on_clientAdd(self, nickname, vaporId, level, ace):
        permission = self.teachers.update(nickname, vaporId)
        if self.state is True:
            if permission is None and ace > 0 and level >= 59:
                self.teachers.add_banned(nickname, vaporId)
                self.commands.ChatBlock(nickname, "AllChat", 20, "forever",
                                        "Only teachers and unbanned players can now talk. Ask Stam for a probable reveal")
        return permission


    def on_nicknameChange(self, newNickname):
        vaporId = self.players.vapor_from_nickname(newNickname)
        self.teachers.update(newNickname, vaporId)


    def setServerMode(self, sender, mode):
        sender_nickname = self.players.nickname_from_vapor(sender)
        if mode == "Newbies and Teachers":
            if self.state is False:
                self.state = True
                self.commands.Whisper(sender_nickname, "Mode is set successfully! Only teachers and newbies will be able to spawn!")
            else:
                self.commands.Whisper(sender_nickname, "This mode is already in use right now, maybe you meant everyone?")
        elif mode == "Everyone":
            if self.state is True:
                self.state = False
                self.commands.Whisper(sender_nickname, "Mode is set successfully! Everyone will be able to spawn!")
            else:
                self.commands.Whisper(sender_nickname, "This mode is already in use right now, maybe you meant newbies and teachers?")


    def addTeacher(self, sender, nickname):
        vaporId = self.players.vapor_from_nickname(nickname)
        sender_nickname = self.players.nickname_from_vapor(sender)
        add = self.teachers.add_teacher(vaporId, nickname = nickname)
        if add == "exists":
            self.commands.Whisper(sender_nickname,
                                  "{} is already a teacher!".format(nickname))
        elif add == "added":
            self.commands.Whisper(sender_nickname,
                                  "{} has been added as a teacher!".format(nickname))



    def addTeacherWithVapor(self, sender, vaporId):
        sender_nickname = self.players.nickname_from_vapor(sender)
        if len(vaporId) != 36:
            self.commands.Whisper(sender_nickname,
                                  "The vapor you entered is invalid!")
        else:
            add = self.teachers.add_teacher(vaporId)
            if add == "exists":
                self.commands.Whisper(sender_nickname,
                                      "The player you tried to add is already a teacher!")
            elif add == "added":
                self.commands.Whisper(sender_nickname,
                                      "The player has been added as a teacher!")


    def removeTeacher(self, sender, nickname):
        vapor = self.players.vapor_from_nickname(nickname)
        sender_nickname = self.players.nickname_from_vapor(sender)
        remove = self.teachers.remove_teacher(vapor)
        if remove == "not found":
            self.commands.Whisper(sender_nickname,
                                  "{} is not yet a teacher!".format(nickname))
        elif remove == "deleted":
            self.commands.Whisper(sender_nickname,
                                  "{} is not a teacher anymore!".format(nickname))



    def removeTeacherWithNickname(self, sender, partial_nickname):
        vaporId = self.teachers.get_vapor_from_teachers(partial_nickname)
        sender_nickname = self.players.nickname_from_vapor(sender)
        if vaporId == "not found":
            self.commands.Whisper(sender_nickname,
                                  "{} was not found, try being more specific!".format(partial_nickname))
        elif str(vaporId).startswith("found") is True:
            _, number, _ = vaporId
            self.commands.Whisper(sender_nickname,
                                  "{} matches were found, be more specific!".format(number))
        else:
            self.teachers.remove_teacher(vaporId[1])
            self.commands.Whisper(sender_nickname,
                                  "{} is not a teacher anymore!".format(vaporId[0]))



    def listTeachers(self, sender):
        sender_nickname = self.players.nickname_from_vapor(sender)
        teacher = self.teachers.get_teachers()
        if teacher is None:
            self.commands.Whisper(sender_nickname,
                                  "There are no teachers right now.")
        else:
            number, messages = teacher
            self.commands.Whisper(sender_nickname, "There are {} teachers:".format(number))
            self.commands.Multiple_Whispers(sender_nickname, messages)




    def removeBan(self, sender, nickname):
        vaporId = self.players.vapor_from_nickname(nickname)
        sender_nickname = self.players.nickname_from_vapor(sender)
        remove = self.teachers.remove_banned(vaporId)
        if remove == "not found":
            self.commands.Whisper(sender_nickname, "{} is not banned!".format(nickname))
        elif remove == "deleted":
            self.teachers.write_unbanned(nickname, vaporId)
            self.commands.RemoveChatBlock(vaporId, "AllChat")
            self.commands.Whisper(sender_nickname, "{}'s ban has been removed!".format(nickname))



    def removeBanWithNickname(self, sender, partial_nickname):
        vaporId = self.teachers.get_vapor_from_banned(partial_nickname)
        sender_nickname = self.players.nickname_from_vapor(sender)
        if vaporId == "not found":
            self.commands.Whisper(sender_nickname,
                                  "{} was not found, try being more specific!".format(partial_nickname))
        elif str(vaporId).startswith("found") is True:
            _, number, _ = vaporId
            self.commands.Whisper(sender_nickname,
                                  "{} matches were found, be more specific!".format(number))
        else:
            self.teachers.remove_banned(vaporId[1])
            self.teachers.write_unbanned(vaporId[0], vaporId[1])
            self.commands.RemoveChatBlock(vaporId[1], "AllChat")
            self.commands.Whisper(sender_nickname, "{}'s ban has been removed!".format(vaporId[0]))


    def addBan(self, sender, nickname):
        vaporId = self.players.vapor_from_nickname(nickname)
        sender_nickname = self.players.nickname_from_vapor(sender)
        banned = self.teachers.add_banned(nickname, vaporId)
        if banned == "exists":
            self.commands.Whisper(sender_nickname, "{} is already banned!".format(nickname))
        else:
            self.teachers.remove_unbanned(vaporId)
            self.commands.ChatBlock(nickname, "AllChat", 20, "forever", "You aren't allowed to talk")
            self.commands.Whisper(sender_nickname, "{} is now banned!".format(nickname))



    def addBanWithVapor(self, sender, vaporId):
        sender_nickname = self.players.nickname_from_vapor(sender)
        if len(vaporId) != 36:
            self.commands.Whisper(sender_nickname, "The vapor you entered is invalid!")
        else:
            nickname = self.teachers.remove_unbanned(vaporId)
            if nickname == "not found":
                self.commands.Multiple_Whispers(sender_nickname, ["Unbanned player not found.",
                                                                  "With this you can only ban someone you had unbanned."])
            else:
                self.teachers.add_banned(nickname, vaporId)
                self.commands.AddChatBlock(vaporId, "AllChat", 20, "forever", "You aren't allowed to talk")
                self.commands.Whisper(sender_nickname, "{} is now banned!".format(nickname))



    def listBans(self, sender):
        sender_nickname = self.players.nickname_from_vapor(sender)
        ban = self.teachers.get_banned()
        if ban is None:
            self.commands.Whisper(sender_nickname,
                                  "There are no bans right now.")
        else:
            number, messages = ban
            self.commands.Whisper(sender_nickname, "There are {} bans:".format(number))
            self.commands.Multiple_Whispers(sender_nickname, messages)


    def listUnbanned(self, sender):
        sender_nickname = self.players.nickname_from_vapor(sender)
        unban = self.teachers.get_unbanned()
        if unban is None:
            self.commands.Whisper(sender_nickname,
                                  "There are no people unbanned right now.")
        else:
            number, messages = unban
            self.commands.Whisper(sender_nickname, "There are {} people unbanned:".format(number))
            self.commands.Multiple_Whispers(sender_nickname, messages)
