from random import choice

class Map:
    def __init__(self, logger, commands_object):
        self.logger = logger
        self.commands = commands_object
        self.ball_maps = ["ball_arcade",
                          "ball_asteroids",
                          "ball_atmosphere",
                          "ball_cave",
                          "ball_cavern",
                          "ball_channelpark",
                          "ball_core",
                          "ball_cross",
                          "ball_darkwar ",
                          "ball_factory",
                          "ball_football",
                          "ball_fracas",
                          "ball_funnelpark",
                          "ball_gliderpark",
                          "ball_greywar",
                          "ball_grotto",
                          "ball_hardcourt",
                          "ball_ice",
                          "ball_labyrinth",
                          "ball_lostcity",
                          "ball_mayhem2",
                          "ball_maze",
                          "ball_meteroids",
                          "ball_pixelized",
                          "ball_planepark",
                          "ball_powder",
                          "ball_proton",
                          "ball_reef",
                          "ball_skylands",
                          "ball_snow",
                          "ball_tron",
                          "ball_ufo",
                          "ball_volcano"]
        self.tbd_maps = ["tbd_assembly",
                         "tbd_asteroids",
                         "tbd_cave",
                         "tbd_cavern",
                         "tbd_channelpark",
                         "tbd_chess",
                         "tbd_core",
                         "tbd_fallout",
                         "tbd_focus",
                         "tbd_fracas",
                         "tbd_gliderpark",
                         "tbd_greywar",
                         "tbd_grotto",
                         "tbd_heights",
                         "tbd_hills",
                         "tbd_justice",
                         "tbd_locomotion",
                         "tbd_lostcity",
                         "tbd_mayhem",
                         "tbd_meteroids",
                         "tbd_middleground",
                         "tbd_nuclear",
                         "tbd_origami_park",
                         "tbd_planepark",
                         "tbd_powder",
                         "tbd_proton",
                         "tbd_scrapyard",
                         "tbd_underpark",
                         "tbd_volcano",
                         "tbd_woods"]
        self.onedm_maps = ["1dm_asteroids",
                           "1dm_asteroids2",
                           "1dm_cave",
                           "1dm_cave2",
                           "1dm_clocktower",
                           "1dm_core",
                           "1dm_fallout",
                           "1dm_grotto",
                           "1dm_locomotion",
                           "1dm_lostcity",
                           "1dm_mayhem",
                           "1dm_mayhem2",
                           "1dm_middleground",
                           "1dm_woods"]

    def ball(self):
        self.commands.ChangeMap(choice(self.ball_maps))

    def tbd(self):
        self.commands.ChangeMap(choice(self.tbd_maps))

    def onedm(self):
        self.commands.ChangeMap(choice(self.onedm_maps))