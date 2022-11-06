help:
	@echo "\nAvailable commnads:"
	@echo ">> test : runs all tests" | sed 's/^/   /'
	@echo ">> commit : commits all changes to git" | sed 's/^/   /'
test:
	##implement make tests but ok well, we'll get there eventually

commit:
	@git add -A
	@DESCRIPTION=$$(gum write --placeholder "Details of this change (CTRL+D to finish)");\
	gum confirm "Commit changes?" && git commit -m "$$DESCRIPTION"
	git push origin master #wrap this in if else: https://stackoverflow.com/questions/15977796/if-conditions-in-a-makefile-inside-a-target
	