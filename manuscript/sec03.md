# Data processing theory

Hooray, you have sequence data! Now what? I'll assume you did paired-end sequencing (but I'll make a note for those of you who didn't). Notably, all 454 sequencing is single-ended.

## Raw data and metadata

Before trying to process your dataset, be sure you have the following raw data[^3] and metadata:

[^3]: In what follows, I'll talk about "raw data", by which I mean data that you would get from the sequencing center. There is actually a more raw kind of data that comes right out of the sequencing machine that gets processed right away. On the Illumina platform, this data is CASAVA. Different version of CASAVA produce slightly different output, and every sequencer might have a different version of CASAVA, so be prepared for slight variations in the format of your raw data.

- *Forward reads*. For Illumina, this means a *fastq* file that might have a name like:
~~~~~~~~
`130423Alm_D13-1939_1_sequence.fastq`
~~~~~~~~
Giveaways that this is a forward read are something like `_1_` or `_R1_` in the
filename. The first line of the file should also end with `/1`. For example, the
first line of the file I have is:
~~~~~~~~
`@MISEQ578:1:1101:15129:1752#CCGACA/1`.
~~~~~~~~
- *Reverse reads* (unless you did single-end sequencing). A fastq file with a
name like the forward reads only with `_2_` or `_R2_` in it. The first line in
the file should end with `/2`, indicating that it's the second read of a pair.
Every entry in the reverse reads should match an entry in the forward reads. In
most cases, the two pairs of a read appear in analogous places in the two files
(i.e., the forward read entry starting on line *x* in the forward read file
corresponds to the reverse read starting on line *x* in the reverse reads file).
- *Barcode* or *index reads*. Depending on your Illumina version, this information might be in different places. In some datasets, it's in the file with the forward reads. In the above example line, the barcode read is `CCGACA` (between the `#` and the `/1`). In other datasets, you might find the index reads in a file with a name that has `_R3_`, `_I_`, or `_I1_` in it.
- *Barcode map*. Information about what barcode goes with what sample. A common gotcha in 16S data processing is that the barcode map might have barcodes that are reverse complements of what are in the samples.
- *Primer sequences*. The sequences of the primers used in the 16S amplification. They might also be the reverse complement of what's in the data.

If you download a dataset or get it from a collaborator, it might come in an
already-processed format. Depending on your purposes, it might be fine to use
that data, which will look similar to something we'll get a little further down
this pipeline. In general, however, it's very useful to ask for or search for
this entire list of things when you're starting to analyze a data set from
scratch.

## Overview of the processing pipeline

16S data analysis breaks down into a few steps:

### Phase 0 (pre-processing).

This is the practical, devoid-of-theory step in which you get (*a*) the data you have into (*b*) the format you need it in to (*c*) move it further down the pipeline. This usually means converting the raw data and metadata into a file format that your software knows how to handle, sifting out the barcode reads, that sort of thing.

### Phase I

These steps take the raw data and turn it into biologically relevant stuff.
There is some freedom about the order in which they can be done. Broadly, they
try to turn the sequencing data into something that is biologically meaningful.

- *Removing* (or "trimming") *primers*. The primers are a man-made thing. If there was a mismatch between the primer and the DNA of interest, you'll only see the primer. We therefore chop it off.
- *Quality filter* (or "trim") reads. For every nucleotide in every read, the
sequencer gives some indication of its assuredness that that base is the thing
it says it is. This assuredness is called *quality*: if a base has high quality,
you can be sure that that base was called correctly. If it has low quality, you should be
more skeptical. In general, reads tend to decrease in quality as they extend,
meaning that we get less sure that the sequence is correct the further away from
the primer we go. Some reads also have overall low quality.[^4] Quality
filtering removes sequences or parts of sequences that we think we cannot trust.

![Reads differ in overall quality and number of "decent" reads.](images/qual-dec.png)

[^4]: Annoyingly, it's my experience that the first reads in the raw data are substantially worse than most of the reads in the file. In the dataset I'm looking at, the first 3,000 or so reads (of 13.5 million total) have an average quality that is about half of what's typical for that dataset.

