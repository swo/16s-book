# Practice

As you can see, there are a lot of in's, out's, and what-have-you's
(IOWHYs) to processing 16S data. Rather than giving you the fish of some
monolithic pipeline, I'd rather try to teach you as much about fish as
you'll find useful. There are plenty of websites that can give you fish
but not many that can introduce you to the IOWHYs.

In the rest of this document, I'll assume you're in a Unix/Linux/Mac
world. If you're on Windows, you'll essentially need to get to the Unix
world with a tool like Cygwin. I didn't make up those rules, but that's
how it is: all the serious bioinformatics are done in the non-Windows
world.

## File formats

The two important file formats are the above-mentioned *fastq* and the
*fasta*. Fastq is an Illumina-specific raw data format. Fasta is the
industry-standard way to display processed sequence data.

### Fastq format

Fastq files usually have the extension `.fastq` or `.fq`. Fastq files
are human-readable. They are made up of *entries* that each correspond
to a single read. Every entry is four lines.[^line] A well-formed fastq
file has a number of lines that is a multiple of four. You can see how
many lines are in a file using the terminal command `wc -l foo.fq`.
Divide that by four to get the number of entries. The lines in the entry
are:

[^line]: Confusingly, the definition of a "line" on Windows is different from Unix/Linux/Mac. If you ever pass data between these two computer systems, make sure that have adjusted the line endings using `dos2unix` (or `unix2dos`). You can also look up how to do this with `tr`, etc.

1. The *header* line (or "at" line). It must begin with the
    at-character `@`. The format of the rest of the line depends on the
    Illumina software version, but in general it gives information about
    the read: the name of the instrument it was sequenced on, the
    flowcell lane, the position of the read on the cell, and whether it
    is a forward or reverse read. In some version of Illumina, the
    barcode read is in the read's header. You can put whatever information
    you want in this line. For example, fastqs on NCBI might have
    `length=1234` somewhere after all the Illumina stuff.
2.  The *sequence* line. Just like it sounds: a series of letters. Note
    that they might not all be `ACGT`: other letters are allowed to say
    that it might be any of a group of bases. For example, `R` means
    purine (`A` or `G`). `N` means "no idea, any base possible".[^iupac]
3.  The *plus* line. It must begin with the plus-character `+`.
    Bizarrely, it can contain anything. Most people set it to the same
    thing as the at-line (which is a waste of space)
    or nothing.[^plusline]
4.  The *quality* line. Every nucleotide in the sequence line has an
    associated quality. Qualities are encoded by letters on the
    quality line. Confusingly, this encoding has changed in overlapping
    and sometimes non-redundant ways.[^ascii] In the newest Illumina format, the
    encoding goes, from low quality to high quality:

    ~~~~~~~~
    !#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHI
    ~~~~~~~~

    The letter `I` means that there is
    a {$$}10^{-4.0}{/$$} probability that this base is wrong (i.e., a 99.99%
    chance that it is correct). `H` means that there is a {$$}10^{-3.9}{/$$}
    chance; `G` means {$$}10^{-3.8}{/$$}, and so on.[^phred] The exclamation
    point is special: it means a quality of zero, i.e., that the
    sequencer has no idea what that base is.[^excl]
	
