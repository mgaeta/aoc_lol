package problems

import (
	"fmt"
	"strconv"
	"y24/src/utils"
)

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

func Solve6a(data string, verbose bool) string {
	output := 0
	lines := utils.GetStrings(data)

	board, width, height := utils.ParseBoard(lines)

	dir := 0
	dirsX := []int{0, 1, 0, -1}
	dirsY := []int{-1, 0, 1, 0}

	currX, currY := FindStr(board, width, height, "^", verbose)

	for {
		if currX < 0 || currY < 0 || currX >= width || currY >= height {
			break
		}
		nextSymbol := "X"
		board[currX][currY] = nextSymbol

		done := false
		for {
			nextX, nextY := currX+dirsX[dir%4], currY+dirsY[dir%4]
			if nextX < 0 || nextY < 0 || nextX >= width || nextY >= height {
				done = true
				break
			}
			nextFound := board[nextX][nextY]
			if nextFound == "#" {
				dir = dir + 1
			} else {
				currX, currY = nextX, nextY
				break
			}
		}
		if done {
			break
		}
	}

	for x := 0; x < width; x++ {
		for y := 0; y < height; y++ {
			if board[x][y] == "X" {
				output++
			}
		}
	}

	return strconv.Itoa(output)
}
