package utils

import "strconv"

func HistogramToString(input map[string]int) string {
	output := "{"
	for key, value := range input {
		output += "\n\t\"" + key + "\":\t" + strconv.Itoa(value) + ","
	}
	output += "\n}"
	return output
}
