package problems

import (
	"fmt"
	"strconv"
	"strings"
	"y24/src/utils"
)

func Solve15a(data string, verbose bool) string {
	lines := utils.GetStrings(data)

	var ii int
	for i, line := range lines {
		if line == "" {
			ii = i
		}
	}
	board, width, height := utils.ParseBoard(lines[:ii])

	instructions := make([]string, 0)
	for _, line := range lines[ii:] {
		parts := strings.Split(line, "")
		for _, part := range parts {
			instructions = append(instructions, part)
		}
	}

	if verbose {
		fmt.Println(instructions)
		utils.PrintBoard(board, width, height)
	}

	for _, instruction := range instructions {
		startX, startY := utils.FindStr(board, width, height, "@", false)
		if verbose {
			fmt.Println("executing", instruction)
		}
		deltaX, deltaY, err := getDelta(instruction)
		if err != nil {
			panic(err)
		}

		var i = 1
		for {
			if verbose {
				fmt.Println("startx", startX, "startY", startY, "deltaX", deltaX, "deltaY", deltaY)
			}
			nextX := startX + deltaX*i
			nextY := startY + deltaY*i
			symbol := board[nextX][nextY]
			if symbol == "#" {
				break
			}
			if symbol == "." {
				//fmt.Println("moving to", nextX, nextY, i)
				for j := i; j > 0; j-- {
					board[startX+deltaX*j][startY+deltaY*j] = board[startX+deltaX*(j-1)][startY+deltaY*(j-1)]
				}
				board[startX][startY] = "."
				if verbose {
					utils.PrintBoard(board, width, height)
				}
				break
			}
			i++
		}

	}
	if verbose {
		utils.PrintBoard(board, width, height)
	}
	output := calculateResult15(board, width, height, verbose)
	return strconv.Itoa(output)
}

func calculateResult15(board [][]string, width int, height int, verbose bool) int {
	output := 0
	for x := 0; x < width; x++ {
		for y := 0; y < height; y++ {
			symbol := board[x][y]
			if symbol == "O" {
				output += x + 100*y
			}
		}
	}
	return output
}

func getDelta(input string) (int, int, error) {
	switch input {
	case "^":
		return 0, -1, nil
	case ">":
		return 1, 0, nil
	case "<":
		return -1, 0, nil
	case "v":
		return 0, 1, nil
	default:
		return 0, 0, fmt.Errorf("bad instruction")
	}
}

func Solve15b(data string, verbose bool) string {
	output := 0
	lines := utils.GetStrings(data)
	if verbose {
		for _, line := range lines {
			fmt.Println(line)
		}
	}

	return strconv.Itoa(output)
}
