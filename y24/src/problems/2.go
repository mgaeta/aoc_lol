package problems

import (
	"fmt"
	"strconv"
	"strings"
	"y24/src/utils"
)

func Solve2a(data string, verbose bool) string {
	output := 0
	lines := utils.GetStrings(data)
	for _, lineString := range lines {
		line := prepareLine(lineString)
		result0 := firstUnsafe(line, verbose)
		if result0 == -1 {
			output += 1
			continue
		}
	}

	return strconv.Itoa(output)
}

func prepareLine(line string) []int {
	output := make([]int, 0)
	for _, partString := range strings.Split(line, " ") {
		partInt, err := strconv.Atoi(partString)
		if err != nil {
			panic(err)
		}
		output = append(output, partInt)
	}
	return output
}

func firstUnsafe(parts []int, verbose bool) int {
	if verbose {
		fmt.Println(parts)
	}
	firstPart := parts[0]
	lastPart := parts[1]

	var isIncreasing bool
	if lastPart < firstPart {
		isIncreasing = true
	} else {
		isIncreasing = false
	}

	delta := utils.Abs(lastPart - firstPart)
	if delta < 1 || delta > 3 {
		return 0
	}

	for i, part := range parts[2:] {
		delta1 := utils.Abs(part - lastPart)
		if delta1 >= 1 && delta1 <= 3 {
			if part > lastPart {
				if isIncreasing {
					return i
				}
			} else {
				if !isIncreasing {
					return i
				}
			}
		} else {
			return i
		}
		lastPart = part
	}
	return -1
}

func Solve2b(data string, verbose bool) string {
	output := 0
	lines := utils.GetStrings(data)
	for _, lineString := range lines {
		if verbose {
			fmt.Println(output)
			fmt.Println(lineString)
		}
		line := prepareLine(lineString)
		result0 := firstUnsafe(line, verbose)
		if result0 == -1 {
			output += 1
			continue
		}

		result1 := firstUnsafe(line[1:], verbose)
		if result1 == -1 {
			output += 1
			continue
		}

		result2 := firstUnsafe(line[:len(line)-1], verbose)
		if result2 == -1 {
			output += 1
			continue
		}

		for i := 1; i < len(line)-1; i++ {
			sliced := make([]int, 0)
			sliced = append(sliced, line[:i]...)
			sliced = append(sliced, line[i+1:]...)
			result3 := firstUnsafe(sliced, verbose)
			if result3 == -1 {
				output += 1
				break
			}
		}
	}

	return strconv.Itoa(output)
}
