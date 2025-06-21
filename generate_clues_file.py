# Generate detected clue tuples file
from puzzle_reader import ListenerPuzzleReader

reader = ListenerPuzzleReader('Listener grid 4869.png', 'Listener 4869 clues.png')
reader.extract_clues()

with open('detected_clues_tuples.txt', 'w') as f:
    all_clues = []
    for direction in ['ACROSS', 'DOWN']:
        for clue in reader.clues[direction]:
            all_clues.append(clue)
    all_clues.sort(key=lambda x: x.number)
    for clue in all_clues:
        f.write(f"Clue {clue.number} {clue.direction}: {clue.cell_indices}\n")

print("Generated detected_clues_tuples.txt with all 24 clues") 