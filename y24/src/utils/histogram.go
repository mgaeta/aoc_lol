package utils

func Histogram(data []string) map[string]int {
	histogram := make(map[string]int)
	for _, element := range data {
		value, found := histogram[element]
		if !found {
			value = 0
		}
		histogram[element] = value + 1
	}
	return histogram
}

func HistogramInt(data []int) map[int]int {
	histogram := make(map[int]int)
	for _, element := range data {
		found, err := histogram[element]
		if err {
			found = 0
		}
		histogram[element] = found + 1
	}
	return histogram
}
