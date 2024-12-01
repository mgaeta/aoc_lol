package utils

import (
	"fmt"
)

func GetInputFileName(dayNumber int, test bool) string {
	var suffix string
	if test {
		suffix = "_test"
	} else {
		suffix = ""
	}
	return fmt.Sprintf("inputs/%d%s.txt", dayNumber, suffix)
}