- *Merging* (or "overlapping" or "assembling" or "stitching") read pairs. When
doing paired-end sequencing, it's desirable for the two reads in the pair to
overlap in the middle. This produces a single full-length read whose quality in
the middle positions is hopefully greater than the quality of either of the two
reads that produced it. There's no such thing as "merging" for single-end
sequencing.
- *Demultiplexing* (or "splitting"). The man-made barcode sequences are replaced by the names of the samples the sequences came from.

![Merging aligns reads, makes a new sequence, and computes new quality scores. Adapted from the `usearch` manual.](images/merge-quality.png)

### Phase II

These steps compact the data and make it easier to work with when calling OTUs. They can happen simultaneously.

- *Dereplicating*. There are fewer *sequences* (strings of `ACGT`) than there are *reads*. This step identifies the set of unique sequences, which is usually much smaller than the number of reads.
- *Provenancing* (or "mapping" or "indexing"). How many reads of each sequence were in each sample? (Only I call it "provenancing"[^3]. I find all the other names I've heard confusing.)

[^3]: In archaeology, an artifact's _provenance_ is the place within the archaeological site where it was found.

### Phase III: OTU calling

This is a complex enough endeavor that I will break it out into a separate section.

### Phase IV: Fun & profit.

The part where you actually use your data! This part is outside the scope of this work.
I do, however, encourage you to use the same intellectual attitude that's promulgated
here: don't just use an analytical tool because it's popular or because someone else
used it. Look inside the sausage as best you can.

## Details of each step

### Removing primers

In an ideal world, this is straightforward: you find the piece of your
read that matches the forward primer, and you pop it off. Repeat for the
reverse read. In practice, there are two important considerations:

- *Where do you look for the primer?* Does the primer start at the very first
nucleotide of the read, or a little further in? You can put a lot of flexibility
in this step without a lot of negative effects, but it's good to know what's
going on in your data.
- *What does "match" mean?* How many mismatched nucleotides do you allow between the
read and your primer sequence before you consider the read "bad"? In practice,
it's common to only keep reads that have at most one error in the primer match.

### Merging

Merging is the most complex part of the pre-OTU-calling steps. Merging requires you to:

- *Find the "best" position for merging.* If you were sure all your amplicons are
exactly the same size, then this is trivial: just overlap them at the right length.
However, even in amplicon sequencing, there are
insertions and deletions in the 16S variable regions, so we can't be sure that
all merged reads will be the exactly the same length.
- *Decide if the "best" position is good enough.* If you have two reads that don't
overlap at all, should you even include it in the downstream analysis?[^5] How
good is good enough?

[^5]: If you had two paired-end reads that didn't overlap but you were somehow sure of the final amplicon size, then you could insert a bunch of `N`'s in between. This is an advanced and specialized topic.

- *Compute the quality of the nucleotides in the merged read using the qualities in
the original reads.* This requires some basic Bayesian statistics. It's not
super-hard, but it was hard enough to be the subject of (among others) a [2010
Alm Lab paper](http://dx.doi.org/10.1371/journal.pone.0011840) and a [2015
paper](http://dx.doi.org/10.1093/bioinformatics/btv401) from the maker of
`usearch`.

I think it's worth noting that `usearch`, which will come up later, is a very
popular tool for merging sequences.

### Quality filter

Why do you need to quality filter? Some of the reads that come off the
sequencer are bad. Sequences tend to vary in overall quality (some good, some bad)
and the number of bases they have that are good. Inherent in the Illumina technology is
a trend for sequences to decrease in quality as you move down the sequence.
The sequencer will give you a sort of quality report about your sequences' average
quality. It will give you a sense of whether your sequencing run as a whole was
good, and it will give you a sense of whether you got the sort of good-quality
length you were hoping for.

![images/quality.png](An read quality report delivered by the Illumina software.)

There are two common ways to quality filter:

- *Quality trimming* means truncating your reads at some nucleotide after which the sequence
is "bad". A common approach is to truncate everything after the first
nucleotides whose quality falls below some threshold.
- *Global quality filtering* means discarding an entire read if the average quality
of the read is too low. Maybe no individual nucleotide falls below your trim
threshold, but the general poor quality of the read means that you'd rather not
include it in analysis. This criterion is expressed equivalently as "average
quality" or "expected number of errors".[^flyv] When I work with 250 bp amplicons,
I like to throw out reads that have more than two expected errors.

[^flyv]: There's a nice paper by [Edgar & Flyvbjerg](http://dx.doi.org/10.1093/bioinformatics/btv401) (doi:10.1093/bioinformatics/btv401) that shows how to compute this.

It makes sense to merge then global quality filter or to quality trim then merge.
It does not make sense to merge then quality trim. I worked with paired-end reads,
so I do global quality filtering as my very last Phase I step.

Confusingly, "trimming" also refers to a different process when, if you're doing
unpaired amplicon sequencing, you pick a length, discard all reads shorter than
that, and truncate all the longer sequences at that length. (You do this for
reasons that might become clearer in the OTU calling section.)

### Demultiplexing

This step is similar to primer removal:

- *Which of the known barcodes is the best match for this barcode read?* That's a
pretty straightforward answer. (What if there's a tie, you say? Barcodes are
chosen with an error-correcting code so that a tie implies that you have at
least two errors in the read. Read on.)

- *Is the match with the known barcode good enough?* A common approach is to throw
away reads whose barcode read has more than one error.

### Dereplicating, denoising, and provenancing

Provenancing is simple: you just look through the list of unique sequences
(i.e., the dereplicated reads) and the list of all reads, counting up how many
times each sequence appears in each sample. Dereplication has one practical
question associated with it:

- *How many times does a sequence have to appear for me to believe it?*
In most data sets, there is a "long tail" of sequences: there are a
few abundant sequences and many rare sequences. I often use a dumb way to
decide which sequences are "real": I just drop the sequences that only appear once
in the entire data set.

My simple choice is just a hack that does some simple denoising and reduces the
size of the resulting data. More intelligent denoising uses a model to infer
which reads in the dereplicated set are
"real" and which ones are due to sequencing error. There is a
whole literature about "denoising" reads, so I will just mention
[*DADA*](http://dx.doi.org/10.1186/1471-2105-13-283), which
seems to be the best-performing algorithm available.[^dada]

[^dada]: In case you didn't get the pun, Dada is the name of an an art movement about, in part, creating irrational, chaotic art.

### Chimera removal (or "slaying")

As mentioned early on, PCR can produce chimeric sequences.[^chimera] Depending
on your choices about OTU calling, you may want to remove chimeras after
dereplicating. Chimera removal checks to see which of your dereplicated sequences
can be made by joining the first part of one sequence (the "head") with the last
part of another sequence (the "tail").

Chimera removal methods come in two main flavors: *reference-based* and *de novo*.
In reference-based methods, you look for the head and tail sequences in some
database. Popular databses include Greengenes, [SILVA](http://www.arb-silva.de/),
the Broad Institute's [ChimeraSlayer](http://microbiomeutil.sourceforge.net/)
or "Gold" database, and [RDP's "Gold"](https://sourceforge.net/projects/rdp-classifier/files/RDP_Classifier_TrainingData/)
database.

In *de novo* methods, you ask which of your sequences
have could be generated by combining other (typically more abundant) sequences
from that same dataset.
In the past, this was a computationally-expensive undertaking, but there are
ever-improving methods, notably, the [UPARSE](http://dx.doi.org/10.1038/nmeth.2604)
algorithm, which is the new `usearch`'s stardard way of simultaneously calling
*de novo* OTUs and doing *de novo* chimera detection.

[^chimera]: The Chimera was a monster in Greek mythology. It had the head of a lion and the tail of a snake. It was slain by the hero Bellerophon.
