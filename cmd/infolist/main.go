package main

import (
	"flag"
	"fmt"
	"os"
	
	"github.com/tonygilkerson/infolist/internal/infolist"
)

// main is the entry point to the infolist app
func main() {

	//
	// Get Env Vars
	//

	// Get location to the info list date (yaml format)
	infoListDataPath := os.Getenv("INFOLIST_DATA")
	if len(infoListDataPath) == 0 {
		infoListDataPath = "/home/tgilkerson/gitlab-dle/anthony.gilkerson/notebook/infolist/infolist-data.yaml"
	}
	fmt.Printf("INFOLIST_DATA path: %v\n\n", infoListDataPath)

	//
	// Flags
	//

	// Find command
	inFlag := flag.String("in","any","find in [ any | name | desc | note | tags ]")
	showNoteFlag := flag.Bool("note",false,"Show notes field")
	

	// Customize the -h / --help output
	flag.Usage = func() {
		fmt.Fprintf(os.Stderr, "Usage: %s [flags] <command> [subcommand]\n\n", os.Args[0])
		fmt.Fprintf(os.Stderr, "Commands:\n")
		fmt.Fprintf(os.Stderr, "  find     Find filter string\n")
		fmt.Fprintf(os.Stderr, "Flags:\n")
		flag.PrintDefaults()
	}

	flag.Parse()
	args := flag.Args()
	cmd := "find" // default command
	arg := ""

	// Keep it simple assume one command and one argument: `$infolist <cmd> <arg>`

	if len(args) > 0 {
		cmd = args[0]
	} 
	if len(args) > 1 {
		arg = args[1]
	} 
	
	// for now lets just accept one argument plus flags
	// if len(args) > 1 {
	// 	// Capture all remaining arguments
	// 	mod = args[1]
	// }

	//
	// Load data
	//
	notes := infolist.New()
	err := notes.LoadFromFile(infoListDataPath)
	if err != nil {
		panic(err)
	}

	//
	// Switch on the subcommand
	// 
	switch cmd {
	case "find":
		fmt.Printf("Find '%v' in '%s' field:\n\n", arg, *inFlag )
		found,filteredNotes := notes.Find(arg,*inFlag)
		if found {
			infolist.PrintNotes(filteredNotes,*showNoteFlag)
		} 

	case "list":
		infolist.PrintNotes(notes,*showNoteFlag)

	case "tags":
		notes.ListTags()

	case "peek":
		notes.Peek(arg)
		
		
	default:
		fmt.Printf("Unknown command: %s\n", os.Args[1])
		flag.Usage()
		os.Exit(1)
	}
	

	// Done
	fmt.Printf("\nDone.\n")

}