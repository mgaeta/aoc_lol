package main

import (
	"fmt"
	"y24/src/problems"
)

// TODO MARCOS 1.0 detect the current day and run the relevant file.

func main() {
	fmt.Println(problems.Solve1a(true))
	fmt.Println(problems.Solve1a(false))
	fmt.Println(problems.Solve1b(true))
	fmt.Println(problems.Solve1b(false))
}
