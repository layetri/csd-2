import simpleaudio as sa

# Give the user a heads-up that the sound is, in fact, playing
print("Hey!")
# Ask for input
# bpm = input("give bpm: ")
times = input("rEpeAT h0W mUcH?? ")

# Calculate interval
# interval = 60000 / int(bpm)

# Load the wave into a WaveObject
wave = sa.WaveObject.from_wave_file("../../assets/testsample.wav")

for i in range(int(times)):
    # Play the sound
    play = wave.play()
    # Sleep till done
    play.wait_done()

# Done!
print("Song's over")
