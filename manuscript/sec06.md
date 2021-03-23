# Parting wisdom

I hope this primer has given you exposure to fundamental concepts in 16S data
processing. To give you a sense of where to go from here, I have some parting
wisdom.

## Become more computationally proficient

QIIME 2 and other tools do provide some visualization and analysis capability,
but if you want to deviate from the beaten path even a little bit, you will
need to develop your own computation skills.

The first key skill to learn is the Unix command line and the basic commands
like `cat`, `cd`, `cp`, `ls`, `mkdir`, `mv`, `rm`, `head`, `less`, `sed` (or
`awk`), `wc`, `grep`, and `vi` (or `emacs`). These tools will help you when
looking at raw data, using computational servers, or writing your own computer
code.[^jp]

[^jp]: Maybe one day we'll have sexy drag-and-drop, hologram-style data
  processing for 16S, but for the foreseeable future it's going to look like
the scene in *Jurassic Park* where Samuel L. Jackson is hunched over a computer
muttering "Access main program...  Access main security... Access main program
grid..."

The second key skill is to learn a programming language with decent
bioinformatics and statistics packages. Python and R are good choices. As a
Masters student, after many years of fitfully using tools like Mathematica,
I spent one week reading and doing all the exercises in Mark Lutz's _Learning
Python_. It was one of the best investments I've ever made.

## Be a data and algorithm detective

The best tool in your belt is a curious attitude. Be critical of your data at
every step in the pipeline before you move onto the next step.  Does it look
the way you expect? How can you check? You may save yourself from substantial
headache later on if you can catch bugs early in your analysis.

As mentioned earlier, processing 16S data requires many decisions, some small
and seeming inconsequential, like error thresholds, and some large, like the
choice of denoising algorithm of OTU picking method. Pipeline software like
QIIME 2 can, through the setting of default values, create the illusion that
some of these choices are not important, or even that you didn't need to make
a choice. I only want to emphasize again that, in 16S data processing, the devil
can be in the details.[^devil]

## Get help

16S processing and analysis is a rapidly evolving and complex field. Even if
you do develop strong computational skills, it is very wise to collaborate with
experts.

Happy processing, and good luck!
