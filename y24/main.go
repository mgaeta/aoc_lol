package main

import (
	"fmt"
	"y24/src/problems"
)

// TODO MARCOS 1.1 smarter test mode, verbose mode
// TODO MARCOS 1.0 detect the current day and run the relevant file.

func main() {
	fmt.Println(problems.Solve2a(true))
	fmt.Println(problems.Solve2a(false))
	fmt.Println(problems.Solve2b(true))
	fmt.Println(problems.Solve2b(false))
}
