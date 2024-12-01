package utils

import (
	"fmt"
	"os"
)

func Read(filename string) string {
	data, err := os.ReadFile(filename)
	if err != nil {
		fmt.Println(err)
		panic(err)
	}
	return string(data)
}
