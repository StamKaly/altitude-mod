from altitude import run


run.Run("27279", "/home/user/altitude-files/servers/command.txt", "/home/user/altitude-files/servers/log.txt",
        "/home/user/altitude-files/servers/log_old.txt", "/home/user/altitude-files/servers/logs_archive.txt",
        "../server-files/files/chat_logs.txt", True).run()
