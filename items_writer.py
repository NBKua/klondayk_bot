from game_state.item_reader import GameItemReader

if __name__ == '__main__':
    reader = GameItemReader()
    reader.read('items.txt')
    reader.pretty_write('pretty_items.txt')
