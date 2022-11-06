git add -A
DESCRIPTION=$(gum write --placeholder "Details of this change (CTRL+D to finish)")
gum confirm "Commit changes?" && git commit -m "$DESCRIPTION" 
	