package problems

import (
	"fmt"
	"sort"
	"strconv"
	"strings"
	"y24/src/utils"
)

const (
	dayNumber = 3
	verbose   = true
)

func Solve1a(test bool) string {
	fmt.Println("Problem 1a")
	data := utils.Read(utils.GetInputFileName(dayNumber, test))

	lines := utils.GetStrings(data)
	lefts := make([]int, 0)
	rights := make([]int, 0)

	for _, line := range lines {
		parts := strings.Split(line, "   ")
		int0, err := strconv.ParseInt(parts[0], 10, 32)
		if err != nil {
			panic(err)
		}
		lefts = append(lefts, int(int0)+10000)
		int1, err := strconv.ParseInt(parts[1], 10, 32)
		if err != nil {
			panic(err)
		}
		rights = append(rights, int(int1)+10000)
	}

	sort.Ints(lefts)
	if verbose {
		for i := range lefts {
			fmt.Println(i, lefts[i])
		}
	}

	sort.Ints(rights)

	output := 0
	for i := range lefts {
		x := utils.Abs(lefts[i] - rights[i])
		if verbose {
			fmt.Println("asdf", i, lefts[i], rights[i])
			fmt.Println("x", x)
		}
		output += x

	}

	return strconv.Itoa(output)
}

func Solve1b(test bool) string {
	fmt.Println("Problem 1b")
	data := utils.Read(utils.GetInputFileName(dayNumber, test))
	lines := utils.GetStrings(data)
	lefts := make([]int, 0)
	rights := make([]string, 0)

	for _, line := range lines {
		parts := strings.Split(line, "   ")
		int0, err := strconv.ParseInt(parts[0], 10, 32)
		if err != nil {
			panic(err)
		}
		lefts = append(lefts, int(int0))
		rights = append(rights, parts[1])
	}

	frequencies := utils.Histogram(rights)
	if verbose {
		fmt.Println("frequencies:", utils.HistogramToString(frequencies))
	}

	output := 0
	for _, left := range lefts {
		if verbose {
			fmt.Println(
				"asdf",
				left,
				frequencies[strconv.Itoa(left)],
				left*frequencies[strconv.Itoa(left)],
			)
		}
		output += left * frequencies[strconv.Itoa(left)]
	}

	return strconv.Itoa(output)
}
