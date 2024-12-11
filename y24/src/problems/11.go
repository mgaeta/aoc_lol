package problems

import (
	"errors"
	"fmt"
	"strconv"
	"strings"
	"y24/src/utils"
)

func splitInt(input int, verbose bool) (int, int, error) {
	inputString := strconv.Itoa(input)
	if len(inputString)%2 == 0 {
		part0 := inputString[(len(inputString) / 2):]
		part1 := inputString[:(len(inputString) / 2)]

		p0, err := strconv.Atoi(part0)
		if err != nil {
			return 0, 0, err
		}
		p1, err := strconv.Atoi(part1)
		if err != nil {
			return 0, 0, err
		}

		if verbose {
			fmt.Println(input, p0, p1)
		}

		return p0, p1, nil

	} else {
		return 0, 0, errors.New("input is not even")
	}
}

var memo = make(map[string]int)

func howManyWillThisBecome(stone int, stepsRemaining int, verbose bool) int {
	if stepsRemaining == 0 {
		return 1
	}
	token := utils.EncodeTuple(stone, stepsRemaining)
	if found, ok := memo[token]; ok {
		return found
	}
	if stone == 0 {
		output := howManyWillThisBecome(1, stepsRemaining-1, verbose)
		memo[token] = output
		return output
	}

	a, b, err := splitInt(stone, verbose)
	if err == nil {
		output := howManyWillThisBecome(a, stepsRemaining-1, verbose) + howManyWillThisBecome(b, stepsRemaining-1, verbose)
		memo[token] = output
		return output
	}

	output := howManyWillThisBecome(stone*2024, stepsRemaining-1, verbose)
	memo[token] = output
	return output
}

func Solve11(data string, steps int, verbose bool) string {
	lines := utils.GetStrings(data)
	stones := make([]int, 0)
	for _, partString := range strings.Split(lines[0], " ") {
		part, err := strconv.Atoi(partString)
		if err != nil {
			panic(err)
		}
		stones = append(stones, part)
	}

	output := 0
	for _, stone := range stones {
		output += howManyWillThisBecome(stone, steps, false)
	}

	return strconv.Itoa(output)
}

func Solve11a(data string, verbose bool) string {
	return Solve11(data, 25, verbose)
}

func Solve11b(data string, verbose bool) string {
	output := Solve11(data, 75, verbose)
	return output
}
