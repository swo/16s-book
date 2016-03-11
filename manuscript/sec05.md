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
industry-standard way to display processed sequence data. The sequence data
on Genbank, for example, is mostly in fasta format.

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
    flowcell lane, the position of the read on the cell, and which part
    of a paired-end read this read is. In some version of Illumina, the
    barcode read is here. You can also add whatever other information
    you want to this line. For example, fastqs on NCBI might have
    `length=1234` somewhere after all the Illumina stuff.

2.  The *sequence* line. Just like it sounds: a series of letters. Note
    that they might not all be `ACGT`: other letters are allowed to say
    that it might be any of a group of bases. For example, `R` means
    purine (A or G). `N` means "no idea, any base possible".[^iupac]
	
[^iupac]: These other options are the IUPAC nucleotide abbreviations. There is a one-letter code for every combination of the four nucleotides.

3.  The *plus* line. It must begin with the plus-character `+`.
    Stupidly, it can contain anything. Most people set it to the same
    thing as the at-line (which is a waste of space)
    or nothing. If I could go back in time and make fastq entries just
    three lines, I would.

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
	
[^ascii]: Technically, these different encodings are named by their ASCII "offsets". ASCII is a system that associates individual characters with integers. The system I show here has an ASCII offset of 33: the character `I` has an ASCII value of 73, and the offset means you subtract 33 from 73 to get 40. The other common offset is 64: in that case, the character `I` encodes a quality 9. Illumina used a 64 character offset for a while, but newer machines use a 33 character offset. You can tell the difference getting familiar with the characters used and just looking by eye, by running your pipeline and seeing if it breaks, or using a tool like `usearch -fastq_chars` to figure out what the offset is.

[^phred]: This conversion between quality {$$}Q{/$$} (the integer) and the probability {$$}p{/$$} of incorrect calling is the "Phred" or "Sanger" system: {$$}Q = -10 \log_{10} p{/$$}, or equivalently, {$$}p = 10^{-Q/10}{/$$}. There is at least one other way of converting between {$$}Q{/$$} and {$$}p{/$$}, which is called the "Solexa" system.

[^excl]: Even more confusingly, in some versions of Illumina, the very low ASCII scores were used to mean special things. In the older, 64-offset Illumina encoding, quality 3 (`C`) was the lowest possible, and the quality 2 character (`B`) was instead used to show that the Illumina software had done its own internal quality trimming and had decided that, starting with the first `B`, that the rest of the sequence was "bad". To my relief, this weird system is not used in the newer Illumina (versions 1.8 and above). I personally think the sequencer should give you *just* raw data, not some combination or raw data and partially-processed data.

Here's an example fastq entry. The sequence and quality lines are too
long to fit on the page, so I cut out some letters in the middle and put
those dots instead. Notice how the quality of the read decreases
(all the way down to quality 2, encoded by the hash symbol `#`) toward the end of the read. The barcode read
is `CCGACA` and the `/1` shows that this is a forward read.

    @MISEQ578:1:1101:15129:1752#CCGACA/1
    TATGGTGCCAGCCGCCGCGGTA...GCGAAGGCGGCTCACTGGCTCGATACTGACGCTGAG
    +
    >1>11B11B11>A1AA0A00E/...FF@@<@FF@@@@FFFFFFEFF@;FE@FF/9-AAB##

### Fasta format

Fasta files usually have the extension `.fasta`, `.fa`, or `.fna`. Fasta
files are human-readable. They are made up of *entries* that each
correspond to a single sequence. Each entry has this format:

1.  A *header* line that starts with the greater-than symbol `>`.
	This signals the start of a
    new entry. The stuff after `>` is usually some kind of ID that names
    this sequence. There might be other information there too.

2.  One or more *sequence* lines. The linebreaks are not meaningful: the
    sequence for this entry just keeps on going until you hit another
    `>`. The early recommendation was to wrap all lines at 80 characters
    to make them easy to read on old-school terminals. Many people and
    software tools conform to this recommendation; others make each
    entry just two lines, one header and one sequence. Both are allowed.

Fasta files provide less information than fastq files, so normally
you'll move to a fasta format when you've decided you aren't going to
look at the quality data again, say, after quality filtering.

Here's an example fasta entry in the traditional format (i.e., each line
no more than 80 characters, with the sequence spread over multiple
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

I won't say you should or shouldn't use QIIME, but I will say that,
regardless of which tool you're using, you should know *what* it's
doing. If you're happy to trust the QIIME maintainers to have made a
sensible tool, then go download that and start reading their
documentation. If you're feeling more inquisitive, read on.

### usearch

