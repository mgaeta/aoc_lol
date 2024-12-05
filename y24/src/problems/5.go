package problems

import (
	"fmt"
	"strconv"
	"strings"
	"y24/src/utils"
)

func Solve5a(data string, verbose bool) string {
	output := 0
	greaterThans, updates := parseData(data, verbose)

	for _, update := range updates {
		if firstInvalid(update, greaterThans, verbose) == -1 {
			output += getMiddleElement(update)
		}
	}

	return strconv.Itoa(output)
}

func firstInvalid(
	input []int,
	greaterThans map[int][]int,
	verbose bool,
) int {
	// There can be indirect relationships.
	for i := 0; i < len(input)-1; i++ {
		current, next := input[i], input[i+1]

		found := false
		allGreaterThan := findAllGreaterThan(current, greaterThans, verbose)
		if verbose {
			fmt.Println("current", current, "next", next)
			fmt.Println("allGreaterThan", allGreaterThan)
		}
		for _, element := range allGreaterThan {
			if verbose {
				fmt.Println("element", element, "next", next)
			}
			if element == next {
				found = true
				break
			}
		}
		if !found {
			if verbose {
				fmt.Println("Not found", current, next)
			}
			return i
		}
	}
	return -1
}

func parseData(data string, verbose bool) (map[int][]int, [][]int) {
	lines := utils.GetStrings(data)
	mode := 0

	greaterThans := make(map[int][]int, 0)
	updates := make([][]int, 0)
	for _, line := range lines {
		if mode == 0 {
			if line == "" {
				mode = 1
				if verbose {
					fmt.Println("greaterThans", greaterThans)
				}
				continue
			}
			parts := strings.Split(line, "|")
			firstString, secondString := parts[0], parts[1]

			first, err := strconv.Atoi(firstString)
			if err != nil {
				panic(err)
			}

			second, err := strconv.Atoi(secondString)
			if err != nil {
				panic(err)
			}

			found, ok := greaterThans[first]
			if !ok {
				found = make([]int, 0)
			}
			greaterThans[first] = append(found, second)
		} else {
			intList := make([]int, 0)
			for _, s := range strings.Split(line, ",") {
				x, err := strconv.Atoi(s)
				if err != nil {
					panic(err)
				}
				intList = append(intList, x)
			}
			updates = append(updates, intList)
		}
	}
	return greaterThans, updates
}

func getMiddleElement(input []int) int {
	return input[len(input)/2]
}

func findAllGreaterThan(
	input int,
	greaterThans map[int][]int,
	verbose bool,
) []int {
	output := make([]int, 0)
	queue := make([]int, 0)
	queue = append(queue, input)
	for len(queue) > 0 {
		next := queue[0]
		queue = queue[1:]
		if verbose {
			fmt.Println("next", next, "length", len(queue))
		}
		foundElements, ok := greaterThans[next]
		if !ok {
			// this is the "largest" so return nothing
			continue
		}
		for _, element := range foundElements {
			output = append(output, element)
		}
	}

	return output
}

func repair(input []int, greaterThans map[int][]int, verbose bool) []int {
	output := make([]int, len(input))
	copy(output, input)
	for {
		found := firstInvalid(output, greaterThans, verbose)
		if found == -1 {
			break
		}

		temp := output[found]
		output[found] = output[found+1]
		output[found+1] = temp
	}
	return output
}

func Solve5b(data string, verbose bool) string {
	output := 0

	greaterThans, updates := parseData(data, verbose)
	for _, update := range updates {
		if firstInvalid(update, greaterThans, verbose) != -1 {
			update = repair(update, greaterThans, verbose)
			output += getMiddleElement(update)
		}
	}

	return strconv.Itoa(output)
}
