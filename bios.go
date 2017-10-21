// Copyright © 2017 Galvanized Logic Inc.

package main

// bios.go was created to test building and packaging a vu engine app for ios.

import (
	"log"
	"runtime/debug"

	"github.com/gazed/vu"
)

// Starts the vu engine which invokes Create and Update methods below.
func main() {
	defer catchErrors()
	if err := vu.Run(&bios{}); err != nil {
		log.Printf("Failed to initialize engine %s", err)
	}
}

// catchErrors attempts to dump debug information if there was a problem.
func catchErrors() {
	if r := recover(); r != nil {
		log.Printf("Panic %s: %s Shutting down.", r, debug.Stack())
	}
}

// =============================================================================
// bios

// bios displays a single spinning model.
type bios struct {
	ball *vu.Ent // Spinning model.
}

// Create is the one-time vu engine asset creation callback.
func (b *bios) Create(eng vu.Eng, s *vu.State) {
	eng.Set(vu.Title("Ball"))
	scene := eng.AddScene()
	scene.Cam().SetClip(0.1, 100).SetFov(90)
	b.ball = scene.AddPart().MakeModel("ball", "msh:ball", "tex:ball")
	b.ball.SetAt(0, 0, -2) // Camera is at 0,0,0 looking down -Z.
}

// Update is the ongoing vu engine callback to the main application logic.
// It occurs roughly every 0.02 seconds.
func (b *bios) Update(eng vu.Eng, in *vu.Input, s *vu.State) {
	b.ball.Spin(0.1, 0.5, 0)
}
