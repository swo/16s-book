---

# Parting wisdom

## Your own tools

I've kept yammering about doing things on your own, being critical of
existing tools, bla bla. How are you supposed to do that?

### The eyes in your head

The best tool in your belt is a curious attitude. Be critical of your
data at every step in the pipeline. Does it look the way you expect? How
can you check? It's wise to *look* at your data, and
look at it a lot, before moving on to the next step. It will also save
you some headaches later on by knowing what happened in the middle.

### The sweat of your brow

What does it mean to "look" at your data? The answer is that you'll need some
computational skills. By "computational" I mean "command-line".  This means
familiarity with the basic tools of the Unix terminal (`cat`, `cd`, `cp`, `ls`,
`mkdir`, `mv`, `rm`, `head`, `less`, `sed` or `awk`, `wc`, `grep`, and `vi` or
`emacs`) and the ability to use some programming language.

You *can* open OTU tables in Excel or whatever, but if you try to use the more
familiar office-sytle software to do the heavy lifting here, you will be
disappointed. Opening a 5 Gb fastq in Notepad or TextEdit won't be fun. Maybe
one day we'll have sexy drag-and-drop, hologram-style data processing for 16S,
but for the foreseeable future it's going to look like the scene in *Jurassic
Park* where Samuel L. Jackson is hunched over a computer muttering "Access
main program...  Access main security... Access main program grid... Please!
Goddamn it! Hate this hacker crap!"

### A programming language

Those simple command-line tools will get you pretty far, but as some point
you'll want to ask a question of your data or do something to your data
that isn't exactly standard. At that point, you'll need to be able to
write a program.

Here are some criteria to help you decide what language is best for you:

- *Support*. You'll have a better time using a language that has good
  documentation, a large global community of users (who produce informal
  documentation in places like [StackOverflow](http://www.stackoverflow.com)),
  and a local community of users, i.e., the person down the hall who can help
  you figure out what that syntax error means.
- *Bioinformatics packages.* It's nice to not re-invent the wheel.  Some
  programming languages have mature, extensive bioinformatics toolkits.
- *Appropriateness for your purpose*. Compiled programming languages run fast
  but are slow to develop; scripting languages run slow but are fast to
  develop. If you're going to be crunching huge datasets that will take days to
  process, think about a compiled language designed for parallelization. If
  you're just working on a few small datasets on your own computer, think about
  a scripting language that's easier to use.

My language of choice for 16S data processing is
[Python](http://www.python.org). It's a popular language with great
documentation. The people around me use it. It has a good bioinformatics
package (`biopython`). It's relatively slow but I don't care because I spend
much more time programming that I do actually running data.

I think [Perl](http://www.perl.org) used to be the most popular bioinformatics
programming language, and I think it's being displaced by Python.
[`R`](http://www.r-project.org) is a great language for analyzing making plots
and doing statistics on the resulting OTU tables, but it's not super-handy for
working with raw sequences. Some people will swear by working in C or C++, but
I think you should wait until you really need a 10-fold speedup before going
that deep.  Apparently [Matlab](http://www.mathworks.com/products/matlab) has
some bioinformatics capability.  [Julia](http://julialang.org) might one day be
a cool option.

## Some early challenges

### Rolling your own

I hear a lot of people say they want to build computational skills.
The way you do that is by learning more and building stuff. Personal
anecdote: I worked for a year in a lab that used Fortran to do most
of its computation. I had previously done most of my computational work
in Mathematica (I was a physics major). After a few months, I
took off one full week of work to read and do all the exercises in
Mark Lutz's _Learning Python_. It was one of the best investments I've
ever made. You learn more by putting in the time. It will pay off.

Another personal anecdote: after working with QIIME and then with another grad
student's codebase, I finally decided to write my own [16S processing
software](https://github.com/swo/caravan) from scratch.  I learned most of
what's in this document as I learned what I had to do to write that software.
If starting with a real big kid script that does real data processing sounds
like too much, try working on the problems at
[Rosalind](http://www.rosalind.info).  They start out easy and get
progressively harder. It's a nice way to do something for a half hour and get
the instant gratification of a gold star.

### Looking at real data

If you're reading this packet, you probably have your own data set in hand. If
not, two great places to get some data to play with are the HMP project's [raw
sequences](http://hmpdacc.org/HMR16S) or the data generated in [Caporaso *et
al.*](http://dx.doi.org/10.1186/gb-2011-12-5-r50) from
[MG-RAST](http://metagenomics.anl.gov).
