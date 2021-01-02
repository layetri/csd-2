#pragma once

#define TWO_PI (M_PI * 2)
#define SAMPLERATE 44100

class Oscillator {
  public:
    Oscillator(float frequency);
    ~Oscillator();

    // Methods for Frequency
    float getFrequency();
    void setFrequency(float frequency);

    // Methods for Amplitude
    float getAmplitude();
    void setAmplitude(float amplitude);

    // Methods for Phase
    float getPhase();
    void incrementPhase();


  protected:
    void tick();
    void buffer();

    void calculatePhaseStep();

    float frequency;
    float amplitude;
    float phase;
    float phase_step;
    int sample;
};