The great and mighty [`usearch`](http://www.drive5.com/usearch/)
underlies a lot of 16S data processing.
A lot of QIIME is built on the back of `usearch`. `usearch` is a single program
that has an ever-growing number of functionalities (including, the
algorithms USEACRH, UCLUST, and UPARSE). The nice thing about `usearch` is that
it's built by someone who's very concerned about making a fast, optimized
tool. The potentially nice thing about usearch is that it's pretty
low-level: if you want to do some medium-lifting (like primer removal
and demultiplexing) but not heavy-lifting (like merging, quality
filtering, clustering, or sequence alignment), then `usearch` is for
you. The potentially bad thing about `usearch` is that it's made by a
single person and is closed source.[^caution]

[^caution]: I caution you to carefully read the `usearch` documentation to get a rough sense of what it's doing. I got weird results for some years before I started to dig into what `usearch` was actually doing. In short, a lot of `usearch`'s capabilities are heuristic, which can be confusing if you interpret them as if they were deterministic. For example, when I used `usearch -fastq_mergepairs` to merge amplicons, I sometimes got weird results, different from what I got if I just merged sequences in a slower, dumber way. This either means I'm confused or that `usearch` does some kind of heuristic alignment when merging. Also cf. the footnote about usearch in the last chapter. 

`usearch` also has a funny caveat: newer versions come in two flavors,
free and wildly expensive. This means that mere mortals (i.e.,
non-Broadies) must be content to use the free version, which will only
process 2 Gb of data at a time. If you need to call OTUs *de novo* from
an enormous data set, then you're sunk; if you merely want to merge,
quality filter, or do alignments, then it's merely annoying.[^split] QIIME comes
with an older version of `usearch` that doesn't have as many
capabilities but which doesn't have the memory restriction.

[^split]: Most other things you do with 16S data are parallelizable: you don't need to hold the entire dataset in memory at once, you just need little parts of it. For example, if you want to use `usearch` to merge a big paired-end dataset, you can split the forward and reverse read files into smaller chunks and merge each pair of chunks one-by-one.

### mothur

Like QIIME, [mothur](http://www.mothur.org/) aims to be "a single
piece of open-source, expandable software to fill the bioinformatics
needs of the microbial ecology community". Their website says mothur
is "currently the most cited bioinformatics tool for analyzing 16S rRNA gene sequences."
Mothur was the other big pipeline used to analyze the HMP data.
I'm more familiar with QIIME than mothur, so I'll simply say the
same thing that I said again, that I encourage you to be a critical
consumer of your tools. There's still a sausage being made somewhere.

## Your own tools

I've kept yammering about doing things on your own, being critical of
existing tools, bla bla. How are you supposed to do that?

### The eyes in your head

The best tool in your belt is a curious attitude. Be critical of your
data at every step in the pipeline. Does it look the way you expect? How
can you check? It's wise to *look* at your data, and
look at it a lot, before moving on to the next step. It will also save
you some headaches later on by knowing what happened in the middle.

You spent a lot of time and energy collected the samples and making the
sequencing libraries, so you shouldn't be flippant about processing your
data.

### The sweat of your brow

What does it mean to "look" at your data? The answer is that you'll need
some computational skills. By "computational" I mean "command-line".
This means
familiarity with the basic tools of the Unix terminal (`cat`, `cd`,
`cp`, `ls`, `mkdir`, `mv`, `rm`, `head`, `less`, `sed` or `awk`, `wc`,
 `grep`, and `vi` or `emacs`) and the ability to use some programming language.
 
You can open OTU tables in Excel or whatever, but if you try to use the
more familiar office-sytle software to do the heavy lifting here, you
will be disappointed. Opening a 5 Gb fastq in Notepad or Textedit or
whatever isn't fun. Maybe one day we'll have sexy graphical, drag-and-drop,
hologram-style data processing for 16S, but for the foreseeable future
it's going to look like the computer scenes in *Jurassic Park*[^park].

[^park]: And not the one where the girl is zooming around in a weird "Unix" GUI; I mean the one where Samuel L. Jackson mutters "access main program... access main security... access program grid..."
 
### A programming language

Those simple command-line tools will get you pretty far, but as some point
you'll want to ask a question of your data or do something to your data
that isn't exactly standard. At that point, you'll need to be able to
write a program.

Rather
than say what programming language is best, I'll share some criteria to
help you decide what language is best:

-   *Support*. You'll have a better time using a language that has good
    documentation, a large global community of users (who produce
    informal documentation in places like [StackOverflow](http://www.stackoverflow.com), and a local
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
[`R`](http://www.r-project.org/) is a great language for analyzing
making plots and doing statistics on the resulting OTU tables, but
it's not super-handy for working with raw sequences. Some people will
swear by working in C or C++, but I think you should wait until you
really need a 10-fold speedup before going that deep. [Matlab](http://www.mathworks.com/products/matlab/)
has some bioinformatics capability, but I don't know much about it.
[Julia](http://julialang.org/) might one day be a cool option.

## Some early challenges

### Rolling your own

I hear a lot of people say they want to build computational skills.
The way you do that is by learning more and building stuff. Personal
anecdote: I worked for a year in a lab that used Fortran to do most
of its computation. I had previously done most of my computational work
in Mathematica (since I was a physics major). After a few months, I
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
They start out easy and get progressively harder. It can be a nice way
to do something for a half hour and get a gold star. The instant
gratification can be a relief.

### Looking at real data

If you're reading this packet, you probably have your own data set
in hand. If not, two great places to get some data to play with are
the HMP project's [raw sequences](http://hmpdacc.org/HMR16S) or the
data generated in [Caporaso *et al.*](10.1186/gb-2011-12-5-r50) from
[MG-RAST](http://metagenomics.anl.gov).
