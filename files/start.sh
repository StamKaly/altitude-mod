echo ">>> Killing mod..."
pkill -9 python3
echo " "
echo ">>> Killing server..."
pkill -9 java
echo " "
cd /home/user/altitude/altitude-mod
echo ">>> Updating mod..."
git pull
echo " "
echo ">>> Updating lobby, game.jar, config and custom commands"
python3 ./files/update_with_server.py
echo " "
echo ">>> Starting mod, appending mod logs to ./server-files/outputs/mod.out"
nohup python3 main.py &> /home/user/altitude/server-files/outputs/mod.out &
echo " "
cd ..
echo ">>> Launching server, appending launcher's logs to ./server-files/outputs/server_launcher-logs.out"
nohup /home/user/altitude-files/server_launcher &> /home/user/altitude/server-files/outputs/server_launcher-logs.out &
echo " "
sleep 2
echo ">>> Creating symlinks: ./server-files/files: logs.txt, logs_archive.txt, commands.txt"
rm /home/user/altitude/server-files/files/logs.txt
rm /home/user/altitude/server-files/files/logs_archive.txt
rm /home/user/altitude/server-files/files/commands.txt
ln -s /home/user/altitude-files/servers/log.txt /home/user/altitude/server-files/files/logs.txt
ln -s /home/user/altitude-files/servers/logs_archive.txt /home/user/altitude/server-files/files/logs_archive.txt
ln -s /home/user/altitude-files/servers/command.txt /home/user/altitude/server-files/files/commands.txt
echo " "
exit 0
