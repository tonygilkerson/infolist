package infolist

import (
	"fmt"
	"maps"
	"os"
	"slices"
	"strings"

	"gopkg.in/yaml.v3"
)

// NoteItem maps to each block in infolist
type Note struct {
	Name        string   `yaml:"Name"`
	Tags        []string `yaml:"Tags"`
	Description string   `yaml:"Description"`
	Note        string   `yaml:"Note"`
}

// List of notes
type Notes []Note

// New creates and initializes an empty Notes slice.
func New() Notes {
	return make(Notes, 0)
}

// LoadNotes reads a YAML file from the given path and unmarshals it into a slice of NoteItem structs.
func (notes *Notes) LoadFromFile(filePath string) error {
	data, err := os.ReadFile(filePath)
	if err != nil {
		return fmt.Errorf("failed to read file: %w", err)
	}

	err = yaml.Unmarshal(data, &notes)
	if err != nil {
		return fmt.Errorf("failed to unmarshal yaml: %w", err)
	}

	return nil
}

// FindInAny will look for the filter string in all Note fields.
func (notes *Notes) Find(filter string, findIn string) (bool, Notes) {

	var filteredNotes Notes

	for _, note := range *notes {


		// found in name?
		if findIn == "any" || findIn == "name" {
			if strings.Contains(strings.ToLower(note.Name), strings.ToLower(filter)) {
				filteredNotes = append(filteredNotes, note)
				continue
			}
		}

		// found in description?
		if findIn == "any" || findIn == "desc" {
			if strings.Contains(strings.ToLower(note.Description), strings.ToLower(filter)) {
				filteredNotes = append(filteredNotes, note)
				continue
			}
		}
		
		// found in note?
		if findIn == "any" || findIn == "note" {
			if strings.Contains(strings.ToLower(note.Note), strings.ToLower(filter)) {
				filteredNotes = append(filteredNotes, note)
				continue
			}
		}

		// found in tags?
		if findIn == "any" || findIn == "tags" {
			tags := strings.Join(note.Tags, ", ")
			if strings.Contains(strings.ToLower(tags), strings.ToLower(filter)) {
				filteredNotes = append(filteredNotes, note)
				continue
			}
		}
	}

	if len(filteredNotes) > 0 {
		return true, filteredNotes
	}

	// No results fond
	return false, nil
}


// Peek will look for the filter string in all Note fields.
func (notes *Notes) Peek(filter string) {

	var results []string
	var found bool
	divider := strings.Repeat("-", 100)

	for _, note := range *notes {

		results = nil
		found = false

		// found in name?
		if strings.Contains(strings.ToLower(note.Name), strings.ToLower(filter)) {
			found = true
		}
		
		// found in description?
		if strings.Contains(strings.ToLower(note.Description), strings.ToLower(filter)) {
			results = append(results, fmt.Sprintf("Desc: %s",note.Description))
			found = true
		}
		
		// found in note?
		if strings.Contains(strings.ToLower(note.Note), strings.ToLower(filter)) {
			results = append(results, "Note:")
			results = append(results, getContext(note.Note,filter,))
			found = true
		}
		
		// found in tags?
		tags := strings.Join(note.Tags, ", ")
		if strings.Contains(strings.ToLower(tags), strings.ToLower(filter)) {
			results = append(results, fmt.Sprintf("Tags: %s",tags))
			found = true
		}

		if found {
			fmt.Printf("%s\n", divider)
			fmt.Printf("Name: %s\n", note.Name)
			for _,line := range results {
				fmt.Printf("%s\n", line)
			}
		}
	}
	if found {
		fmt.Printf("%s\n", divider)
	}

}


// ListTags will print a unique list of tags
func (notes *Notes) ListTags() {

	seen := make(map[string]struct{})

	for _,note := range *notes {
		for _,tag := range note.Tags {
			seen[tag] = struct{}{} 
		}
	}

	// Extract map keys directly into a slice
	uniqueTags := slices.Collect(maps.Keys(seen))
	slices.Sort(uniqueTags)

	fmt.Printf("Unique list of tags seen:\n\n")
	for _,tag := range uniqueTags {
		fmt.Printf("%s\n",tag)
	}

}


// PrintNotes will print the list of notes
func PrintNotes(notes Notes, showNote bool) {

	divider := strings.Repeat("-", 100)
	colDiv := strings.Repeat("-", 35)
	printHeader := true

	for _, note := range notes {
		tagsStr := strings.Join(note.Tags, ", ")

		if showNote {
			if printHeader {
				fmt.Printf("%s\n",divider)
				printHeader = false
			}
			fmt.Printf("Name: %s\nTags: %v\nDesc: %s\nNote:\n%s\n%s\n",
				note.Name, note.Tags, note.Description, note.Note, divider)
		} else {
			if printHeader {
				fmt.Printf("%-40s %-35s %s\n", "Name","Tags","Descriptions")
				fmt.Printf("%-40s %-35s %s\n", colDiv,colDiv,colDiv)
				printHeader = false
			}
			fmt.Printf("%-40s %-35s %s\n", truncate(note.Name, 40), truncate(tagsStr, 35), note.Description)
		}

	}
}

// Helper to truncate text so long strings don't break the column layout
func truncate(s string, maxLen int) string {
	if len(s) > maxLen {
		return s[:maxLen-3] + "..."
	}
	return s
}

// GetContext searches for target in multiLineStr and return
// the matching line along with its preceding and succeeding lines.
func getContext(multiLineStr string, target string) string {
	// Split the multi-line string into individual lines
	lines := strings.Split(multiLineStr, "\n")
	totalLines := len(lines)

	for i, line := range lines {
		var context string

		// Case-sensitive check (use strings.ToLower for case-insensitive)
		if strings.Contains(strings.ToLower(line), strings.ToLower(target)) {

			// Line BEFORE (check upper boundary)
			if i > 0 {
				context = fmt.Sprintf("%s\n", lines[i-1])
			} 

			// MATCHING Line
			context = context + fmt.Sprintf(">>>%s\n", line)

			// Line AFTER (check lower boundary)
			if i < totalLines-1 {
				context = context + fmt.Sprintf("%s\n", lines[i+1])
			} 

			// return context
			return context
		}
	}

	return ""
}