all:
	@echo "\nAvailable commnads:"
	@echo ">> test : runs all tests" | sed 's/^/   /'
test:
	pytest --no-header -v