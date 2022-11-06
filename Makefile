all:
	@echo "\nAvailable commnads:"
	@echo ">> test : runs all tests" | sed 's/^/   /'
	@echo ">> commit : commits all changes to git" | sed 's/^/   /'
test:
	-@pytest --no-header -v

commit:
	
	git add -A
	DESCRIPTION=$$(gum write --placeholder "Details of this change (CTRL+D to finish)");\
	gum confirm "Commit changes?" && git commit -m "$$DESCRIPTION" 
	