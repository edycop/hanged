list_event = []

def event_consumer(event):
	"list_event"
	while True:
		location = yield location
		print(location)

def main():
	consumer = event_consumer()
	consumer.start()

if __name__ == '__main__':
	main()