[^iupac]: These other options are the IUPAC nucleotide abbreviations. There is a one-letter code for every possible combination of the four nucleotides.
[^ascii]: Technically, these different encodings are named by their ASCII "offsets". ASCII is a system that associates individual characters with integers. The system I show here has an ASCII offset of 33: the character `I` has an ASCII value of 73, and the offset means you subtract the offset 33 from the ASCII value 73 to get the quality score 40. The other common offset is 64: in that case, the character `I` encodes quality 9. Illumina used a 64-offset for a while, but newer machines use a 33-offset. You can tell the difference getting familiar with the characters used and just looking by eye, by running your pipeline and seeing if it breaks, or by using a tool like `usearch -fastq_chars`.
[^plusline]: The original fastq [specification](http://dx.doi.org/10.1093/nar/gkp1137) (doi:10.1093/nar/gkp1137) allowed the sequence and quality information to run over multiple lines (like in the fasta format). This led to a lot of confusion, since `+` and `@` appear in some quality encodings. So it's now recommended to *not* spread the sequence and quality information over multiple lines. Thus, the plus line is there for backward compatibility.
[^phred]: This conversion between quality {$$}Q{/$$} (the integer) and the probability {$$}p{/$$} of incorrect calling is the "Phred" or "Sanger" system: {$$}Q = -10 \log_{10} p{/$$}, or equivalently, {$$}p = 10^{-Q/10}{/$$}. There is at least one other way of converting between {$$}Q{/$$} and {$$}p{/$$}, the "Solexa" system.
[^excl]: Even more confusingly, in some versions of Illumina, the very low ASCII scores were used to mean special things. In the older, 64-offset Illumina encoding, quality 3 (character `C`) was the lowest possible, and the quality 2 character (character `B`) was instead used to show that the Illumina software had done its own internal quality trimming and had decided that, starting with the first `B`, that the rest of the sequence was "bad". To my relief, this weird system is not used in the newer Illumina (versions 1.8 and above). I personally think the sequencer should give you *just* raw data, not some combination or raw data and partially-processed data.

Here's an example fastq entry. The sequence and quality lines are too
long to fit on the page, so I cut out some letters in the middle and put
those dots instead. Notice how the quality of the read decreases
(all the way down to quality 2, encoded by the hash symbol `#`) toward the end of the read. The barcode read
is `CCGACA`. The `/1` at the end of the first line shows that this is a forward read.

    @MISEQ578:1:1101:15129:1752#CCGACA/1
    TATGGTGCCAGCCGCCGCGGTA...GCGAAGGCGGCTCACTGGCTCGATACTGACGCTGAG
    +
    >1>11B11B11>A1AA0A00E/...FF@@<@FF@@@@FFFFFFEFF@;FE@FF/9-AAB##

### Fasta format

Fasta files usually have the extension `.fasta`, `.fa`, or `.fna`.[^fasta] Fasta
files are human-readable. They are made up of *entries* that each
correspond to a single sequence. Each entry has this format:

1.  A *header* line that starts with the greater-than symbol `>`.
	This signals the start of a
    new entry. The stuff after `>` is usually some kind of ID that names
    this sequence. There might be other information there too.
2.  One or more *sequence* lines. The line breaks are not meaningful: the
    sequence for this entry just keeps on going until you hit another
    `>`. The early recommendation was to wrap all lines at 80 characters
    to make them easy to read on old-school terminals. Many people and
    software tools conform to this recommendation; others make each
    entry just two lines, one header and one sequence. Both are allowed.

[^fasta]: The last `a` in `fasta` stands for "all", meaning nucleotide or amino acid or whatever. The `n` in `fna` stands for "nucleotide".

Fasta files provide less information than fastq files, so normally
you'll move to a fasta format when you've decided you aren't going to
look at the quality data again, i.e., after quality filtering.

Here's an example fasta entry in the traditional format (i.e., each line
no more than 80 characters and the sequence is spread over multiple
lines).

~~~~~~~~
>seq1;size=1409414;
TACGGAGGATCCGAGCGTTATCCGGATTTATTGGGTTTAAAGGGAGCGTAGGCGGGTTGT 
TAAGTCAGTTGTGAAAGTTTGCGGCTCAACCGTAAAATTGCAGTTGATACTGGCATCCTT 
GAGTACAGTAGAGGTAGGCGGAATTCGTGGTGTAGCGGTGAAATGCTTAGATATCACGAA 
GAACTCCGATTGCGAAGGCAGCCTGCTGGACTGTAACTGACGCTGATGCTCGAAAGTGTG
GGTATCAAACAGG
~~~~~~~~

### Other formats

I've been talking about Illumina, but the other important data type
comes from 454 sequencing. Raw 454 data comes in *sff* format. Unlike
fastq files, sff files are not human-readable. Luckily, you can convert
sff files to fastq files pretty easily.[^sff]
Unluckily, 454 sequence data has its own in's and out's that are beyond
the scope of this document. Caveat sequentor.[^latin1]

[^sff]: 454 sequencing is a fundamentally different technology from Illumina, so converting the raw sff to fastq involves some inference and processing. sff files are not human-readable, so you'll probably want to use a ready-made tool like `biopython`'s `convert` command or a tool like `sff2fastq`.

[^latin1]: That's a joke for Latin scholars. It's meant to mean "let the one processing the data beware".

## Existing tools

Everything in this document up to this point will help you be critical
of an analysis pipeline. This is true whether you use an existing
pipeline, work with someone who has a pipeline, or make your own
pipeline. The more you want to be involved in looking at and working
with your own data, the more computer skills you'll need. You'll also
need more of your own skills if you want to do more creative analysis or
be more sure of exactly what's being done with your data.[^fault]

[^fault]: This all being said, I don't fault anyone for using tools that actually *work*. Some of the theoretically "nicer" tools aren't coded in a way that makes them easy to use, robust, or capable of working on big datasets. Many theoretically nice tools don't have good documentation, which makes them essentially unusable.

### QIIME

