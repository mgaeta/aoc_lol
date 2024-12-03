package problems

import (
	"fmt"
	"regexp"
	"strconv"
	"strings"
	"y24/src/utils"
)

const mulSting = `mul\(\d{1,3},\d{1,3}\)`
const doString = `do\(\)`
const dontSting = `don't\(\)`

func Solve3a(test bool) string {
	fmt.Println("Problem 2a:")
	data := utils.Read(utils.GetInputFileName(dayNumber, test))

	output := 0
	lines := utils.GetStrings(data)
	for _, lineString := range lines {
		if verbose {
			fmt.Println(lineString)
		}
		r := regexp.MustCompile(mulSting)
		matches := r.FindAllString(lineString, -1)
		for _, match := range matches {
			parts := strings.Split(match[4:len(match)-1], ",")
			part0, err := strconv.Atoi(parts[0])
			if err != nil {
				panic(err)
			}
			part1, err := strconv.Atoi(parts[1])
			if err != nil {
				panic(err)
			}
			output += part0 * part1
		}

	}

	return strconv.Itoa(output)
}

func Solve3b(test bool) string {
	fmt.Println("Problem 2b:")
	data := utils.Read(utils.GetInputFileName(dayNumber, test))

	// the solution is going to look like consuming one mul at a time.
	// once I have a new string I need to look at rest
	// run three checks: do, don't, and mul
	// only use whichever is first!

	output := 0
	on := true
	lines := utils.GetStrings(data)
	for _, lineString := range lines {
		if verbose {
			fmt.Println(lineString)
		}
		r0 := regexp.MustCompile(mulSting)
		r1 := regexp.MustCompile(doString)
		r2 := regexp.MustCompile(dontSting)
		for {
			locPair0 := r0.FindStringIndex(lineString)
			locPair1 := r1.FindStringIndex(lineString)
			locPair2 := r2.FindStringIndex(lineString)

			// No more tokens
			if locPair0 == nil && locPair1 == nil && locPair2 == nil {
				break
			}

			var loc0, loc1, loc2 int
			if locPair0 == nil {
				loc0 = 1000000000
			} else {
				loc0 = locPair0[0]
			}

			if locPair1 == nil {
				loc1 = 1000000000
			} else {
				loc1 = locPair1[0]
			}

			if locPair2 == nil {
				loc2 = 1000000000
			} else {
				loc2 = locPair2[0]
			}
			if verbose {
				fmt.Printf("%d,%d,%d\n", loc0, loc1, loc2)
				fmt.Printf(lineString + "\n")
			}

			if loc0 < loc1 && loc0 < loc2 {
				start, end := locPair0[0], locPair0[1]
				match := lineString[start:end]
				parts := strings.Split(match[4:len(match)-1], ",")
				part0, err := strconv.Atoi(parts[0])
				if err != nil {
					panic(err)
				}
				part1, err := strconv.Atoi(parts[1])
				if err != nil {
					panic(err)
				}
				if verbose {
					fmt.Println("about to add", part0, part1, on)
				}
				if on {
					output += part0 * part1
				}

				if end >= len(lineString)-1 {
					break
				}
				lineString = lineString[end:]
			} else if loc1 < loc0 && loc1 < loc2 {
				_, end := locPair1[0], locPair1[1]
				on = true
				lineString = lineString[end:]
			} else if loc2 < loc0 && loc2 < loc1 {
				// Here was the bug
				_, end := locPair2[0], locPair2[1]
				on = false
				lineString = lineString[end:]
			} else {
				panic("on no!!!!!!!!!!")
			}
		}
	}

	return strconv.Itoa(output)
}
