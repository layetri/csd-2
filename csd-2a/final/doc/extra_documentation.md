# Extra Documentation
As requested by Ciska during class, here I share my thoughts and the process of developing the training strategy for this project.

### Approach and Training Models
When thinking about an approach to tackle this assignment, I figured they easiest option would be to not use conventional methods from an established framework like TensorFlow, but to build a crude analysis algorithm from scratch instead. The concept for the algorithm is simple.
- First, we need to actually receive user input. We do this through collecting all the files in a folder that is specified by the user. These can be short files, long files, or even entire songs. For the presentation in class I trained the model on short drum loops only, since that was the only kind of source that I could find in semi-large quantities.
- With the source files in place, it's now time to analyze them one by one. We scale all note positions in the source file to be expressed as a multitude of 48, the default PPQ (Pulses Per Quarter note) value this program runs on. With these new positions, we can now start counting.
- We count all the occurrences of note _x_ at position _y_ throughout all the source files. All position indexes are marginally quantized, as humanization might confuse the analysis system by interpreting the same hit in different places and thus messing up the overall calculated average.
- Finally, we iterate over these total counts to transform them to averages spanning the entire length of the longest file, and then subsequently into a single measure average. This data is then stored on disk for generating rhythms.

### Why not TensorFlow?
I have looked into other ways of running this kind of data analysis, and specific frameworks that offer these kinds of methods, but found that ultimately I would only end up making the task more complex than it needed to be in order to create a crude but functional machine learning algorithm specifically designed for the task of analyzing rhythms. These methods, like HMM and KNN, would likely render better results, but would also require a much longer thought- and design process to be implemented in a sensible way to be used in this context. The resulting algorithm can be trained to be quite reliable when bigger datasets or longer rhythms are used. This, however, was beyond the scope of the assignment.