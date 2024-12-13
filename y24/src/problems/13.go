package problems

import (
	"fmt"
	"strconv"
	"strings"
	"y24/src/utils"
)

func Solve13a(data string, verbose bool) string {
	output := 0
	lines := utils.GetStrings(data)
	games := parseInputs(lines)
	if verbose {
		for _, game := range games {
			PrintGame(game)
			solutions := solveGame(game)
			if len(solutions) == 0 {
				continue
			}
			minTokens := 9999999999999

			for _, solution := range solutions {
				x, y, err := utils.DecodeTuple(solution)
				if err != nil {
					panic(err)
				}

				value := x*3 + y
				if value < minTokens {
					minTokens = value
				}
			}
			output += minTokens
		}
	}

	return strconv.Itoa(output)
}

func solveGame(game Game) []string {
	output := make([]string, 0)
	for a := 0; a <= 100; a++ {
		for b := 0; b <= 100; b++ {
			testX := game.ValueAX*a + game.ValueBX*b
			testY := game.ValueAY*a + game.ValueBY*b
			if testX == game.PrizeX && testY == game.PrizeY {
				result := utils.EncodeTuple(a, b)
				output = append(output, result)
			}
		}
	}
	return output
}

func solveGame2(game Game) []string {
	output := make([]string, 0)
	for a := 0; a <= 100; a++ {
		for b := 0; b <= 100; b++ {
			testX := game.ValueAX*a + game.ValueBX*b
			testY := game.ValueAY*a + game.ValueBY*b
			if testX == game.PrizeX && testY == game.PrizeY {
				result := utils.EncodeTuple(a, b)
				output = append(output, result)
			}
		}
	}
	return output
}

type Game struct {
	ValueAX int
	ValueAY int
	ValueBX int
	ValueBY int
	PrizeX  int
	PrizeY  int
}

func parseInputs(input []string) []Game {
	output := make([]Game, 0)
	temp := make([]string, 0)
	for _, line := range input {
		if line != "" {
			temp = append(temp, line)
			continue
		}

		game, err := parseGame(temp)
		if err != nil {
			panic(err)
		}
		output = append(output, game)
		temp = make([]string, 0)

	}
	game, err := parseGame(temp)
	if err != nil {
		panic(err)
	}
	output = append(output, game)
	temp = make([]string, 0)
	return output
}

func parseGame(lines []string) (Game, error) {
	prefix := "Button A: X+"
	delimiter := ", Y+"
	prefixPrize := "Prize: X="
	prizeDelimiter := ", Y="
	parts0 := strings.Split(lines[0][len(prefix):], delimiter)
	parts1 := strings.Split(lines[1][len(prefix):], delimiter)
	parts2 := strings.Split(lines[2][len(prefixPrize):], prizeDelimiter)

	ax, err := strconv.Atoi(parts0[0])
	if err != nil {
		return Game{}, err
	}
	ay, err := strconv.Atoi(parts0[1])
	if err != nil {
		return Game{}, err
	}
	bx, err := strconv.Atoi(parts1[0])
	if err != nil {
		return Game{}, err
	}
	by, err := strconv.Atoi(parts1[1])
	if err != nil {
		return Game{}, err
	}
	px, err := strconv.Atoi(parts2[0])
	if err != nil {
		return Game{}, err
	}
	py, err := strconv.Atoi(parts2[1])
	if err != nil {
		return Game{}, err
	}

	return Game{
		ValueAX: ax,
		ValueAY: ay,
		ValueBX: bx,
		ValueBY: by,
		PrizeX:  px,
		PrizeY:  py,
	}, nil
}

func PrintGame(g Game) {
	fmt.Println(g.PrizeX, g.PrizeY, g.ValueAX, g.ValueAY, g.ValueBX, g.ValueBY)
}

func Solve13b(data string, verbose bool) string {
	output := 0
	lines := utils.GetStrings(data)
	games := parseInputs(lines)
	if verbose {
		for _, game := range games {
			PrintGame(game)
			game.PrizeX += 10000000000000
			game.PrizeY += 10000000000000
			solutions := solveGame2(game)
			if len(solutions) == 0 {
				continue
			}
			minTokens := 99999999999999

			for _, solution := range solutions {
				x, y, err := utils.DecodeTuple(solution)
				if err != nil {
					panic(err)
				}

				value := x*3 + y
				if value < minTokens {
					minTokens = value
				}
			}
			output += minTokens
		}
	}

	return strconv.Itoa(output)
}
