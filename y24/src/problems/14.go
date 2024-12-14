package problems

import (
	"fmt"
	"strconv"
	"strings"
	"y24/src/utils"
)

type Robot struct {
	PX int
	PY int
	VX int
	VY int
}

func Solve14a(data string, verbose bool) string {
	lines := utils.GetStrings(data)
	maxX, maxY := 0, 0

	robots := make([]*Robot, 0)
	for _, line := range lines {
		robot, err := parseLine14(line)
		if err != nil {
			panic(err)
		}
		if robot.PX > maxX {
			maxX = robot.PX
		}
		if robot.PY > maxY {
			maxY = robot.PY
		}
		robots = append(robots, robot)
	}

	quadrant0, quadrant1, quadrant2, quadrant3, middle := 0, 0, 0, 0, 0
	for _, robot := range robots {
		x, y := simulate(robot, maxX+1, maxY+1, 100)
		if verbose {
			fmt.Println(x, y)
		}

		if x < (maxX+1)/2 && y < (maxY+1)/2 {
			quadrant0++
		} else if x < (maxX+1)/2 && y > (maxY+1)/2 {
			quadrant1++
		} else if x > (maxX+1)/2 && y > (maxY+1)/2 {
			quadrant2++
		} else if x > (maxX+1)/2 && y < (maxY+1)/2 {
			quadrant3++
		} else {
			middle++
		}
	}

	if verbose {
		fmt.Println("Quadrants:", quadrant0, quadrant1, quadrant2, quadrant3)
		fmt.Println("Middle:", middle)
	}

	return strconv.Itoa(quadrant0 * quadrant1 * quadrant2 * quadrant3)
}

func simulate(robot *Robot, width int, height int, steps int) (int, int) {
	return (robot.PX + (robot.VX+width)*steps) % width, (robot.PY + (robot.VY+height)*steps) % height
}

func parseLine14(line string) (*Robot, error) {
	parts := strings.Split(line, " ")
	positionString := parts[0][2:]
	velocityString := parts[1][2:]

	positionParts := strings.Split(positionString, ",")
	velocityParts := strings.Split(velocityString, ",")

	px, err := strconv.Atoi(positionParts[0])
	if err != nil {
		return nil, err
	}
	py, err := strconv.Atoi(positionParts[1])
	if err != nil {
		return nil, err
	}
	vx, err := strconv.Atoi(velocityParts[0])
	if err != nil {
		return nil, err
	}
	vy, err := strconv.Atoi(velocityParts[1])
	if err != nil {
		return nil, err
	}

	return &Robot{px, py, vx, vy}, nil
}

func Solve14b(data string, verbose bool) string {
	lines := utils.GetStrings(data)
	maxX, maxY := 0, 0

	robots := make([]*Robot, 0)
	for _, line := range lines {
		robot, err := parseLine14(line)
		if err != nil {
			panic(err)
		}
		if robot.PX > maxX {
			maxX = robot.PX
		}
		if robot.PY > maxY {
			maxY = robot.PY
		}
		robots = append(robots, robot)
	}

	for i := 0; i < 10000; i++ {
		if isTree(robots, maxX+1, maxY+1) {
			if verbose {
				fmt.Println(i)
				printBoard(robots, maxX+1, maxY+1)
			}
			return strconv.Itoa(i)
		}
		for _, robot := range robots {
			x, y := simulate(robot, maxX+1, maxY+1, 1)
			robot.PX = x
			robot.PY = y
		}
	}

	return strconv.Itoa(0)
}

func isTree(robots []*Robot, width int, height int) bool {
	board := make([][]int, width)
	for x := 0; x < width; x++ {
		board[x] = make([]int, height)
	}
	for _, robot := range robots {
		board[robot.PX][robot.PY]++
	}

	for y := 0; y < height; y++ {
		maxStreak := 0
		streak := 0
		for x := 0; x < width; x++ {
			if board[x][y] > 0 {
				streak++
				if streak > maxStreak {
					maxStreak = streak
				}
			} else {
				streak = 0
			}
		}
		if maxStreak > 10 {
			return true
		}
	}
	return false
}

func printBoard(robots []*Robot, width int, height int) {
	board := make([][]int, width)
	for x := 0; x < width; x++ {
		board[x] = make([]int, height)
	}

	for _, robot := range robots {
		board[robot.PX][robot.PY]++
	}

	for x := 0; x < width; x++ {
		for y := 0; y < height; y++ {
			found := board[x][y]
			if found == 0 {
				fmt.Print(".")
			} else {
				fmt.Print(found)
			}
		}
		fmt.Println()
	}
}
