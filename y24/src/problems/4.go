package problems

import (
	"fmt"
	"strconv"
	"y24/src/utils"
)

func Solve4a(test bool) string {
	fmt.Println("Problem 4a:")
	data := utils.Read(utils.GetInputFileName(dayNumber, test))
	output := 0
	lines := utils.GetStrings(data)

	// my strategy is to create a map of tuples to values
	// so that I can quickly look up the value at a location
	// then I'm going to find all of the "X" values.
	// for each "X", I'm going to iterate over the 8 possible directions
	// I'm going to check that the next three letters are "MAS"
	// breaking if we hit and edge.

	for _, lineString := range lines {
		if verbose {
			fmt.Println(lineString)
		}
	}

	board, width, height := utils.ParseBoard(lines)
	fmt.Println("width:", width, "height:", height)
	utils.PrintBoard(board)

	for y := 0; y < height; y++ {
		for x := 0; x < width; x++ {
			found := board[x][y]
			if found == "X" {
				neighbors := utils.ListNeighborsN(
					board,
					width,
					height,
					x,
					y,
					3,
					verbose,
				)
				for _, neighbor := range neighbors {
					if neighbor == "MAS" {
						output += 1
					}
				}
			}
		}
	}

	return strconv.Itoa(output)
}

func Solve4b(test bool) string {
	fmt.Println("Problem 4b:")
	data := utils.Read(utils.GetInputFileName(dayNumber, test))
	output := 0
	lines := utils.GetStrings(data)
	board, width, height := utils.ParseBoard(lines)
	if verbose {
		fmt.Println("width:", width, "height:", height)
		utils.PrintBoard(board)
	}

	for y := 0; y < height; y++ {
		for x := 0; x < width; x++ {
			found := board[x][y]
			if found == "A" {
				neighbors := utils.ListNeighborsN(
					board,
					width,
					height,
					x,
					y,
					1,
					verbose,
				)

				// 012
				// 3 4
				// 567

				left := false
				right := false

				if neighbors[0] == "M" && neighbors[7] == "S" {
					left = true
				} else if neighbors[7] == "M" && neighbors[0] == "S" {
					left = true
				} else if neighbors[7] == "S" && neighbors[0] == "M" {
					left = true
				} else if neighbors[0] == "S" && neighbors[7] == "M" {
					left = true
				}

				if neighbors[2] == "M" && neighbors[5] == "S" {
					right = true
				} else if neighbors[2] == "S" && neighbors[5] == "M" {
					right = true
				} else if neighbors[5] == "S" && neighbors[2] == "M" {
					right = true
				} else if neighbors[5] == "M" && neighbors[2] == "S" {
					right = true
				}

				if left && right {
					output += 1
				}
			}
		}
	}

	return strconv.Itoa(output)
}
