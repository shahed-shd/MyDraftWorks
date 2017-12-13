if [[ -e Resource_links.txt ]] ; then
	echo 'The "readme.txt" file exists.'
	echo 'Second line.'
	#./slnk
	./sym_link
else
	echo 'The "readme.txt" file does not exist.'
fi