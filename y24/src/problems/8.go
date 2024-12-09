package problems

import (
	"fmt"
	mapset "github.com/deckarep/golang-set/v2"
	"strconv"
	"y24/src/utils"
)

func Solve8a(data string, verbose bool) string {
	lines := utils.GetStrings(data)
	board, width, height := utils.ParseBoard(lines)
	frequencies := collectFrequencies(board, width, height)
	if verbose {
		fmt.Println("Frequencies:", frequencies)
	}
	output := countAntiNodes(frequencies, width, height, false, verbose)
	return strconv.Itoa(output)
}

func collectFrequencies(board [][]string, width int, height int) map[string][]string {
	//                      char //token
	frequencies := make(map[string][]string)
	for x := 0; x < width; x++ {
		for y := 0; y < height; y++ {
			symbol := board[x][y]
			if symbol == "." {
				continue
			}

			found, ok := frequencies[symbol]
			if !ok {
				found = make([]string, 0)
			}

			found = append(found, utils.EncodeTuple(x, y))
			frequencies[symbol] = found
		}
	}
	return frequencies
}

func countAntiNodes(
	frequencies map[string][]string,
	width int,
	height int,
	resonate bool,
	verbose bool,
) int {
	antiNodes := mapset.NewSet[string]()

	// For every frequency
	// for every pair (n^2)
	// for each antinode
	// if it's in bounds, output ++
	for symbol, locations := range frequencies {
		if verbose {
			fmt.Println("Symbol:", symbol)
		}
		for i := 0; i < len(locations); i++ {
			for j := i + 1; j < len(locations); j++ {
				location0X, location0Y, err := utils.DecodeTuple(locations[i])
				if err != nil {
					panic(err)
				}
				location1X, location1Y, err := utils.DecodeTuple(locations[j])
				if err != nil {
					panic(err)
				}

				deltaX, deltaY := location1X-location0X, location1Y-location0Y
				antiNode0X, antiNode0Y := location0X, location0Y
				antiNode1X, antiNode1Y := location1X, location1Y
				done := false
				for antiNode0X >= 0 &&
					antiNode0Y >= 0 &&
					antiNode0X < width &&
					antiNode0Y < height {
					if resonate || done {
						antiNodes.Add(utils.EncodeTuple(antiNode0X, antiNode0Y))
						if !resonate {
							break
						}
					} else {
						done = true
					}
					antiNode0X -= deltaX
					antiNode0Y -= deltaY

				}
				done = false
				for antiNode1X >= 0 &&
					antiNode1Y >= 0 &&
					antiNode1X < width &&
					antiNode1Y < height {
					if resonate || done {
						antiNodes.Add(utils.EncodeTuple(antiNode1X, antiNode1Y))
						if !resonate {
							break
						}
					} else {
						done = true
					}
					antiNode1X += deltaX
					antiNode1Y += deltaY
				}
			}
		}
	}
	if verbose {
		fmt.Println("Anti Nodes:", antiNodes)
	}
	return antiNodes.Cardinality()
}

func Solve8b(data string, verbose bool) string {
	lines := utils.GetStrings(data)
	board, width, height := utils.ParseBoard(lines)
	frequencies := collectFrequencies(board, width, height)
	if verbose {
		fmt.Println("Frequencies:", frequencies)
	}

	output := countAntiNodes(frequencies, width, height, true, verbose)
	return strconv.Itoa(output)
}
