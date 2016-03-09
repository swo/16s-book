# Data processing theory

Hooray, you have sequence data! Now what? I'll assume you did paired-end sequencing (but I'll make a note for those of you who didn't). Notably, all 454 sequencing is single-ended.

## Raw data and metadata

Before trying to process your dataset, be sure you have the following raw data[^3] and metadata:

-   *Forward reads*. For Illumina, this means a *fastq* file that might
    have a name like `130423Alm_D13-1939_1_sequence.fastq`. Giveaways
    that this is a forward read are something like `_1_` or `_R1_` in
    the filename. The first line of the file should also end with `/1`.
    For example, the first line of the file I have is
    `@MISEQ578:1:1101:15129:1752#CCGACA/1`.

-   *Reverse reads* (unless you did single-end sequencing). A fastq file
    with a name like the forward reads only with `_2_` or `_R2_` in it.
    The first line in the file should end with `/2`, indicating that
    it's the second read of a pair. Every entry in the reverse reads
    should match an entry in the forward reads. In most cases, the two
    pairs of a read appear in analogous places in the two files (i.e.,
    the forward read entry starting on line $x$ in the forward read file
    corresponds to the reverse read starting on line $x$ in the reverse
    reads file).

-   *Barcode* or *index* ****** *reads*. Depending on your Illumina
    version, this information might be in different places. In some
    datasets, it's in the file with the forward reads. In the above
    example line, the barcode read is `CCGACA` (between the `#` and the
    `/1`). In other datasets, you might find the index reads in a file
    with a name that has `_R3_`, `_I_`, or `_I1_` in it.

-   *Barcode map*. Information about what barcode goes with what sample.
    A common gotcha in 16S data processing is that the barcode map might
    have barcodes that are reverse complements of what are in
    the samples.

-   *Primer sequences*. The sequences of the primers used in the
    16S amplification. They might also be the reverse complement of
    what's in the data.

If you download a dataset or get it from a collaborator, it might come
in an already-processed format. Depending on your purposes, it might be
fine to use that data, which will look similar to something we'll get a
little further down this pipeline.

Overview of the processing pipeline
-----------------------------------

16S data analysis breaks down into a few steps:

-   **Phase 0 (pre-processing**). This is the practical,
    devoid-of-theory step in which you get (*a*) the data you have into
    (*b*) the format you need it in to (*c*) move it further down
    the pipeline. This usually means converting the raw data and
    metadata into a file format that your software knows how to handle,
    sifting out the barcode reads, that sort of thing.

-   **Phase I**. These steps take the raw data and turn it into
    biologically relevant stuff. There is some freedom about the order
    in which they can be done.

    -   *Removing* (or "trimming") *primers*. The primers are a
        man-made thing. If there was a mismatch between the primer and
        the DNA of interest, you'll only see the primer. We therefore
        chop it off.

    -   *Quality filter* (or "trim") reads. For every nucleotide in
        every read, the sequencer gives some indication of its
        assuredness that that base is the thing it says it is. This
        assuredness is called *quality*: if a base has high quality, you
        can be sure that it is that nucleotide. If it has low quality,
        you should be more skeptical. In general, reads tend to decrease
        in quality as they extend, meaning that we get less sure that
        the sequence is correct the further away from the primer we go.
        Some reads also have overall low quality.[^4] Quality filtering
        removes sequences or parts of sequences that we think we
        cannot trust.

    -   *Merging* (or "overlapping" or "assembling" or "stitching")
        read pairs. When doing paired-end sequencing, it's desirable for
        the two reads in the pair to overlap in the middle. This
        produces a single full-length read whose quality in the middle
        positions is hopefully greater than the quality of either of the
        two reads that produced it (). There's no such thing as
        "merging" for single-end sequencing.

        ![Merging reads involves aligning the two single-end reads and
        adjusting the quality scores. Q40 is a high quality score; Q2 is
        a low quality.\[fig:merge\]](fig/overlapper)

    -   *Demultiplexing* (or "splitting"). The man-made barcode
        sequences are replaced by the names of the samples the sequences
        came from.

