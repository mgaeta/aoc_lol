package problems

import (
	"fmt"
	"strconv"
	"y24/src/utils"
)

func Solve18a(data string, verbose bool) string {
	output := 0
	lines := utils.GetStrings(data)
	if verbose {
		for _, line := range lines {
			fmt.Println(line)
		}
	}

	return strconv.Itoa(output)
}

func Solve18b(data string, verbose bool) string {
	output := 0
	lines := utils.GetStrings(data)
	if verbose {
		for _, line := range lines {
			fmt.Println(line)
		}
	}

	return strconv.Itoa(output)
}
