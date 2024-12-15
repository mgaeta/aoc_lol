package problems

import (
	"fmt"
	mapset "github.com/deckarep/golang-set/v2"
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
				fmt.Println(
					"startX",
					startX,
					"startY",
					startY,
					"deltaX",
					deltaX,
					"deltaY",
					deltaY,
				)
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
	output := calculateResult15(board, width, height, "O")
	return strconv.Itoa(output)
}

func calculateResult15(board [][]string, width int, height int, needle string) int {
	output := 0
	for x := 0; x < width; x++ {
		for y := 0; y < height; y++ {
			symbol := board[x][y]
			if symbol == needle {
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
	lines := utils.GetStrings(data)

	var ii int
	for i, line := range lines {
		if line == "" {
			ii = i
		}
	}
	board0, width0, height := utils.ParseBoard(lines[:ii])
	board := make([][]string, 0)

	for x := 0; x < width0; x++ {
		column0 := make([]string, height)
		column1 := make([]string, height)
		board = append(board, column0, column1)
	}

	for x := 0; x < width0; x++ {
		for y := 0; y < height; y++ {
			symbol0 := board0[x][y]
			switch symbol0 {
			case ".", "#":
				board[x*2][y] = symbol0
				board[x*2+1][y] = symbol0

			case "@":
				board[x*2][y] = symbol0
				board[x*2+1][y] = "."
			case "O":
				board[x*2][y] = "["
				board[x*2+1][y] = "]"
			}
		}
	}

	width := width0 * 2

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

		if instruction == "<" || instruction == ">" {
			var i = 1
			for {
				if verbose {
					fmt.Println(
						"startX",
						startX,
						"startY",
						startY,
						"deltaX",
						deltaX,
						"deltaY",
						deltaY,
					)
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
		} else {
			// we're going to sort of push the heads in waves.
			heads := mapset.NewSet[string]()
			heads.Add(utils.EncodeTuple(startX, startY))
			for {
				nextHeads := mapset.NewSet[string]()

				canMove := true
				for _, head := range heads.ToSlice() {
					headX, headY, err := utils.DecodeTuple(head)
					if err != nil {
						panic(err)
					}
					headNextY := headY + deltaY
					if board[headX][headNextY] == "#" {
						// this whole stack cannot move.
						canMove = false
						break
					}
					if board[headX][headNextY] == "[" {
						nextHeads.Add(utils.EncodeTuple(headX, headNextY))
						nextHeads.Add(utils.EncodeTuple(headX+1, headNextY))
					} else if board[headX][headNextY] == "]" {
						nextHeads.Add(utils.EncodeTuple(headX-1, headNextY))
						nextHeads.Add(utils.EncodeTuple(headX, headNextY))
					}
				}
				if !canMove {
					break
				}

				if nextHeads.Cardinality() > 0 {
					heads = nextHeads
					continue
				}

				// move Everything in heads
				for _, head := range heads.ToSlice() {
					headX, headY, err := utils.DecodeTuple(head)
					if err != nil {
						panic(err)
					}
					headNextY := headY + deltaY
					board[headX][headNextY] = board[headX][headY]
					board[headX][headY] = "."
				}

				if board[startX][startY] == "." {
					// then we moved the starting spot.
					break
				}
				// otherwise start over
				heads.Clear()
				heads.Add(utils.EncodeTuple(startX, startY))
			}
		}
	}
	if verbose {
		utils.PrintBoard(board, width, height)
	}
	output := calculateResult15(board, width, height, "[")
	return strconv.Itoa(output)
}