-   **Phase II**. These steps compact the data and make it easier to
    work with when calling OTUs. They can happen simultaneously.

    -   *Dereplicating*. There are fewer *sequences* (strings of `ACGT`)
        than there are *reads*. This step identifies the set of unique
        sequences, which is usually much smaller than the number
        of reads.

    -   *Provenancing* (or "mapping" or "indexing"). How many reads of
        each sequence were in each sample? (Only I call it
        "provenancing". I find all the other names I've
        heard confusing.)

-   **Phase III: OTU calling**. This is a complex enough endeavor that I
    will break it out into a separate section.

-   **Phase IV: Fun & profit.** The part where you actually use your
    data! This part is outside the scope of this work.

Details of each step
--------------------

### Removing primers

In an ideal world, this is straightforward: you find the piece of your
read that matches the forward primer, and you pop it off. Repeat for the
reverse read. In practice, there are two important considerations:

-   Where do you look for the primer? Does the primer start at the very
    first nucleotide of the read, or a little further in? You can put a
    lot of flexibility in this step without a lot of negative effects,
    but it's good to know what's going on in your data.

-   What does "match" mean? How many mismatched nucleotides do you allow
    between the read and your primer sequence before you consider the
    read "bad"? In practice, it's common to only keep reads that have at
    most one error in the primer match.

### Quality filter

For some people, "trim" is synonymous with "quality filter", but
trimming is only one of two common ways to quality filter:

-   Trimming means truncating your reads at some nucleotide after which
    the sequence is "bad". A common approach is to truncate everything
    after the first nucleotides whose quality falls below
    some threshold.

-   Global quality filtering means discarding an entire read if the
    average quality of the read is too low. Maybe no individual
    nucleotide falls below your trim threshold, but the general poor
    quality of the read means that you'd rather not include it
    in analysis. This criterion is expressed equivalently as "average
    quality" or "expected number of errors". I like to throw out reads
    that have more than two expected errors.

Note that it makes sense to trim before you merge, but it doesn't make
sense to global quality filter before you merge. I work with paired-end
reads, so I do global quality filtering as my very last step in Phase I.

### Merging

Merging is the most complex part of the pre-OTU-calling steps. Merging
requires you to:

-   Find the "best" position for merging. Evern in amplicon sequencing,
    there are insertions and deletions in the 16S variable regions, so
    we can't be sure that all merged reads will be the exactly the
    same length.

-   Decide if the "best" position is good enough. If you have two reads
    that don't overlap at all, should you even include it in the
    downstream analysis?[^5] How good is good enough?

-   Compute the quality of the nucleotides in the merged read using the
    qualities in the original reads. This requires some basic
    Bayesian statistics. It's not super-hard, but it was hard enough to
    be the subject of a 2010 Alm Lab paper.

### Demultiplexing

This step is similar to primer removal:

-   Which of the known barcodes is the best match for this barcode read?
    That's a pretty straightforward answer. (What if there's a tie, you
    say? Barcodes are chosen with an error-correcting code so that a tie
    implies that you have at least two errors in the read. Read on.)

-   Is the match with the known barcode good enough? A common approach
    is to throw away reads whose barcode read has more than one error.

### Dereplicating and provenancing

Provenancing is simple: you just look through the list of unique
sequences (i.e., the dereplicated reads) and the list of all reads,
counting up how many times each sequence appears in each sample.
Dereplication has one practical question associated with it:

-   How many times does a sequence have to appear for me to believe it?
    There is a whole literature about "denoising" reads, essentially
    inferring which reads are the result of sequencing error and which
    ones are real sequences from rare bacteria. In most data sets, there
    is a "long tail" of sequences: there are a few abundant sequences
    and many rare sequences. It's common to simply drop sequences that
    appear only once in the data set. This is a hack that does some
    simple denoising and reduces the size of the resulting data.

### Chimera removal (or "slaying")

As mentioned early on, PCR can produce chimeric sequences. Depending on
your choices about OTU calling, you may want to remove chimeras after
dereplicating. Chimera removal methods come in two main flavors:
*reference-based* and *de novo*. In reference-based methods, you simply
check to see if any of your sequences are in an existing database of
known chimeras. Greengenes has one. In *de novo* methods, you ask which
of the sequences you have could be generated by combining other
(typically more abundant) sequences. In the past, this was a
computationally-expensive undertaking, but there are ever-improving
methods.
