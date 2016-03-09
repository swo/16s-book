# Foreword

## Where this document came from

I wrote an early form of this document as a teaching aid for a workshop on 16S data processing that I gave for my research group, the Alm Lab at MIT. I eventually put this document up for the larger world because it was starting to be shared in wider circles.

## What this document is for

My goal for this document is to help you understand the theory behind 16S data processing. I want you to be able to do the analysis that makes the most sense for you. I don't think it's wise to shove every dataset through the same pipeline. There are pipelines that make data analysis easy and simple. I'm going to show you how the sausage is made. It's ugly. The nice pipelines also use an ugly, complicated process somewhere inside; they just don't advertise that ugliness. I want to empower you to be able to critique and doubt other people's methods. That's part of how science advances!

## Who this document is for

This document should be a fun read for advanced undergraduates, graduate students, and postdocs who are interested in getting down and dirty with 16S data. If you know too much, I expect this document will annoy you, because you will recognize its shortcomings.

## What this document is not

This document is not perfect. It is full of my own igorance, ideas, and opinions. Take it with a grain of salt. If you find errors, blame me and not my adviser or the other members of my lab. And do point them out to me!

This document is also not intended to be a literature review. 16S data processing is an enormous field, and here I do less than scratch the surface of that field. Some specific methods are included and they show my biases toward my own lab's work.


# Where 16S data comes from

By "16S data" I mean amplicon sequencing of some section of the bacterial 16S gene. A lot of what I discuss in this document may also apply to other types of taxonomic marker sequences like the eukaryotic 18S or the fungal ITS.

## The 16S gene

All bacteria (and archaea) have at least one copy of the 16S gene in their genome.[^kembel] The gene has some sections that are *conserved*, meaning that they are very similar across all bacteria, and some sections that are *variable*. The idea behind 16S sequencing is that the variable regions are not under strong evolutionary pressure, so random mutations accumulate there. Closely-related bacteria will have more similar variable regions than distantly-related bacteria.

