import simpleaudio as sa

# Give the user a heads-up that the sound is, in fact, playing
print("Song's starting")

# Load the wave into a WaveObject
wave = sa.WaveObject.from_wave_file("../../assets/testsong.wav")
# Play the sound
play = wave.play()
# Sleep till done
play.wait_done()

# Done!
print("Song's over")