The great and mighty [QIIME](http://www.qiime.org) is a big part of
the 16S data processing landscape. QIIME was one of the two big
pipelines used to analyze the HMP data. I see the taxa plots produced
by QIIME in many papers.

### usearch

The great and mighty [`usearch`](http://www.drive5.com/usearch)
underlies a lot of 16S data processing.
A lot of QIIME is built on the back of `usearch`. `usearch` is a single program
that has an ever-growing number of functionalities (including, the
algorithms USEARCH, UCLUST, and UPARSE).

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
subsequences starting at positions spaced {$$}\mu{/$$} apart. For example, if
{$$}\mu = 1{/$$}, then your words are all the *w*-mers in the sequence. If
{$$}\mu = w{/$$}, then your words are the first *w* nucleotides, the next *w*
nucleotides, and so forth. Conveniently, sensible values for {$$}\mu{/$$}
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
in the reference-based calling. I wrote a [blog
post](http://microbiome.mit.edu/2016/02/07/usearch/) unpacking this phenomenon.

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

A potentially bad thing about `usearch` is that it's made by a
single person and is closed source. It also comes with
a funny caveat: newer versions of `usearch` come in two flavors,
free and wildly expensive. This means that mere mortals (i.e.,
non-Broadies) must be content to use the free version, which will only
process 2 Gb of data at a time.[^vsearch] If you need to call OTUs *de novo* from
an enormous data set, then you're sunk; if you merely want to merge,
quality filter, or do alignments, then it's merely annoying.[^split] QIIME comes
with an older version of `usearch` that doesn't have as many
features but which also doesn't have the memory restriction.

[^split]: Most other things you do with 16S data are parallelizable: you don't need to hold the entire dataset in memory at once, you just need little parts of it. For example, if you want to use `usearch` to merge a big paired-end dataset, you can split the forward and reverse read files into smaller chunks and merge each pair of chunks one-by-one.

[^vsearch]: The closed-source and the wildly-expensive problems might be solved by an open-source implementation of USEARCH and the other algorithms, as is being developed under the creative name [VSEARCH](http://dx.doi.org/10.7287/peerj.preprints.2409v1), where I think the V stands for "versatile".

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

What does it mean to "look" at your data? The answer is that you'll need
some computational skills. By "computational" I mean "command-line".
This means
familiarity with the basic tools of the Unix terminal (`cat`, `cd`,
`cp`, `ls`, `mkdir`, `mv`, `rm`, `head`, `less`, `sed` or `awk`, `wc`,
 `grep`, and `vi` or `emacs`) and the ability to use some programming language.
 
You *can* open OTU tables in Excel or whatever, but if you try to use the
more familiar office-sytle software to do the heavy lifting here, you
will be disappointed. Opening a 5 Gb fastq in Notepad or TextEdit 
won't be fun. Maybe one day we'll have sexy drag-and-drop,
hologram-style data processing for 16S, but for the foreseeable future
it's going to look like the scene in *Jurassic Park* where Samuel L.
Jackson is hunched over a computer muttering "Access main program... 
Access main security... Access main program grid... Please! Goddamn it!
Hate this hacker crap!"
 
### A programming language

Those simple command-line tools will get you pretty far, but as some point
you'll want to ask a question of your data or do something to your data
that isn't exactly standard. At that point, you'll need to be able to
write a program.

Here are some criteria to help you decide what language is best for you:

-   *Support*. You'll have a better time using a language that has good
    documentation, a large global community of users (who produce
    informal documentation in places like [StackOverflow](http://www.stackoverflow.com)), and a local
    community of users, i.e., the person down the hall who can help you
    figure out what that syntax error means.

-   *Bioinformatics packages.* It's nice to not re-invent the wheel.
    Some programming languages have mature, extensive
    bioinformatics toolkits.

-   *Appropriateness for your purpose*. Compiled programming languages
    run fast but are slow to develop; scripting languages run slow but
    are fast to develop. If you're going to be crunching huge datasets
    that will take days to process, think about a compiled language
    designed for parallelization. If you're just working on a few small
    datasets on your own computer, think about a scripting language
    that's easier to use.

My language of choice for 16S data processing is [Python](http://www.python.org). It's a popular
language with great documentation. The people around me use it. It has a
good bioinformatics package (`biopython`). It's relatively slow but I
don't care because I spend much more time programming that I do actually
running data.

I think [Perl](http://www.perl.org) used to be the most popular bioinformatics
programming language, and I think it's being displaced by Python.
[`R`](http://www.r-project.org) is a great language for analyzing
making plots and doing statistics on the resulting OTU tables, but
it's not super-handy for working with raw sequences. Some people will
swear by working in C or C++, but I think you should wait until you
really need a 10-fold speedup before going that deep.
Apparently [Matlab](http://www.mathworks.com/products/matlab)
has some bioinformatics capability.
[Julia](http://julialang.org) might one day be a cool option.

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

Another personal anecdote: after working with QIIME and then with
another grad student's codebase, I finally decided to write my own
[16S processing software](https://github.com/swo/caravan) from scratch.
I learned most of what's in this
document as I learned what I had to do to write that software. If
starting with a real big kid script that does real data processing
sounds like too much, try working on the problems at [Rosalind](http://www.rosalind.info).
They start out easy and get progressively harder. It's a nice way
to do something for a half hour and get the instant gratification of
a gold star.

### Looking at real data

If you're reading this packet, you probably have your own data set
in hand. If not, two great places to get some data to play with are
the HMP project's [raw sequences](http://hmpdacc.org/HMR16S) or the
data generated in [Caporaso *et al.*](http://dx.doi.org/10.1186/gb-2011-12-5-r50) from
[MG-RAST](http://metagenomics.anl.gov).
