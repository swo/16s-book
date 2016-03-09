Practice
========

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

File formats
------------

The two important file formats are the above-mentioned *fastq* and the
*fasta*. Fastq is an Illumina-specific raw data format. Fasta is the
industry-standard way to display processed sequence data. Sequence data
on Genbank, for example, is mostly in fasta format.

### Fastq format

Fastq files usually have the extension `.fastq` or `.fq`. Fastq files
are human-readable. They are made up of *entries* that each correspond
to a single read. Every entry is four lines.[^6] A well-formed fastq
file has a number of lines that is a multiple of four. You can see how
many lines are in a file using the terminal command `wc -l foo.fq`.
Divide that by four to get the number of entries. The lines in the entry
are:

1.  The *header* line (or "at" line). It must begin with the
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
    purine (A or G). `N` means "no idea, any base possible".

3.  The *plus* line. It must being with the plus-character `+`.
    Stupidly, it can contain anything. Most people set it to the same
    thing as the at-line (which is a waste of computer memory)
    or nothing. If I could go back in time and make fastq entries just
    three lines, I would.

4.  The *quality* line. Every nucleotide in the sequence line has an
    associated quality. Qualities are encoded by letters on the
    quality line. Confusingly, this encoding has changed in overlapping
    and sometimes non-redundant ways. In the newest Illumina format, the
    encoding goes, from low quality to high quality:
    `!#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHI`. `I` means that there is
    a $10^{-4.1}$ probability that this base is wrong (i.e., a 99.99%
    chance that it is correct). `H` means that there is a $10^{-4.0}$
    chance; `G` means $10^{-3.9}$, and so on down to ``. The exclamation
    point is special: it means a quality of zero, i.e., that the
    sequencer has no idea what that base is.

Here's an example fastq entry. The sequence and quality lines are too
long to fit on the page, so I cut out some letters in the middle and put
those red dots instead. Notice how the quality of the read decreases
(all the way down to `#`) toward the end of the read. The barcode read
is `CCGACA` and the `/1` shows that this is a forward read.

``

\[t\]<span>1</span>`@MISEQ578:1:1101:15129:1752#CCGACA/1`

`TATGGTGCCAGCCGCCGCGGTA````GCGAAGGCGGCTCACTGGCTCGATACTGACGCTGAG`

`+`

`>1>11B11B11>A1AA0A00E/````FF@@<@FF@@@@FFFFFFEFF@;FE@FF/9-AAB##`

### Fasta format

Fasta files usually have the extension `.fasta`, `.fa`, or `.fna`. Fasta
files are human-readable. They are made up of *entries* that each
correspond to a single sequence. Each entry has this format:

1.  A *header* line that starts with `>`. This signals the start of a
    new entry. The stuff after `>` is usually some kind of ID that names
    this sequence. There might be other information there too.

2.  A number of *sequence* lines. The linebreaks are not meaningful: the
    sequence for this entry just keeps on going until you hit another
    `>`. The early recommendation was to wrap all lines at 80 characters
    to make them easy to read on old-school terminals. Many people and
    software tools conform to this recommendation; others make each
    entry just two lines, one header and one sequence. Both are allowed.

Fasta files provide less information than fastq files, so normally
you'll move to a fasta format when you've decided you aren't going to
look at the quality data again, typically after quality filtering.

Here's an example fasta entry in the traditional format (i.e., each line
no more than 80 characters, with the sequence spread over multiple
lines).

\[t\]<span>1</span>`>seq1;size=1409414;`

`TACGGAGGATCCGAGCGTTATCCGGATTTATTGGGTTTAAAGGGAGCGTAGGCGGGTTGT TAAGTCAGTTGTGAAAGTTTGCGGCTCAACCGTAAAATTGCAGTTGATACTGGCATCCTT GAGTACAGTAGAGGTAGGCGGAATTCGTGGTGTAGCGGTGAAATGCTTAGATATCACGAA GAACTCCGATTGCGAAGGCAGCCTGCTGGACTGTAACTGACGCTGATGCTCGAAAGTGTG`

`GGTATCAAACAGG`

### Other formats

I've been talking about Illumina, but the other important data type
comes from 454 sequencing. Raw 454 data comes in *sff* format. Unlike
fastq files, sff files are not human-readable. Luckily, you can convert
sff files to fastq files with only a minor loss of information.
Unluckily, 454 sequence data has its own in's and out's that are beyond
the scope of this document. Caveat sequentor.[^7]

Tools
-----

Everything in this document up to this point will help you be critical
of an analysis pipeline. This is true whether you use an existing
pipeline, work with someone who has a pipeline, or make your own
pipeline. The more you want to be involved in looking at and working
with your own data, the more computer skills you'll need. You'll also
need more of your own skills if you want to do more creative analysis or
be more sure of exactly what's being done with your data.

### Existing tools

The great and mighty QIIME dominates the 16S data processing landscape.
I won't say you should or shouldn't use QIIME, but I will say that,
regardless of which tool you're using, you should know *what* it's
doing. If you're happy to trust the QIIME maintainers to have made a
sensible tool, then go download that and start reading their
documentation. If you're feeling more inquisitive, read on.

### Usearch

The great and mighty `usearch` underlies a lot of 16S data processing.
QIIME is built on the back of `usearch`. `usearch` is a single program
that has an ever-growing number of functionalities (including, the
algorithms usearch and uclust). The nice thing about `usearch` is that
it's built by a guy who's very concerned about making a fast, optimized
tool. The potentially nice thing about usearch is that it's pretty
low-level: if you want to do some medium-lifting (like primer removal
and demultiplexing) but not heavy-lifting (like merging, quality
filtering, clustering, or sequence alignment), then `usearch` is for
you. The potentially bad thing about `usearch` is that it's made by a
single guy and is closed source. He describes his methods, but no one
can check the code to make sure it does what he says it does.

`usearch` also has a funny caveat: newer versions come in two flavors,
free and wildly expensive. This means that mere mortals (i.e.,
non-Broadies) must be content to use the free version, which will only
process 2 Gb of data at a time. If you need to call OTUs *de novo* from
an enormous data set, then you're sunk; if you merely want to merge,
quality filter, or do alignments, then it's merely annoying. QIIME comes
with an older version of `usearch` that doesn't have as many
capabilities but which doesn't have the memory restriction.

### The eyes in your head

The best tool in your belt is a curious attitude. Be critical of your
data at every step in the pipeline. Does it look the way you expect? How
can you check? More often than not it's wise to *look* at your data, and
look at it a lot, before moving on to the next step. It will also save
you some headaches later on by knowing what happened in the middle.

You spent a lot of time and energy collected the samples and making the
sequencing libraries, so you shouldn't be flippant about processing your
data.

### The sweat of your brow

The second best tool is some computational skills. This means
familiarity with the basic tools of the Unix terminal (`cat`, `cd`,
`cp`, `ls`, `mkdir`, `mv`, `rm`, `head`, `less`, `sed` or `awk`, `wc`,
and `grep`) and the ability to use some programming language. Rather
than say what programming language is best, I'll share some criteria to
help you decide what language is best:

-   *Support*. You'll have a better time using a language that has good
    documentation, a large global community of users (who produce
    informal documentation in places like StackOverflow), and a local
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

My language of choice for 16S data processing is Python. It's a popular
language with great documentation. The people around me use it. It has a
good bioinformatics package (biopython). It's relatively slow but I
don't care because I spend much more time programming that I do actually
running data.

