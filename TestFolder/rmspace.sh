 #!/bin/bash

function usage() {
	echo "USAGE is"
}


function get_max_int()
{
	# This function gets the maximum integer value that system supports.

	local mx x=1

	for (( p = 1; x > 0 ; ++p )) ; do
		mx="$x"
		x=$(( (1 << p) - 1 ))
	done

	echo "$mx"
}


function get_depth()
{
	# Function to calculate depth of a file or directory from a starting path.
	# It requires 3 arguments as follows:
	# (1) The starting path, (2) the path to calculate depth, (3) wheather the path to calculate depth is directory or not.
	# If starting path is relative path, path to calculate depth has to be relative path.
	# If starting path is absolute path, path to calculate depth has to be absolute path.
	# Ex: get_depth a/b a/b/c/d/e true
	#     returns 3

	local from_path="$1"
	local path_to_calculate_depth="$2"
	local is_dir_path_to_calculate_depth="$3"	# boolean true or false
	
	# append '/' if necessary
	if [ "${from_path: -1}" != '/' ] ; then
		from_path="$from_path/"
	fi

	# append '/' if necessary
	if "$is_dir_path_to_calculate_depth" && [ "${path_to_calculate_depth: -1}" != '/' ] ; then
		path_to_calculate_depth="$path_to_calculate_depth/"
	fi

	# Remove FROM_PATH from PATH_TO_CALCULATE_DEPTH
	path_to_calculate_depth=${path_to_calculate_depth#$from_path}
	local depth

	if [ -z "$path_to_calculate_depth" ] ; then
		depth=0
	else
		# Remove trailing '/' if exists
		if [ "${path_to_calculate_depth: -1}" == '/' ] ; then
			path_to_calculate_depth=${path_to_calculate_depth::-1}
		fi

		# Count the number of occurance of '/'
		depth=$( echo "$path_to_calculate_depth" | grep -o '/' | wc -l )
		depth=$(( ++depth ))	# Increment by 1
	fi

	echo "$depth"
}

function ask_yes_or_no()
{
	local ans
	read ans

	if [ "$ans" == 'Y' ] || [ "$ans" == 'y' ] ; then
		return 0
	else
		return 1
	fi
}


function perform_renaming()
{
	# This function performs renaming for this script.
	# It takes 2 arguments as follows:
	# (1) path to the directory which contains the file to be renamed (2) the file name to be renamed.
	# Ex: perform_renaming a/b/c f
	#		here f can be either file or folder name which is in a/b/c directory.

	local file_dir="$1"
	local file_name="$2"

	local to_replace="$opt_replace"
	local replace_with="$opt_replacewith"

	local file_name_to_be=$( echo "$file_name" | sed "s/$to_replace/$replace_with/g" )

	# append '/' if necessary
	if [ "${file_dir: -1}" != '/' ] ; then
		file_dir="$file_dir/"
	fi

	# Prompt if interactive mood is enabled.
	if "$opt_interactive" ; then
		local file_or_dir='FILE'
		if [ -d "$file_dir$file_name" ] ; then
			file_or_dir='DIRECTORY'
		fi

		echo ""
		echo "IN DIRECTORY \"$file_dir\""
		echo "RENAME $file_or_dir \"$file_name\" TO \"$file_name_to_be\" ? [Y/n]"

		if ! ask_yes_or_no ; then
			return 0
		fi
	fi

	mv "$file_dir$file_name" "$file_dir$file_name_to_be"

	# If verbose or interactive mood enabled.
	if "$opt_verbose" || "$opt_interactive" ; then
		echo "'$file_name' -> '$file_name_to_be'"
	fi

	return 0
}


function travarse()
{
	# This function travarses directories through breadth first search (BFS) style
	# It takes 2 arguments as follows:
	# (1) starting directory path (2) maximum depth to travarse

	local start_dir="$1"
	local maxdepth="$2"

	# append '/' if necessary
	if [ "${start_dir: -1}" != '/' ] ; then
		start_dir="$start_dir/"
	fi

	local dir_stack=("$start_dir")
	local hold_IFS="$IFS"	# IFS is a built-in variable
	IFS=$'\n'				# Modify IFS value temporarily

	while [ "${#dir_stack[@]}" -gt 0 ] ; do
		local work_path=${dir_stack[-1]}
		unset 'dir_stack[-1]'

		local content_list=$( ls -1A --group-directories-first "$work_path" )

		for content in $content_list ; do
			local content_full_path="$work_path$content"

			local is_dir=false
			if [ -d "$content_full_path" ] ; then
				is_dir=true
			fi

			local depth=$( get_depth "$start_dir" "$content_full_path" "$is_dir" )
			if [ "$depth" -gt "$maxdepth" ] ; then
				echo "DEBUG max depth continue"
				continue
			fi

			# Checking selection from options
			if [ "${content:0:1}" == '.' ] && ( ! "$opt_all" ) ; then
				continue
			fi

			if [ -f "$content_full_path" ] && ( ! "$opt_all" ) && ( ! "$opt_files" ) ; then
				continue
			fi

			if "$is_dir" && ( ! "$opt_all" ) && ( ! "$opt_directories" ) ; then
				continue
			fi

			# Checking if space found
			if [[ $content =~ $opt_replace ]] ; then
				perform_renaming "$work_path" "$content"
			fi
		done

		# Push directories to the stack
		local directory_list=$( ls -Apr "$work_path" | grep '/' )
		
		for directory in $directory_list ; do
			dir_stack+=("$work_path$directory")
		done
	done

 	IFS="$hold_IFS"		# Regain the previous value
}


# Checking availability of GNU enhanced getopt
getopt --test > /dev/null
if [ $? -ne 4 ] ; then
	echo 'getopt --test failed in this environment, GNU enhanced getopt is not found.'
	exit 1
fi

# Parse options with getopt
OPTIONS=rp:m:vidfa
LONGOPTIONS=recursive,path:,maxdepth:,verbose,interactive,directories,files,all,replace:,replacewith:

PARSED=$( getopt --options="$OPTIONS" --longoptions="$LONGOPTIONS" --name "$0" -- "$@" )
if [ $? -ne 0 ] ; then
	# then getopt has complained about wrong arguments to stdout'
	exit 2
fi

eval set -- "$PARSED"

# Assign option variables.
opt_recursive=false
opt_path=$( pwd )
opt_maxdepth=1
opt_maxdepth_found=false
opt_verbose=false
opt_interactive=false
opt_directories=false
opt_files=false
opt_all=false
opt_replace=$' '
opt_replacewith='_'

while  true ; do
	case "$1" in
		-r | --recursive )
 			opt_recursive=true
 			shift
 			;;
 		-p | --path )
 			opt_path="$2"
 			shift 2
 			;;
 		-m | --maxdepth )
 			opt_maxdepth="$2"
 			opt_maxdepth_found=true
 			shift 2
 			;;
 		-v | --verbose )
 			opt_verbose=true
 			shift
 			;;
 		-i | --interactive )
 			opt_interactive=true
 			shift
 			;;
 		-d | --directories )
 			opt_directories=true
 			shift
 			;;
 		-f | --files )
 			opt_files=true
 			shift
 			;;
 		-a | --all )
 			opt_all=true
 			shift
 			;;
 		--replace )
 			opt_replace="$2"
 			shift 2
 			;;
 		--replacewith )
 			opt_replacewith="$2"
 			shift 2
 			;;
 		-- )
 			shift
 			break
 			;;
 		* )
 			echo "options $1 is not recognized."
 			exit 3
 			;;
	esac
done

if "$opt_recursive" && ( ! "$opt_maxdepth_found" ) ; then
	opt_maxdepth=$( get_max_int )
fi

# Travarse and perform renaming
travarse "$opt_path" "$opt_maxdepth"
