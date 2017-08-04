def find_word(word, char, position):
	'Find the char in the gived position'
	if char == word[position]:
		return True
	else:
		return False

if __name__ == '__main__':
	was = find_word('example', 'p', 4)
	print was