![**The 16S gene has variable regions.** These are nucleotide positions in the aligned 94% OTUs in [Greengenes](http://dx.doi.org/10.1128/AEM.03006-05). "Variability" (which I made up for the purposes of this figure) at a position is {$$}1-{/$$} the fraction of OTUs that had the most common nucleotide at that position. For example, if all OTUs had `A` at a position, the "variability" is 0. If half of the OTUs had `A` at that position, the "variability" is {$$}0.5{/$$}. The actual plot is very spiky, so I smoothed over 50 nucleotide windows. This shows you that there are subsequences of the gene that are more variable than others.](fig/variab.pdf)

[^kembel]: It’s not unusual for bacteria to have multiple copies of the 16S gene, and those copies might not be identical to one another. Some people are concerned by the effect this could have on 16S data (e.g., [Kembel *et al*.](http://dx.doi.org/10.1371/journal.pcbi.1002743)

## Amplifying the gene

After a sample is taken, the cells in the sample are lysed, typically using some combination of chemical membrane-dissolving and physical membrane-busting. The DNA in the sample is *extracted*, meaning that all the protein, lipids, and other stuff in the sample is thrown away. From this pile of DNA spaghetti, we aim to collect information about the bacteria that were in the original sample.

In theory, sequencing all the DNA in the sample at some depth will give as much information as just sequencing the 16S gene alone. In practice, this approach is more expensive and, in terms of the bioinformatics, much more complex. You’ll need to go elsewhere to learn about the theory and practice of metagenomic sequencing. (Confusingly, the adjective "metagenomic" is also applied to 16S amplicon sequencing of bacterial communities, since these samples have more than one genome.)

In the amplicon sequencing approach, PCR is used to amplify a section of the 16S gene. The size of the sequenced section is limited by the length of reads produced by high-throughput sequencing. The sections of the 16S gene that are amplified are named according to what variable regions of the gene are covered. There are nine variable regions, but there isn't an exact definition of where they begin and end.

- *V1-V2* (the first two variable regions). This section of the gene provides better taxonomic resolution for some bacteria associated with the skin microbiome, so skin studies sometimes sequence V1-V2.
- *V4* (variable region 4). This section of the gene provides good taxonomic resolution for bacteria associated with the gut microbiome, so it is the most popular section. I get the sense that V4 is also the best "catch-all" region, but I don’t know of a good reference to back up that sense.
- *V5-V6*. I've only seen this section in projects that aim to be particularly complete (e.g., the [Human Microbiome Project](http://hmpdacc.org/)).

PCR reactions on these regions have primers that match the constant regions around the variable regions. Papers should always mention which primers they used, and they usually also mention the amplified region. The primers have names like 8F (meaning, a forward primer starting at nucleotide 8 in the gene) and 1492R (meaning, a reverse primer starting at nucleotide 1492).

Compared to the metagenomic approach, the amplicon-based approach has some advantages. First, as mentioned above, it is cheaper. Second, because only bacteria have the 16S gene, all your sequencing reads go toward sequencing bacteria. In contrast, the majority of metagenomic reads from a swab of human skin will be reads of human DNA. Third, your reads come "pre-aligned". (They’re not *actually* "aligned" in the bioinformatic sense, but it’s a good analogy.) This means that you know where each read came from: the 16S gene, from this nucleotide position to that nucleotide position. Every read therefore provides, roughly speaking, an equal amount of information about the composition of the sample's bacterial community.

## The amplified DNA is not exactly like the original DNA

The process of extracting DNA from bacterial cells and then amplifying a 16S region introduces certain biases into the resulting sequence data. These effects mean its better to look for changes in bacterial community structure rather than assert that such-and-such a species is more abundant than other-and-such a species. It also means that large effects, like variations over orders of magnitude, are to be trusted far more than smaller changes. These grains of salt to be kepts in mind are
*extraction bias*, *PCR bias*, and PCR *chimeras*.

The strongest effect is from extraction bias: different cells respond differently to different extraction protocols. Splitting a sample and using different extraction protocols on the different parts will produce markeldy different results. The original HMP effort suffered a big surprise during early data analysis: no matter how you slice it, the biggest signal in the HMP data is “center”. Each sample in HMP was processed at one of the three sequencing centers, each of which used their own extraction protocol. The thing that makes two samples most different in the HMP data is if they were sequenced at different centers.

*PCR bias* is less important than extraction bias. I don’t think PCR bias is a huge problem, but it’s good to have heard about it. First, even though the PCR primers bind a “constant” region, some bacteria in the sample will have different nucleotides there, meaning that the PCR primers will bind with different affinities to the DNA of different bacteria. This effect decreases the number of reads from bacteria whose constant regions don’t perfectly match the primer.[^2] Second, it’s known that PCR has different efficiencies for different types of sequences, meaning that some 16S variable regions will amplify better than others. Third, statistical fluctuations can occur, especially in low-diversity samples. This means that a sequence that, by chance, gets lots of amplification in early PCR cycles could dominate the sample in late PCR cycles.

In general, PCR bias is not as bad when there is more DNA and (relatedly) when the PCR is run for fewer cycles.

In the lab we’ve run experiments to quantify PCR bias: we synthesize some DNA that looks like bacterial 16S genes, mix them in known proportions, do the amplification and sequencing, and compare the sequencing data to the known proportions. The errors are somewhere in the neighborhood of 1% to 10%. Not enough to make you think that 16S data is all garbage, but high enough to make you doubt small changes in composition.

PCR also creates a weird artifact called *chimeras*. When using PCR to amplify two DNA sequences *a* and *b*, you’ll get a lot of *a*, a lot of *b*, and some sequences that have an *a* head and *b* tail (or vice versa). There are some things about your PCR protocol that you can adjust to decrease the prevalence of chimeras, but they are beyond the scope of this document.

There are also biases that arise from *any* DNA-based experiment, like the biases that result from the method of collection or storage. Some people run mini-studies to ask about the effects of storage at different temperatures for different times, the effect of the buffer used, etc. Regardless of what method of collection and storage is used, using the same method for every sample in a study is a good way to reduce biases.

## Multiplexing helps evaluate contamination (or other weirdness)

Next-generation sequencing wasn’t that helpful to microbial ecology until *sample multiplexing* (or “barcoding”) was worked out. The first paper to use multiplexed bacterial samples came out in 2008. Before multiplexing, every sample had to be run on its own sequencing lane. This was expensive and bioinformatically annoying, since, especially in those dark ages of sequencing, weird stuff would frequently happen during sequencing runs, and it was hard to distinguish a bad lane from a
weird sample.

In contrast, multiplexing adds a barcode or “tag” to the 16S amplicon. Each barcode corresponds to a sample, and all amplicons in that sample get that barcode. It’s now common to multiplex 96 (or 384) samples and sequence them in one lane. Aside from making the sequencing 100-fold cheaper, multiplexing means that it’s easier to include some controls in each lane:

- *Negative controls*: Usually just vehicle with no DNA, as a way to check for contamination from reagents or poor sample preparation.
- *Positive controls*: Mock communities of known composition, which can be used to check that the sequencing was not “weird”. If you have a lot of samples from the same project and you need to run them in more than one lane, you can use the positive controls as an internal check that sequencing proceeded similarly across lanes.

The bioinformatic cost of multiplexing is that the reads must be *demultiplexed* in the analysis stage. This is not very difficult.

## Sequencing

A little more work has to be done before putting the sample in the sequencer. These steps will depend on the sequencing platform. Here I’ll talk about Illumina because it’s popular and I have experience with it.

Samples to be sequenced on an Illumina machine need to have Illumina-specific *adapters* added in another PCR. These adapters allow the DNA amplicons to bind the flowcell where they are sequenced. It is sometimes also desirable to have a *diversity region* added between the adapter and the 16S primer. The Illumina sequencers expect to see a diversity of nucleotides at every read position. In amplicon sequencing, almost all the reads are the same through the primer region, which freaks out the sequencer. A diversity region is just some random nucleotides that helps the sequencer do its job. In our lab we use `YRYR`, where `Y` means `T` or `C` and `R` means `G` or `A`.

All of these pieces --the 16S region you’re interested in, forward and reverse primers, barcodes, diversity region, and Illumina adapters-- are all made into a single *PCR construct*, which is a single piece of DNA. The sequencer reads the nucleotides in the construct and uses its knowledge about the arrangement of the construct to infer which nucleotides are the region of interest and which are the barcode.

![**An example PCR construct.** The parts labeled on top are interesting only for technical reasons. The parts on the bottom have information that’s useful for someone analyzing sequence data.](fig/pcr-construct.pdf)

# Data processing theory

Hooray, you have sequence data! Now what? I’ll assume you did paired-end sequencing (but I’ll make a note for those of you who didn’t). Notably, all 454 sequencing is single-ended.

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
    it’s the second read of a pair. Every entry in the reverse reads
    should match an entry in the forward reads. In most cases, the two
    pairs of a read appear in analogous places in the two files (i.e.,
    the forward read entry starting on line $x$ in the forward read file
    corresponds to the reverse read starting on line $x$ in the reverse
    reads file).

-   *Barcode* or *index* ****** *reads*. Depending on your Illumina
    version, this information might be in different places. In some
    datasets, it’s in the file with the forward reads. In the above
    example line, the barcode read is `CCGACA` (between the `#` and the
    `/1`). In other datasets, you might find the index reads in a file
    with a name that has `_R3_`, `_I_`, or `_I1_` in it.

-   *Barcode map*. Information about what barcode goes with what sample.
    A common gotcha in 16S data processing is that the barcode map might
    have barcodes that are reverse complements of what are in
    the samples.

-   *Primer sequences*. The sequences of the primers used in the
    16S amplification. They might also be the reverse complement of
    what’s in the data.

If you download a dataset or get it from a collaborator, it might come
in an already-processed format. Depending on your purposes, it might be
fine to use that data, which will look similar to something we’ll get a
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

    -   *Removing* (or “trimming”) *primers*. The primers are a
        man-made thing. If there was a mismatch between the primer and
        the DNA of interest, you’ll only see the primer. We therefore
        chop it off.

    -   *Quality filter* (or “trim”) reads. For every nucleotide in
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

    -   *Merging* (or “overlapping” or “assembling” or “stitching”)
        read pairs. When doing paired-end sequencing, it’s desirable for
        the two reads in the pair to overlap in the middle. This
        produces a single full-length read whose quality in the middle
        positions is hopefully greater than the quality of either of the
        two reads that produced it (). There’s no such thing as
        “merging” for single-end sequencing.

        ![Merging reads involves aligning the two single-end reads and
        adjusting the quality scores. Q40 is a high quality score; Q2 is
        a low quality.\[fig:merge\]](fig/overlapper)

    -   *Demultiplexing* (or “splitting”). The man-made barcode
        sequences are replaced by the names of the samples the sequences
        came from.

-   **Phase II**. These steps compact the data and make it easier to
    work with when calling OTUs. They can happen simultaneously.

    -   *Dereplicating*. There are fewer *sequences* (strings of `ACGT`)
        than there are *reads*. This step identifies the set of unique
        sequences, which is usually much smaller than the number
        of reads.

    -   *Provenancing* (or “mapping” or “indexing”). How many reads of
        each sequence were in each sample? (Only I call it
        “provenancing”. I find all the other names I’ve
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
    but it’s good to know what’s going on in your data.

-   What does “match” mean? How many mismatched nucleotides do you allow
    between the read and your primer sequence before you consider the
    read “bad”? In practice, it’s common to only keep reads that have at
    most one error in the primer match.

### Quality filter

For some people, “trim” is synonymous with “quality filter”, but
trimming is only one of two common ways to quality filter:

-   Trimming means truncating your reads at some nucleotide after which
    the sequence is “bad”. A common approach is to truncate everything
    after the first nucleotides whose quality falls below
    some threshold.

-   Global quality filtering means discarding an entire read if the
    average quality of the read is too low. Maybe no individual
    nucleotide falls below your trim threshold, but the general poor
    quality of the read means that you’d rather not include it
    in analysis. This criterion is expressed equivalently as “average
    quality” or “expected number of errors”. I like to throw out reads
    that have more than two expected errors.

Note that it makes sense to trim before you merge, but it doesn’t make
sense to global quality filter before you merge. I work with paired-end
reads, so I do global quality filtering as my very last step in Phase I.

### Merging

Merging is the most complex part of the pre-OTU-calling steps. Merging
requires you to:

-   Find the “best” position for merging. Evern in amplicon sequencing,
    there are insertions and deletions in the 16S variable regions, so
    we can’t be sure that all merged reads will be the exactly the
    same length.

-   Decide if the “best” position is good enough. If you have two reads
    that don’t overlap at all, should you even include it in the
    downstream analysis?[^5] How good is good enough?

-   Compute the quality of the nucleotides in the merged read using the
    qualities in the original reads. This requires some basic
    Bayesian statistics. It’s not super-hard, but it was hard enough to
    be the subject of a 2010 Alm Lab paper.

### Demultiplexing

This step is similar to primer removal:

-   Which of the known barcodes is the best match for this barcode read?
    That’s a pretty straightforward answer. (What if there’s a tie, you
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
    There is a whole literature about “denoising” reads, essentially
    inferring which reads are the result of sequencing error and which
    ones are real sequences from rare bacteria. In most data sets, there
    is a “long tail” of sequences: there are a few abundant sequences
    and many rare sequences. It’s common to simply drop sequences that
    appear only once in the data set. This is a hack that does some
    simple denoising and reduces the size of the resulting data.

### Chimera removal (or “slaying”)

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

OTU-calling theory
==================

*Operational taxonomic units* (OTUs) are often the fundamental unit used
in 16S data analysis. In most data processing pipelines, OTUs and their
abundances in the samples are the output.

OTU-calling methods are (to me) surprisingly diverse, and the choice of
method can have a huge impact on the the results of your analysis. Any
OTU-based information, plot, or analysis must be interpreted in the
context of how those OTUs were called.

An abridged history of the OTU
------------------------------

This is my short and probably incorrect history of the OTU concept.

In the 1980s, Carl Woese showed that the 16S gene could be used as a
molecular clock. Using 16S data, he re-drew this tree of life, breaking
up the older Monera into Bacteria and Archaea, showing that Eukaryotes
and Archaea are closer cousins than are Archaea and Bacteria. The 16S
gene was therefore a promising practical candidate for distinguishing
bacterial *species*.

The species concept is easy for people studying sexual macroorganisms:
two living things of opposite sex are in the same species if they can
produce fertile offspring together. Bacteria don’t have sex, but they do
perform homologous recombination. Homologous recombination requires some
sequence similarity, so it came about that the definition of a bacterial
species was all those strains whose isolated DNA was 70%
DNA-DNA-hybridization similar.

In the 1990s, people sequenced the 16S genes of the strains gropued into
species by the hybridization assay. It emerged as a rule of thumb that
two bacteria were the same species if their 16S genes had 97% nucleotide
identity. In the next-generation era, this rule of thumb developed a
second-hand version: two bacteria are in the same species if their 16S
amplicons (however they got amplified) at least 97% similar.

Because of this history, a lot of discussion around OTUs involves
finding these 97% clusters, and some people will take “OTU” to mean “97%
clusters”. I try here to be a little more open-minded: I say an OTU is
whatever thing comes out of your method of combining unique 16S
sequences into some taxonomically-motivated unit that you think is
meaningful for your problem.

Why call OTUs?
--------------

Creating OTUs is some combination of denoising and data reduction.
Historically people called OTUs because for a few reasons.

Some reasons were practical. For some people, the data reduction was
really important. Dereplication can give you hundreds of thousands of
unique sequences, which can feel overwhelming. In earlier times, this
may have been computationally overwhelming. You might also think that
the denoising aspect of some OTU calling improves the quality of your
data.

Some reasons are philosophical or analytical. If you want to study
bacterial species and were a firm believer in the idea that a 97%
cluster is the best approximation of a species, then you’d want to
organize your data into those approximate-species and go from there.
More generally, you’ll want to organize your sequences into some
operational unit (i.e., OTU) that works well with the kind of analysis
you want to do. If you’re interested in broad changes in community
composition, you might want to call OTUs that are your best
approximations of phyla. If you’re interested in what individual
organisms are doing, you’ll probably want to do very little (if any)
grouping of sequences into OTUs, since the unique sequences are, in a
sense, the best information you have about those organisms.

Regardless of how you call OTUs, I think you should call them in a way
that doesn’t throw away information that could be useful or interesting.
Only throw away information that you are sure you won’t find interesting
for *any* downstream analysis. You might be able to tell that I think
that OTUs are often called too liberally early on. Having these reduced
chunks of information can make it easier to think about your data, but
beware: you want those chunks to be meaningful and the best information
you have to answer the questions you want to answer.

OTU calling is not the same as lineage assignment
-------------------------------------------------

*Calling* OTUs means assigning your unique 16S sequences to OTUs. Each
OTU has a sequence that may or may not be the sequence of one of its
members. If an OTU’s sequence is the same as one of its members, that
member is called the *representative sequence*.

Often the OTU sequence itself is not very interesting. We’d rather know
“what” that sequence is. A common way to get this information is to
assign *lineages* (or “taxonomies”) to each OTU. A lineage is usually an
assignment of that sequence to the taxonomic *ranks:* kingdom (or
“domain”), phylum, class, order, family, genus, and species. (Note that
weird stuff can happen here: there are other ranks like subclass, and
sometimes a sequence could, say, get assigned to a genus but not a
class.)

Confusingly, in some cases OTUs are in fact called using lineage
assigments. It’s useful to keep these two concepts separate. For
example, it’s common to call OTUs in some way, then assign lineages to
OTUs, then do a second round of OTU calling in which you merge OTUs that
have the same lineage. Now the OTUs are labelled by the lineages. This
is how the ubiquitous taxa plots are made.

Common and uncommon OTU-calling methods
---------------------------------------

This is a survey of OTU-calling methods that are out there in the
literature. This list is not exhaustive. The methods are listed are in
the order I thought was easiest to explain.

### Dereplication

It may sound a little crazy, but simple dereplication is a kind of OTU
calling: every unique sequence is its own OTU. Sometimes this approach
is called “100% identity OTUs” to emphasize that all sequences in an OTU
are 100% similar, that is, that there is only one sequence in each OTU.

The advantage of dereplication is that it’s quick and conceptually
straightforward. You need not wrangle over whether the OTU calling
method has introduced any weird bias into your data since, roughly
speaking, the OTUs are just your data.

### *De novo* clustering

As the name suggests, *de novo* clustering means making your own OTUs
from scratch. There is an enormous diversity of *de novo* clustering
methods. An important one to know is *uclust*, which is implemented in
the software program `usearch`. Uclust may be the most popular *de novo*
clustering algorithm. It is popular because it’s relatively fast and,
more importantly, it’s part of the QIIME software pipeline.

In short, these algorithms try to identify a set of OTUs that are at
some distance from one another. (As you might guess, 97% OTUs are
popular.) In some cases, the OTU’s representative sequence will be the
sequence of its most abundant member; in other cases, the OTU’s
representative sequence is some mish-mash of its member sequences.

*De novo* clustering suffers from some insidious and very serious
disadvantages. First, *de novo* methods are more computationally
expensive than other methods. Second, it is becoming increasingly clear
that many methods produce *de novo* OTUs that are not *stable*, meaning
that small changes in the sequence data you feed into the algorithm can
lead to large changes in the number of OTUs, the OTUs’ representative
sequences, and the assignment of reads to OTUs. Third, it is difficult
to incorporate new data into a dataset that has been processed into *de
novo* OTUs (it usually requires calling OTUs all over again). It’s also
difficult to compare *de novo* OTUs across datasets (you and I might
have lots of the same sequences but our OTUs might differ).

The principle advantage of *de novo* clustering is that it won’t throw
out abundant sequences from your data. Why would that happen? Read on!

### Reference-based methods

In reference-based OTU calling, the OTUs are specified ahead of time.
Usually these OTUs are in a database like Greengenes, which was made by
calling *de novo* OTUs on some large set of data. Greengenes is such a
popular database that sometimes people use “OTU” to mean “the 97% OTUs
in Greengenes”.

The principle advantages of reference-based calling are:

-   *Stability*. Similar inputs should produce similar outputs, since
    you’re just comparing to a fixed reference.

-   *Comparability*. If you and I called our OTUs using the same
    reference, it’s easy for us to check if we have similar sequences in
    our datasets. We can even combine our datasets in a snap.

-   *Computational cheapness*. Unlike *de novo* OTU calling,
    reference-based methods only need to hold one sequence in memory at
    a time. This makes them cheap (in terms of memory) and
    embarrassingly parallelizable (which is a real
    computer-science phrase).

-   *Chimeras need not be slain*. If you’re only keeping sequences that
    align to some database, which has hopefully been pre-screened for
    chimeras, then you don’t need to worry about them yourself.

The major weakness of reference-based methods can be dastardly and
insidious: if a sequence in your dataset doesn’t match a sequence in the
database, what do you do? Frighteningly, many methods just throw it out
without telling you. If you work in the human gut microbiome, this might
not bother you, since the gut is the best-studied ecosystem and
databases like Greengenes have heaps of gut data baked into them. If you
work in environmental microbiology or even in mice, however, many of
your sequences might not hit Greengenes.

Reference-based methods also suffer a converse problem: what if your
sequence is an equally good match to more than one database entry? This
can happen in amplicon sequencing: the Greengenes OTUs are the entire
16S gene, but you only have a little chunk of it. The Greengenes OTUs
are (say) 97% similar (i.e., 3% dissimilar) across the *entire gene*,
but they might be identical over the stretch that aligns to your little
chunk. Usearch, a popular algorithm for matching sequences to a database
(and QIIME’s tool for reference-based OTU calling), assigns reads
heuristically (in a sense, randomly). Two very similar sequences in your
dataset might get assigned to Greengenes OTUs that have different
taxonomies.

### Open-reference calling

Just throwing out non-matching sequences is *closed-reference* calling.
If you’re interested in those non-matching sequences, you could *de
novo* cluster them separately so that your OTUs are a mix of
reference-based and *de novo*. This is *open-reference* calling.

### Lineage-based assignments

Reference OTUs tend to have unsatisfying names. For example, the
Greengenes OTUs are labeled with numbers. It’s common (but not
necessarily good) practice to do a second round of OTU calling: the new
OTUs are made by combining the old OTUs that have the same lineage.

How does this work? Greengenes associates a taxonomy with each of its
OTUs. This is relatively easy for sequences that came from isolates: if
that sequence belongs to some OTU, give that OTU the classification you
would have given the isolate. It gets more tricky for OTUs that aren’t
just taken from isolates: it requires some sort of phylogenetic
inference. This means that you construct a tree of all your sequences,
figure out where the taxonomic clades are, and assign taxonomies to OTUs
based on what you found.

Someone at Greengenes has done all this hard work, but I want to make it
clear that this is not a foolproof process. All lineage assignments
should be treated with a healthy skepticism.

The most popular alternative to Greengenes for lineage assignments is
the Ribosomal Database Project (RDP) Naive Bayesian Classifier. Rather
than comparing a sequence to existing OTUs, the RDP classifier breaks up
the sequence into $k$-mers and compares the $k$-mer content of that
sequence to a big database that relates $k$-mer content with known
taxonomies. The practical advantage to this is that RDP gives
*confidences* to each level of the taxonomic assignment. For example, a
sequence might definitely be from some phylum (99%), but it might be
difficult to specify its class (80%) and nearly impossible to identify
its order (30%). In contrast, using the Greengenes approach, the same
sequence might happen to hit an OTU that is known all the way down to
the genus, and you would mistakenly think that your sequence had a lot
of taxonomic information in it.

### Distribution-based methods

All the algorithms mentioned only look at the list of unique sequences;
they don’t take any notice of how those sequences are distributed among
the samples. Some Alm Lab work has shown that you get more accurate OTUs
(i.e., OTUs that better reflect the composition of a known, mock
community) if you take the sequence provenances into account. If an
abundant sequence and a sequence-similar, rare sequence are distributed
the same way across samples, the rare sequence is probably sequencing
error and should be put in the same OTU with the abundant one.
Conversely, if two very similar sequence are never found together, they
probably represent ecologically-distinguishable bacteria, so they should
be kept in separate OTUs. This approach is confusingly called
*distribution-based* OTU calling or, less confusingly,
*ecologically-based* OTU calling. It’s not very popular beyond the Alm
Lab, but it’s a good way to call OTUs.

![Distribution-based OTU calling separates sequence-similar reads if
they are distributed differently across samples.](fig/zam9991048100001)

Practice
========

As you can see, there are a lot of in’s, out’s, and what-have-you’s
(IOWHYs) to processing 16S data. Rather than giving you the fish of some
monolithic pipeline, I’d rather try to teach you as much about fish as
you’ll find useful. There are plenty of websites that can give you fish
but not many that can introduce you to the IOWHYs.

In the rest of this document, I’ll assume you’re in a Unix/Linux/Mac
world. If you’re on Windows, you’ll essentially need to get to the Unix
world with a tool like Cygwin. I didn’t make up those rules, but that’s
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

1.  The *header* line (or “at” line). It must begin with the
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
    purine (A or G). `N` means “no idea, any base possible”.

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
    `!#$%&’()*+,-./0123456789:;<=>?@ABCDEFGHI`. `I` means that there is
    a $10^{-4.1}$ probability that this base is wrong (i.e., a 99.99%
    chance that it is correct). `H` means that there is a $10^{-4.0}$
    chance; `G` means $10^{-3.9}$, and so on down to ``. The exclamation
    point is special: it means a quality of zero, i.e., that the
    sequencer has no idea what that base is.

Here’s an example fastq entry. The sequence and quality lines are too
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
you’ll move to a fasta format when you’ve decided you aren’t going to
look at the quality data again, typically after quality filtering.

Here’s an example fasta entry in the traditional format (i.e., each line
no more than 80 characters, with the sequence spread over multiple
lines).

\[t\]<span>1</span>`>seq1;size=1409414;`

`TACGGAGGATCCGAGCGTTATCCGGATTTATTGGGTTTAAAGGGAGCGTAGGCGGGTTGT TAAGTCAGTTGTGAAAGTTTGCGGCTCAACCGTAAAATTGCAGTTGATACTGGCATCCTT GAGTACAGTAGAGGTAGGCGGAATTCGTGGTGTAGCGGTGAAATGCTTAGATATCACGAA GAACTCCGATTGCGAAGGCAGCCTGCTGGACTGTAACTGACGCTGATGCTCGAAAGTGTG`

`GGTATCAAACAGG`

### Other formats

I’ve been talking about Illumina, but the other important data type
comes from 454 sequencing. Raw 454 data comes in *sff* format. Unlike
fastq files, sff files are not human-readable. Luckily, you can convert
sff files to fastq files with only a minor loss of information.
Unluckily, 454 sequence data has its own in’s and out’s that are beyond
the scope of this document. Caveat sequentor.[^7]

Tools
-----

Everything in this document up to this point will help you be critical
of an analysis pipeline. This is true whether you use an existing
pipeline, work with someone who has a pipeline, or make your own
pipeline. The more you want to be involved in looking at and working
with your own data, the more computer skills you’ll need. You’ll also
need more of your own skills if you want to do more creative analysis or
be more sure of exactly what’s being done with your data.

### Existing tools

The great and mighty QIIME dominates the 16S data processing landscape.
I won’t say you should or shouldn’t use QIIME, but I will say that,
regardless of which tool you’re using, you should know *what* it’s
doing. If you’re happy to trust the QIIME maintainers to have made a
sensible tool, then go download that and start reading their
documentation. If you’re feeling more inquisitive, read on.

### Usearch

The great and mighty `usearch` underlies a lot of 16S data processing.
QIIME is built on the back of `usearch`. `usearch` is a single program
that has an ever-growing number of functionalities (including, the
algorithms usearch and uclust). The nice thing about `usearch` is that
it’s built by a guy who’s very concerned about making a fast, optimized
tool. The potentially nice thing about usearch is that it’s pretty
low-level: if you want to do some medium-lifting (like primer removal
and demultiplexing) but not heavy-lifting (like merging, quality
filtering, clustering, or sequence alignment), then `usearch` is for
you. The potentially bad thing about `usearch` is that it’s made by a
single guy and is closed source. He describes his methods, but no one
can check the code to make sure it does what he says it does.

`usearch` also has a funny caveat: newer versions come in two flavors,
free and wildly expensive. This means that mere mortals (i.e.,
non-Broadies) must be content to use the free version, which will only
process 2 Gb of data at a time. If you need to call OTUs *de novo* from
an enormous data set, then you’re sunk; if you merely want to merge,
quality filter, or do alignments, then it’s merely annoying. QIIME comes
with an older version of `usearch` that doesn’t have as many
capabilities but which doesn’t have the memory restriction.

### The eyes in your head

The best tool in your belt is a curious attitude. Be critical of your
data at every step in the pipeline. Does it look the way you expect? How
can you check? More often than not it’s wise to *look* at your data, and
look at it a lot, before moving on to the next step. It will also save
you some headaches later on by knowing what happened in the middle.

You spent a lot of time and energy collected the samples and making the
sequencing libraries, so you shouldn’t be flippant about processing your
data.

### The sweat of your brow

The second best tool is some computational skills. This means
familiarity with the basic tools of the Unix terminal (`cat`, `cd`,
`cp`, `ls`, `mkdir`, `mv`, `rm`, `head`, `less`, `sed` or `awk`, `wc`,
and `grep`) and the ability to use some programming language. Rather
than say what programming language is best, I’ll share some criteria to
help you decide what language is best:

-   *Support*. You’ll have a better time using a language that has good
    documentation, a large global community of users (who produce
    informal documentation in places like StackOverflow), and a local
    community of users, i.e., the person down the hall who can help you
    figure out what that syntax error means.

-   *Bioinformatics packages.* It’s nice to not re-invent the wheel.
    Some programming languages have mature, extensive
    bioinformatics toolkits.

-   *Appropriateness for your purpose*. Compiled programming languages
    run fast but are slow to develop; scripting languages run slow but
    are fast to develop. If you’re going to be crunching huge datasets
    that will take days to process, think about a compiled language
    designed for parallelization. If you’re just working on a few small
    datasets on your own computer, think about a scripting language
    that’s easier to use.

My language of choice for 16S data processing is Python. It’s a popular
language with great documentation. The people around me use it. It has a
good bioinformatics package (biopython). It’s relatively slow but I
don’t care because I spend much more time programming that I do actually
running data.


[^2]: It may be that there are a lot of interesting bugs whose 16S
    sequences are so divergent that they don’t match the typical primers
    (cf. doi:10.1038/nature14486).

[^3]: In what follows, I’ll talk about “raw data”, by which I mean data
    that you would get from the sequencing center. There is actually a
    more raw kind of data that comes right out of the sequencing machine
    that gets processed right away. On the Illumina platform, this data
    is CASAVA. Different version of CASAVA produce slightly different
    output, and every sequencer might have a different version of
    CASAVA, so be prepared for slight variations in the format of your
    raw data.

[^4]: Annoyingly, it’s my experience that the first reads in the raw
    data are substantially worse than most of the reads in the file. In
    the dataset I’m looking at, the first 3,000 or so reads (of 13.5
    million total) have an average quality that is about half of what’s
    typical for that dataset.

[^5]: If you had two paired-end reads that didn’t overlap but you were
    somehow sure of the final amplicon size, then you could insert a
    bunch of `N`’s in between. This is an advanced and specialized
    topic.

[^6]: Confusingly, the definition of a “line” on Windows is different
    from Unix/Linux/Mac. If you ever pass data between these two
    computer systems, make sure that have adjusted the line endings
    using `dos2unix`.

[^7]: That’s a joke for Latin scholars. It’s meant to mean “let the one
    processing the data beware”.
