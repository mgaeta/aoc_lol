package problems

import (
	"fmt"
	mapset "github.com/deckarep/golang-set/v2"
	"strconv"
	"y24/src/utils"
)

type Region struct {
	Id     int
	Points mapset.Set[string]
	Symbol string
}

func ListNeighbors12(
	width int,
	height int,
	x int,
	y int,
) []string {
	output := make([]string, 0)
	for deltaX := -1; deltaX <= 1; deltaX++ {
		for deltaY := -1; deltaY <= 1; deltaY++ {
			// only cardinal
			if utils.Abs(deltaX+deltaY) != 1 {
				continue
			}
			nextX := x + deltaX
			nextY := y + deltaY
			if !(nextX < 0 || nextX >= width || nextY < 0) && nextY < height {
				output = append(output, utils.EncodeTuple(nextX, nextY))
			}
		}
	}
	return output
}

func Solve12a(data string, verbose bool) string {
	output := 0
	lines := utils.GetStrings(data)

	board, width, height := utils.ParseBoard(lines)
	if verbose {
		utils.PrintBoard(board, width, height)
	}
	// collect all possible letters?
	// create n*n regions and merge them?

	regionsById, pointsToRegions, err := generateRegions(board, width, height, verbose)
	if err != nil {
		panic(err)
	}

	// once the regions are established, we can calculate their areas and perimeters
	for _, region := range regionsById {
		output += calculateResult(
			pointsToRegions,
			region,
			width,
			height,
			verbose,
		)
	}

	return strconv.Itoa(output)
}

func calculateResult(
	pointsToRegions map[string]int,
	region Region,
	width int,
	height int,
	verbose bool,
) int {
	area := 0
	perimeter := 0
	for _, point := range region.Points.ToSlice() {
		p := 4
		x, y, err := utils.DecodeTuple(point)
		if err != nil {
			panic(err)
		}
		neighbors := ListNeighbors12(width, height, x, y)
		for _, neighborPoint := range neighbors {
			neighborRegionId, ok := pointsToRegions[neighborPoint]
			if !ok {
				panic("couldn't find region for point")
			}

			if neighborRegionId == region.Id {
				p--
			}
		}
		perimeter += p
		area++
	}

	if verbose {
		fmt.Println("area", area, "perimeter", perimeter)
	}
	return area * perimeter
}

func generateRegions(
	board [][]string,
	width int,
	height int,
	verbose bool,
) (
	map[int]Region,
	map[string]int,
	error,
) {
	regionsById := make(map[int]Region)
	nextId := 0
	pointsToRegions := make(map[string]int)
	for x := 0; x < width; x++ {
		for y := 0; y < height; y++ {
			symbol := board[x][y]
			points := mapset.NewSet[string]()
			token := utils.EncodeTuple(x, y)
			points.Add(token)
			regionsById[nextId] = Region{
				Id:     nextId,
				Symbol: symbol,
				Points: points,
			}
			pointsToRegions[token] = nextId
			nextId++
		}
	}

	for x := 0; x < width; x++ {
		for y := 0; y < height; y++ {
			regionId := pointsToRegions[utils.EncodeTuple(x, y)]
			neighbors := ListNeighbors12(
				width,
				height,
				x,
				y,
			)
			for _, neighborPoint := range neighbors {
				region := regionsById[regionId]
				if verbose {
					fmt.Println(
						region.Symbol,
						"region.Points",
						region.Points,
						"neighborPoint",
						neighborPoint,
					)
				}
				if region.Points.Contains(neighborPoint) {
					if verbose {
						fmt.Println("region.Points.Contains(neighborPoint)")
					}
					continue
				}
				otherRegionId, ok := pointsToRegions[neighborPoint]
				if !ok {
					return nil, nil, fmt.Errorf("couldn't find region for point")
				}

				otherRegion, ok := regionsById[otherRegionId]
				if !ok {
					return nil, nil, fmt.Errorf("invalid region ID")
				}

				if verbose {
					fmt.Println(
						"region.Symbol",
						region.Symbol,
						region.Id,
						"otherRegion.Symbol",
						otherRegion.Symbol,
						otherRegion.Id,
					)
				}
				if otherRegion.Symbol == region.Symbol {
					newPoints := region.Points.Union(otherRegion.Points)
					if verbose {
						fmt.Println("newPoints", newPoints)
					}
					regionsById[regionId] = Region{
						Id:     regionId,
						Points: newPoints,
						Symbol: region.Symbol,
					}
					if verbose {
						fmt.Println(
							"deleting from regions by id",
							otherRegion.Id,
							"in favor of",
							region.Symbol,
							region.Id,
						)
					}
					delete(regionsById, otherRegion.Id)
					// I have to do this for every point in the region
					for _, otherPoint := range otherRegion.Points.ToSlice() {
						pointsToRegions[otherPoint] = region.Id
					}
				}
			}
		}
	}
	return regionsById, pointsToRegions, nil
}

func countCorners(
	region Region,
	pointsToRegions map[string]int,
	verbose bool,
) int {
	output := 0
	for _, point := range region.Points.ToSlice() {
		x, y, err := utils.DecodeTuple(point)
		if err != nil {
			panic(err)
		}
		neighbors := ListNeighbors12Part2(
			pointsToRegions,
			x,
			y,
			region.Id,
		)
		fmt.Println(
			region.Symbol,
			neighbors,
		)
		for i := 0; i < len(neighbors); i += 2 {
			edge0 := neighbors[(i+7)%8]
			edge1 := neighbors[(i+1)%8]
			corner := neighbors[i]
			if verbose {
				fmt.Println(
					i,
					(i+7)%8,
					(i+1)%8,
					"=",
					edge0,
					edge1,
					corner,
				)
			}

			// If all false-??-false, we have an outer corner
			if !edge0 && !edge1 {
				output += 1
				continue
			}
			// If it's true-false-true, we have an inner corner
			if edge0 && edge1 && !corner {
				output += 1
			}
		}
	}
	return output
}

func calculateResult2(
	pointsToRegions map[string]int,
	region Region,
	verbose bool,
) int {
	area := region.Points.Cardinality()
	perimeter := countCorners(region, pointsToRegions, verbose)
	if verbose {
		fmt.Println(region.Symbol, "area", area, "perimeter", perimeter)
	}
	return area * perimeter
}

func ListNeighbors12Part2(
	pointsToRegions map[string]int,
	x int,
	y int,
	id int,
) []bool {
	output := make([]bool, 0)
	for deltaX := -1; deltaX <= 1; deltaX++ {
		for deltaY := -1; deltaY <= 1; deltaY++ {
			token := utils.EncodeTuple(x+deltaX, y+deltaY)
			found, ok := pointsToRegions[token]
			output = append(output, ok && found == id)
		}
	}
	// 036
	// 147
	// 258
	return []bool{
		output[0],
		output[1],
		output[2],
		output[5],
		output[8],
		output[7],
		output[6],
		output[3],
	}
}

func Solve12b(data string, verbose bool) string {
	output := 0
	lines := utils.GetStrings(data)

	board, width, height := utils.ParseBoard(lines)
	if verbose {
		utils.PrintBoard(board, width, height)
	}
	// collect all possible letters?
	// create n*n regions and merge them?
	regionsById, pointsToRegions, err := generateRegions(board, width, height, false)
	if err != nil {
		panic(err)
	}

	for _, region := range regionsById {
		output += calculateResult2(
			pointsToRegions,
			region,
			verbose,
		)
	}
	return strconv.Itoa(output)
}
