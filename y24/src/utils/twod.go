package utils

import (
	"fmt"
	"strconv"
	"strings"
)

func EncodeTuple(startIndex int, length int) string {
	return fmt.Sprintf("%d,%d", startIndex, length)
}

func DecodeTuple(input string) (int, int, error) {
	parts := strings.Split(input, ",")
	startIndex, err := strconv.Atoi(parts[0])
	if err != nil {
		return 0, 0, err
	}
	length, err := strconv.Atoi(parts[1])
	if err != nil {
		return 0, 0, err
	}
	return startIndex, length, nil
}

func FindStr(
	board [][]string,
	width int,
	height int,
	needle string,
	verbose bool,
) (int, int) {
	var currX, currY int
	found := false
	for x := 0; x < width; x++ {
		for y := 0; y < height; y++ {

			if board[x][y] == needle {
				currX, currY = x, y
				found = true
				break
			}
		}
		if found {
			break
		}
	}
	if verbose {
		fmt.Println("startX, startY", currX, currY)
	}
	return currX, currY
}

func CopyBoard(board [][]string, width int, height int) [][]string {
	output := make([][]string, 0)
	for x := 0; x < width; x++ {
		column := make([]string, 0)
		for y := 0; y < height; y++ {
			column = append(column, board[x][y])
		}
		output = append(output, column)
	}
	return output
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

func PrintBoard(board [][]string, width int, height int) {
	for y := 0; y < height; y++ {
		for x := 0; x < width; x++ {
			fmt.Print(board[x][y])
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
	verbose bool,
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
						fmt.Println(nextX, nextY, "edge")
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
