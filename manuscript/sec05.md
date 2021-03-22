# Nuts and bolts of 16S data processing

## Existing tools

Everything in this document up to this point will help you be critical
of an analysis pipeline. This is true whether you use an existing
pipeline, work with someone who has a pipeline, or make your own
pipeline. The more you want to be involved in looking at and working
with your own data, the more computer skills you'll need. You'll also
need more of your own skills if you want to do more creative analysis or
be more sure of exactly what's being done with your data.[^fault]

[^fault]: This all being said, I don't fault anyone for using tools that
  actually *work*. Some of the theoretically "nicer" tools aren't coded in a
  way that makes them easy to use, robust, or capable of working on big
  datasets. Many theoretically nice tools don't have good documentation, which
  makes them essentially unusable.

### QIIME

The great and mighty [QIIME](http://www.qiime.org) is a big part of the 16S
data processing landscape. QIIME was one of the two big pipelines used to
analyze the HMP data. I see the taxa plots produced by QIIME in many papers.

### usearch

The great and mighty [`usearch`](http://www.drive5.com/usearch) underlies a lot
of 16S data processing.  A lot of QIIME is built on the back of `usearch`.
`usearch` is a single program that has an ever-growing number of
functionalities (including, the algorithms USEARCH, UCLUST, and UPARSE).

Because USEARCH is so widely used, I will take a moment to dive a little more
deeply into its workings. I have seen a lot of confusion arise because of
USEARCH, mostly because users (like me!) expected USEARCH to do one thing when,
in fact, it does something else. The caveats I'm going to lay out apply if
you're using USEARCH via `usearch`, QIIME, or another pipeline.

Critically, USEARCH is a *heuristic* algorithm. This means that it applies some
shortcuts to achieve faster speed (i.e., orders of magnitude faster than simple
BLAST). In the [paper](http://dx.doi.org/10.1093/bioinformatics/btq461), Mr. Edgar
explains that USEARCH gets its speed-up from three places.

1. Search for a match according to a decreasing expected sequence similarity.
2. Use heuristics to speed up the sequence alignments.
3. Apply stopping criteria. The default is to stop after a single hit that meets the accepting criteria.

The first rule means that your query sequence will be compared to database
sequences according to some order; the third rule means that the first of these
database sequences that is a sufficiently good match to your query will be
delivered as the result. For example, if you are assigning your OTUs by making
a search to the 97% OTUs in Greengenes, then the first database sequence that
is at least 97% similar to your query will be considered its parent OTU.

This would be of no concern if the comparisons were performed in the order of
decreasing sequence similarity. Then the first hit would be the best one.
This, however, puts the cart before the horse: you need to somehow *guess*
which sequence will be the best match before actually performing the alignment.

USEARCH guesses the sequence similarity between two sequences using the *U*
value (which is the U in USEARCH). *U* is the number of unique *words* shared
by two sequences. You get these words by looking for length *w* (default is 8)
subsequences starting at positions spaced $\mu$ apart. For example, if
$\mu = 1$, then your words are all the *w*-mers in the sequence. If
$\mu = w$, then your words are the first *w* nucleotides, the next *w*
nucleotides, and so forth. Conveniently, sensible values for $\mu$
are inferred using tables of optimal choices derived from running USEARCH
on databases of sequences using different values of the identity threshold.

This heuristic selection of database entries for comparison can lead to some
quirky results. When working on a mouse microbiome project, I found that many
sequences in my dataset were very similar (say, one nucleotide different in a
250 nucleotide amplicon) but ended up in different 97% OTUs. I've heard stories
of people who discovered this quirk when they called OTUs *de novo* and using
reference-based calling. They expected that since their *de novo* and
reference-based OTUs were both 97%, they should be about the same "size",
except that reference-based OTU calling would miss some of the OTUs that *de
novo* calling would catch. In fact, this approach usually leads to *more* OTUs
in the reference-based calling.

In light of these weird effects, I caution you to carefully read the `usearch`
documentation to get a rough sense of what it's doing. I got weird results for
some years before I started to dig into what `usearch` was actually doing.
Don't expect it to do something that it doesn't do!

Overall, the nice thing about `usearch` is that
it's built by someone who's very concerned about making a fast, optimized
tool. The potentially nice thing about `usearch` is that it's pretty
low-level: if you want to do some medium-lifting (like primer removal
and demultiplexing) but not heavy-lifting (like merging, quality
filtering, clustering, or sequence alignment), then `usearch` is for
you.

A potentially bad thing about `usearch` is that it's made by a single person
and is closed source. It also comes with a funny caveat: newer versions of
`usearch` come in two flavors, free and wildly expensive. This means that mere
mortals (i.e., non-Broadies) must be content to use the free version, which
will only process 2 Gb of data at a time.[^vsearch] If you need to call OTUs
*de novo* from an enormous data set, then you're sunk; if you merely want to
merge, quality filter, or do alignments, then it's merely annoying.[^split]
QIIME comes with an older version of `usearch` that doesn't have as many
features but which also doesn't have the memory restriction.

[^split]: Most other things you do with 16S data are parallelizable: you don't
  need to hold the entire dataset in memory at once, you just need little parts
  of it. For example, if you want to use `usearch` to merge a big paired-end
  dataset, you can split the forward and reverse read files into smaller chunks
  and merge each pair of chunks one-by-one.

[^vsearch]: The closed-source and the wildly-expensive problems might be solved
  by an open-source implementation of USEARCH and the other algorithms, as is
  being developed under the creative name
  [VSEARCH](http://dx.doi.org/10.7287/peerj.preprints.2409v1), where I think
  the V stands for "versatile".

### mothur

Similar to QIIME, [mothur](http://www.mothur.org) aims to be "a single
piece of open-source, expandable software to fill the bioinformatics
needs of the microbial ecology community". Their website says mothur
is "currently the most cited bioinformatics tool for analyzing 16S rRNA gene sequences."
Mothur was the other big pipeline used to analyze the HMP data.

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
