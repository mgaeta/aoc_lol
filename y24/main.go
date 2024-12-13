package main

import (
	"fmt"
	"y24/src/problems"
	"y24/src/utils"
)

const (
	dayNumber = 13
	verbose   = true
)

type F func(string, bool) string

func Solve() (F, F) {
	switch dayNumber {
	case 1:
		return problems.Solve1a, problems.Solve1b
	case 2:
		return problems.Solve2a, problems.Solve2b
	case 3:
		return problems.Solve3a, problems.Solve3b
	case 4:
		return problems.Solve4a, problems.Solve4b
	case 5:
		return problems.Solve5a, problems.Solve5b
	case 6:
		return problems.Solve6a, problems.Solve6b
	case 7:
		return problems.Solve7a, problems.Solve7b
	case 8:
		return problems.Solve8a, problems.Solve8b
	case 9:
		return problems.Solve9a, problems.Solve9b
	case 10:
		return problems.Solve10a, problems.Solve10b
	case 11:
		return problems.Solve11a, problems.Solve11b
	case 12:
		return problems.Solve12a, problems.Solve12b
	case 13:
		return problems.Solve13a, problems.Solve13b
	case 14:
		return problems.Solve14a, problems.Solve14b
	case 15:
		return problems.Solve15a, problems.Solve15b
	case 16:
		return problems.Solve16a, problems.Solve16b
	case 17:
		return problems.Solve17a, problems.Solve17b
	case 18:
		return problems.Solve18a, problems.Solve18b
	case 19:
		return problems.Solve19a, problems.Solve19b
	case 20:
		return problems.Solve20a, problems.Solve20b
	case 21:
		return problems.Solve21a, problems.Solve21b
	case 22:
		return problems.Solve22a, problems.Solve22b
	case 23:
		return problems.Solve23a, problems.Solve23b
	case 24:
		return problems.Solve24a, problems.Solve24b
	case 25:
		return problems.Solve25a, problems.Solve25b

	default:
		panic("invalid day number")

	}
}

func main() {
	//part1, _ := Solve()
	_, part2 := Solve()

	testData := utils.Read(utils.GetInputFileName(dayNumber, true))
	data := utils.Read(utils.GetInputFileName(dayNumber, false))

	//fmt.Println("Test 1:\t", part1(testData, verbose))
	//fmt.Println("REAL 1:\t", part1(data, verbose))
	fmt.Println("Test 2:\t", part2(testData, verbose))
	fmt.Println("REAL 2:\t", part2(data, verbose))
}
