package problems

import (
	"errors"
	"fmt"
	mapset "github.com/deckarep/golang-set/v2"
	"strconv"
	"y24/src/utils"
)

func determinePeaks(board [][]string, width int, height int) []string {
	possiblePeaks := mapset.NewSet[string]()
	for x := 0; x < width; x++ {
		for y := 0; y < height; y++ {
			symbol := board[x][y]
			if symbol == "9" {
				possiblePeaks.Add(utils.EncodeTuple(x, y))
			}
		}
	}
	return possiblePeaks.ToSlice()
}

func findTrailHeads(
	board [][]string,
	width int,
	height int,
	start string,
	verbose bool,
) []string {
	startX, startY, err := utils.DecodeTuple(start)
	if err != nil {
		panic(err)
	}

	currentSymbol := board[startX][startY]
	currentHeight, err := strconv.Atoi(currentSymbol)
	if err != nil {
		panic(err)
	}
	if currentSymbol == "0" {
		return []string{start}
	}
	neighbors := utils.ListNeighborsN(
		board,
		width,
		height,
		startX,
		startY,
		1,
		false,
	)

	output := make([]string, 0)
	// We actually need i to figure out where to recurse to.
	for i, neighborSymbol := range neighbors {
		if neighborSymbol == "" {
			continue
		}
		neighborValue, err := strconv.Atoi(neighborSymbol)
		if err != nil {
			fmt.Println(width, height, neighborSymbol, neighborValue)
			panic(err)
		}
		if currentHeight-1 == neighborValue {
			nextX, nextY, err := determineNext(startX, startY, i)
			if err == nil {
				neighbor := utils.EncodeTuple(nextX, nextY)
				result := findTrailHeads(board, width, height, neighbor, verbose)
				output = append(output, result...)
			}
		}
	}
	return output
}

func determineNext(x int, y int, i int) (int, int, error) {
	switch i {
	case 0:
		return x - 1, y - 1, fmt.Errorf("no diagonal")
	case 1:
		return x - 1, y, nil
	case 2:
		return x - 1, y + 1, fmt.Errorf("no diagonal")
	case 3:
		return x, y - 1, nil
	case 4:
		return x, y + 1, nil
	case 5:
		return x + 1, y - 1, fmt.Errorf("no diagonal")
	case 6:
		return x + 1, y, nil
	case 7:
		return x + 1, y + 1, fmt.Errorf("no diagonal")
	}
	return 0, 0, errors.New("invalid index")
}

func Solve10a(data string, verbose bool) string {
	output := 0
	lines := utils.GetStrings(data)
	board, width, height := utils.ParseBoard(lines)

	// map the token to a count.
	trailheads := make(map[string]mapset.Set[string])

	possiblePeaks := determinePeaks(board, width, height)
	for _, peak := range possiblePeaks {
		if verbose {
			fmt.Println("peak:", peak)
		}
		// a peak can be reached by multiple trailheads and vice versa.
		nextHeads := findTrailHeads(board, width, height, peak, verbose)
		for _, head := range nextHeads {
			found, ok := trailheads[head]
			if !ok {
				found = mapset.NewSet[string]()
			}
			found.Add(peak)
			trailheads[head] = found
		}
	}

	for head, setOfPeaks := range trailheads {
		if verbose {
			fmt.Println("head=", head, setOfPeaks.Cardinality(), setOfPeaks.ToSlice())
		}
		output += setOfPeaks.Cardinality()
	}

	return strconv.Itoa(output)
}

func Solve10b(data string, verbose bool) string {
	output := 0
	lines := utils.GetStrings(data)
	board, width, height := utils.ParseBoard(lines)

	// map the token to a count.
	trailheads := make(map[string]int)

	possiblePeaks := determinePeaks(board, width, height)
	for _, peak := range possiblePeaks {
		if verbose {
			fmt.Println("peak:", peak)
		}
		// a peak can be reached by multiple trailheads and vice versa.
		nextHeads := findTrailHeads(board, width, height, peak, verbose)
		for _, head := range nextHeads {
			found, ok := trailheads[head]
			if !ok {
				found = 0
			}
			found++
			trailheads[head] = found
		}
	}

	for _, trailCount := range trailheads {
		output += trailCount
	}

	return strconv.Itoa(output)
}
