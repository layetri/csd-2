#pragma once

#define TWO_PI (M_PI * 2)

class Oscillator {
  public:
    Oscillator(float frequency, int samplerate);
    virtual ~Oscillator();

    // Methods for Frequency
    float getFrequency();
    void setFrequency(float frequency);

    // Methods for Amplitude
    float getAmplitude();
    void setAmplitude(float amplitude);

    // Methods for Phase
    float getPhase();
    void incrementPhase();

    // Methods for Samplerate
    double getSamplerate();
    void setSamplerate(int samplerate);

    // Methods to override
    virtual float getSample();
    virtual void next();


  protected:
    void buffer();

    void calculatePhaseStep();

    double samplerate;

    float frequency;
    float amplitude;
    float detune;
    float phase;
    float phase_step;
};
