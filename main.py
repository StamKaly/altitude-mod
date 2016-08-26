import json
with open("log.txt") as log_file:
    logs = log_file.readlines()



players = ['0', '1', '2']
real_players = []


for line in logs:
    try:
        decoded = json.loads(line)
    except json.decoder.JSONDecodeError:
        continue
    if 'message' in line: 
        print(decoded['message'])
    if 'positionByPlayer' in line:
        for arg in players:
            print(decoded['positionByPlayer'][arg])
    if 'logServerStatus' in line:
        player_list = [decoded["nicknames"], decoded["vaporIds"], decoded["playerIds"], decoded["ips"]]
        count = 0
        for _ in range(len(decoded["ips"])):
            player = [player[count] for player in player_list]
            real_players.append(player)
            count += 1
        print(real_players)
    with open("log.txt", 'w'):
        pass