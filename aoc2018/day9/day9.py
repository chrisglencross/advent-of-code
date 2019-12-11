from blist import blist

marbles = blist()
marbles.append(0)
current_index = 0

marble = 1

players = 477
last_marble = 70851 * 100

player_scores = [0 for i in range(0, players)]
for marble in range(1, last_marble + 1):
    if marble % 23 != 0:
        index = (current_index + 2) % len(marbles)
        if index == 0:
            marbles.append(marble)
            current_index = len(marbles) - 1
        else:
            marbles.insert(index, marble)
            current_index = index
    else:
        player_scores[marble % players] = player_scores[marble % players] + marble
        index_to_remove = (current_index + len(marbles) - 7) % len(marbles)
        marble_to_remove = marbles[index_to_remove]
        player_scores[marble % players] = player_scores[marble % players] + marble_to_remove
        del marbles[index_to_remove]
        current_index = index_to_remove
    if marble % 10000 == 0:
        print(100 * marble / last_marble)
    # print(marbles)
    # print(current_index)

print(player_scores)
print(sorted(player_scores, reverse=True)[0])
