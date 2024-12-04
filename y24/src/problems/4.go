package problems

import (
	"fmt"
	"strconv"
	"strings"
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

	board, width, height := ParseBoard(lines)
	fmt.Println("width:", width, "height:", height)
	PrintBoard(board)

	for y := 0; y < height; y++ {
		for x := 0; x < width; x++ {
			found := board[x][y]
			if found == "X" {
				neighbors := ListNeighborsN(
					board,
					width,
					height,
					x,
					y,
					3,
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

func ParseBoard(input []string) ([][]string, int, int) {
	firstLine := input[0]
	width := len(firstLine)
	height := len(input)

	output := make([][]string, width)
	for i := 0; i < width; i++ {
		output[i] = make([]string, height)
	}

	for y, line := range input {
		chars := strings.Split(line, "")
		for x, char := range chars {
			output[x][y] = char
		}
	}

	return output, width, height
}

func PrintBoard(board [][]string) {
	for _, line := range board {
		for _, char := range line {
			fmt.Print(string(char))
		}
		fmt.Println()
	}
}

func ListNeighborsN(
	board [][]string,
	width int,
	height int,
	x int,
	y int,
	n int,
) []string {
	output := make([]string, 0)
	for deltaX := -1; deltaX <= 1; deltaX++ {
		for deltaY := -1; deltaY <= 1; deltaY++ {
			if deltaX == 0 && deltaY == 0 {
				continue
			}
			currentString := ""
			for count := 1; count <= n; count++ {

				nextX := x + deltaX*count
				nextY := y + deltaY*count
				if nextX < 0 || nextX >= width || nextY < 0 || nextY >= height {
					if verbose {
						fmt.Println("edge")
					}
				} else {
					currentString = currentString + board[nextX][nextY]
				}
			}
			output = append(output, currentString)
		}
	}
	return output
}

func Solve4b(test bool) string {
	fmt.Println("Problem 4b:")
	data := utils.Read(utils.GetInputFileName(dayNumber, test))
	output := 0
	lines := utils.GetStrings(data)
	for _, lineString := range lines {
		if verbose {
			fmt.Println(lineString)
		}

	}

	board, width, height := ParseBoard(lines)
	fmt.Println("width:", width, "height:", height)
	PrintBoard(board)

	for y := 0; y < height; y++ {
		for x := 0; x < width; x++ {
			found := board[x][y]
			if found == "A" {
				neighbors := ListNeighborsN(
					board,
					width,
					height,
					x,
					y,
					1,
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
