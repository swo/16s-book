# 16S data processing

As the microbiome field has matured, there are ever-better tools and pipelines
for processing 16S data. These resources can save you time and can enhance
reproducibility, but they are no substitute for a deep understanding of the
underlying processes. This chapter steps through the files and algorithms used
in the more mundane steps of 16S processing.

## Phase I: Preprocessing

Before talking about how to preprocess the data, it's important to have a
handle on what exactly we're talking about when we say "the data".

### File formats

The two important file formats for 16S data are *fastq* and
*fasta*.[^fast] Fastq is an Illumina-specific raw data format, while fasta is the
industry-standard way to display processed sequence data.

[^fast]: Technically, these formats should be written FASTQ and FASTA, but I find this cumbersome, so I write them as if they were not acronyms. Fastq is pronounced "fast-Q". Fasta is supposed to be pronounced as "fast-A", but I hear "*fast*-uh" just as often.

#### Fastq format

Fastq files usually have the extension `.fastq` or `.fq`. Fastq files
are human-readable. They are made up of *entries* that each correspond
to a single read. Every entry is four lines.[^line] A well-formed fastq
file has a number of lines that is a multiple of four.
The lines in the entry
are:

[^line]: Confusingly, the definition of a "line" on Windows is different from Unix/Linux/Mac. If you pass data between these two computer systems, you may need to adjust the line endings using a tool like `dos2unix` or `tr`.

1. The *header* line
2. The *sequence* line
3. The *plus* line
4. The *quality* line

The header line gives an identifier for the read. The line must begin with the
character `@`. The format of the rest of the line depends on the Illumina
software version, but in general it gives information about the read: the name
of the instrument it was sequenced on, the flowcell lane, the position of the
read on the cell, and whether it is a forward or reverse read. In some version
of Illumina, the barcode read is in the read's header.

Like the name suggests, the sequence line is a series of letters encoding the
sequencing data, one character per nucleotide. Note that the letter might not
all be `ACGT`. Other letters are allowed to say that it might be any of a group
of bases. For example, `R` means purine (`A` or `G`). `N` means "no idea, any
base possible".[^iupac]

[^iupac]: These other options are the IUPAC nucleotide abbreviations. There is
  a one-letter code for every possible combination of the four nucleotides.

I call line 3 the "plus" line because it must begin with the plus-character
`+`. The rest of the line after the plus can be anything; it is often left
blank.[^plusline]

[^plusline]: The original fastq
  [specification](http://dx.doi.org/10.1093/nar/gkp1137)
  (doi:10.1093/nar/gkp1137) allowed the sequence and quality information to run
  over multiple lines (like in the fasta format). This led to a lot of
  confusion, since `+` and `@` appear in some quality encodings. It's now
  recommended to *not* spread the sequence and quality information over
  multiple lines. Thus, the plus line is there for backward compatibility.

The quality line gives information about the quality of the base calls shown in
the sequence line.  Each character gives information about the quality of one
base call.  Confusingly, the encoding has changed in overlapping and sometimes
non-redundant ways.[^ascii] In the newest Illumina format, the encoding goes,
from low quality to high quality:

    !#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHI

The letter `I`, the highest-quality mark, means that there is a $10^{-4.0}$
probability that this base is wrong (i.e., a 99.99% chance that it is correct).
`H`, the second-highest quality, means that there is a $10^{-3.9}$ chance; `G`
means $10^{-3.8}$, and so on.[^phred] The exclamation point is special: it
means a quality of zero, i.e., that the sequencer has no idea what that base
is.[^excl]

[^ascii]: Technically, these different encodings are named by their ASCII
  "offsets". ASCII is a system that associates individual characters with
  integers. The system I show here has an ASCII offset of 33: the character `I`
  has an ASCII value of 73, and the offset means you subtract the offset 33
  from the ASCII value 73 to get the quality score 40. The other common offset
  is 64: in that case, the character `I` encodes quality 9. Illumina used a
  64-offset for a while, but newer machines use a 33-offset.
[^phred]: This conversion between quality $Q$ (the integer) and the
  probability $p$ of incorrect calling is the "Phred" or "Sanger"
  system: $Q = -10 \log_{10} p$.
  There is at least one other way of converting between
  $Q$ and $p$, the "Solexa" system.
[^excl]: Even more confusingly, in some versions of Illumina, the very low
  ASCII scores were used to mean special things. In the older, 64-offset
  Illumina encoding, quality 3 (character `C`) was the lowest possible, and the
  quality 2 character (character `B`) was instead used to show that the
  Illumina software had done its own internal quality trimming and had decided
  that, starting with the first `B`, that the rest of the sequence was "bad".

Here's an example fastq entry. The sequence and quality lines are too long to
fit on the page, so I cut out some letters in the middle and put those dots
instead:

    @MISEQ578:1:1101:15129:1752#CCGACA/1
    TATGGTGCCAGCCGCCGCGGTA...GCGAAGGCGGCTCACTGGCTCGATACTGACGCTGAG
    +
    >1>11B11B11>A1AA0A00E/...FF@@<@FF@@@@FFFFFFEFF@;FE@FF/9-AAB##

Some things to note about this read:

- The first line gives information about the machine used, where the read was
  on the flow cell, etc. `CCGACA` was the barcode read, and the final `/1`
  means it was a forward read.
- The plus line has been left blank.
- The quality of the read's base calls decreases from `>`, encoding quality 29
  (i.e., a $10^{-2.9} = 0.1\%$ probability of error), all the way down to `#`,
  or quality 2 (i.e., a $10^{-0.2} = 63\%$ probability of error).

#### Fasta format

Fasta files usually have the extension `.fasta`, `.fa`, or `.fna`.[^fasta] They
are made up of *entries* that each correspond to a single sequence. Each entry
consists of a *header* line and one or more *sequence* lines.

[^fasta]: The last `a` in `fasta` stands for "all", meaning nucleotide or amino
  acid or whatever. The `n` in `fna` stands for "nucleotide".

The *header* line must start with the greater-than symbol `>`. This signals the
start of a new entry. The rest of the header line is an identifier, analogous to the content of the header line in a fastq.

In a fastq file, each linebreak was meaningful. In a fasta file, only the
linebreak at the end of the header line is meaningful. Linebreaks in the
following sequence lines are all ignored. The sequence for this entry just
keeps on going until you hit another `>`. The early
recommendation was to wrap all lines at 80 characters to make them easy to read
on old-school terminals. Many people and software tools conform to this
recommendation; others make each entry just two lines, one header and one
sequence.

Fasta files provide strictly less information than fastq files, so normally
you'll move to a fasta format after quality filtering, when you've decided
you aren't going to use the quality data again.

Here's an example fasta entry in the traditional format (i.e., each line
no more than 80 characters and the sequence is spread over multiple
lines):

    >sequence1
    TACGGAGGATCCGAGCGTTATCCGGATTTATTGGGTTTAAAGGGAGCGTAGGCGGGTTGT
    TAAGTCAGTTGTGAAAGTTTGCGGCTCAACCGTAAAATTGCAGTTGATACTGGCATCCTT
    GAGTACAGTAGAGGTAGGCGGAATTCGTGGTGTAGCGGTGAAATGCTTAGATATCACGAA
    GAACTCCGATTGCGAAGGCAGCCTGCTGGACTGTAACTGACGCTGATGCTCGAAAGTGTG

### Finding your raw data and metadata

Before trying to process your dataset, be sure you have the appropriate raw data[^raw_data] and metadata.
In all cases, this means you'll need at least one set of reads.
For Illumina, this means a *fastq* file that might have a name like:

    130423Alm_D13-1939_R1_sequence.fastq

This filename is typical for raw sequencing data: it has information about the date (2013-04-23), the
group that requested the sequencing (Alm Lab), then something about the specifics of the sequencing
run. The `_R1_` indicates that these were forward reads.

[^raw_data]: In what follows, I'll talk about "raw data", by which I mean data that you would get from the sequencing center. For Illumina data at least, there is actually a more raw kind of data that comes right out of the sequencing machine that gets processed right away. The software that processes that very raw data changes slightly across different version, so be prepared for slight variations in the format of your "raw" data.

If you did paired-end sequencing, you will also need the *reverse reads*.
This is a fastq file with a
name like the forward reads except with `_R2_` in it.
Every entry in the reverse reads should match an entry in the forward reads.

### Demultiplexing

It is now standard practice for delivered to you to have already been
*demultiplexed*, meaning split into samples. Rather than all the forward reads
from a sequencing run being in one big file, they are split, with one file per
sample. Reverse reads are similarly split so that each sample should have two
associated read files, one forward and one reverse.

If you data are not demultiplexed (i.e., you only have one big file of forward
reads), then you will also need the *barcode* or *index reads*. Depending on
your Illumina version, this information might be in different places. In some
datasets, it's in the file with the forward reads. For example, the file I
mentioned above, which was not demultiplexed, the first line is

    @MISEQ578:1:1101:15129:1752#CCGACA/1

The barcode read is
`CCGACA` (between the `#` and the `/1`). In other datasets, you might find
the index reads in a file with a name that has `_R3_`, `_I_`, or `_I1_` in
it.

If you have barcodes, you will also need a *barcode map*.
This is the information about what barcode goes with what sample. A common
gotcha in 16S data processing is that the barcode map might have barcodes
that are reverse complements of what are in the samples.

In theory, demultiplexing sounds simple: you look in the raw sequence for the
barcode, look up what sample that barcode corresponds to using the barcode map,
and then trim off the barcode. In practice, there are two questions that need
to be answered:

- *Which of the known barcodes is the best match for this barcode read?* That's
  a pretty straightforward answer. But what if there's a tie? In fact,
  barcodes are chosen with an error-correcting
  code[^code] so that a tie implies that you have
  at least two errors in the read, which is unlikely.
- *Is the match with the known barcode good enough?* A common approach is,
  given a barcode read, to compare that read with all the known barcodes (i.e.,
  the barcodes you're looking for). If the known barcode that matches best has
  more than one mismatch with the barcode read, call that read "bad" and discard
  it.

[^code]: Hamady *et al*. (doi:10.1038/nmeth.1184)

### Removing primer sequences

During PCR amplification, it is the primer that is amplified, not the DNA that
the primer was bound to. This means that, if there was a mismatch between the
primer and the DNA of interest, you won't see the actual DNA; you only ever see
the primer sequence. Keeping the primer sequences in your reads makes it appear
in downstream analyses as if the primer sequence was the actual sequence
present in the sampled DNA. The common practice is to cut off the primers, and
nowadays primers may have already been removed (or "trimmed") before they are
handed to you the researcher.

If the primers haven't already been removed, you'll need to remove them
yourself. In an ideal world, this is straightforward: you find the piece of
your read that matches the primer, and you pop it off. In practice, there are
two important considerations:

- *Where do you look for the primer?* Does the primer start at the very first
nucleotide of the read, or a little further in? You can put a lot of flexibility
in this step without a lot of negative effects, but it's good to know what's
going on in your data.
- *What does "match" mean?* How many mismatched nucleotides do you allow between the
read and your primer sequence before you consider the read "bad"? In practice,
it's common to only keep reads that have at most one error in the primer match.

There are also some less intellectually interesting "gotcha's" that I suffered
multiple times as a graduate student:

- I didn't know the primer sequences, or the primer sequences I was told were
  not the actual ones present in the data.
- I thought I had the sequences of the primers but I actually had the reverse
  complements of those primers.
- I thought (or had been told) that the primers had been pre-removed when they
  were actually still present.

### Summary of expected files

Overall, you will likely need:

- Demultiplexed forward reads, with one file per sample
- Demultiplexed reverse reads, with one file per sample

However, depending on how the data were delivered to you, you might also
need:

- Non-demultiplexed forward reads (i.e., one big file of forward reads)
- Non-demultiplexed reverse reads
- Barcode reads
- Barcode map
- Primer sequences

If you download a dataset or get it from a collaborator, it might come in an
already-processed format. Depending on your purposes, it might be fine to use
that data, which will look similar to something we'll get a little further down
this pipeline. It's useful to know exactly what the content of the data is before
you start working on it. If it lacks any of these parts, make sure to find
them before you try to get to work!

## Phase II: Cleaning

These steps take the raw data and turn it into biologically relevant stuff.
There is some freedom about the order in which they can be done. I separate
these steps out from preprocessing because the choices you make here can
substantially affect your data.

### Quality filtering

Sequences tend to vary in overall quality (some good, some bad)
and the number of bases they have that are good. Inherent in the Illumina technology is
a trend for sequences to decrease in quality as you move down the sequence.

![Reads differ in overall quality and number of "non-bad" reads. (data smoothed over 10 bases)](images/qual-dec.png)

The sequencer will give you a sort of quality report about your sequences' average
quality. It will give you a sense of whether your sequencing run as a whole was
good, and it will give you a sense of whether you got the sort of good-quality
length you were hoping for.

![A read quality report delivered by the Illumina software.](images/quality.png)

The big quality report gives you a sense of whether you should do the whole
sequencing run over again. Even in a good sequencing run there are bad sequences
that should be filtered out. There are two common ways to quality filter:

- *Quality trimming* means truncating your reads at some nucleotide after which the sequence
is "bad".[^othertrim] A common approach is to truncate everything after the first
nucleotides whose quality falls below some threshold.
- *Global quality filtering* means discarding an entire read if the average quality
of the read is too low. Maybe no individual nucleotide falls below your trim
threshold, but the general poor quality of the read means that you'd rather not
include it in analysis. This criterion is expressed equivalently as "average
quality" or "expected number of errors".[^flyv]

[^othertrim]: Confusingly, "trimming" also refers to a different process when, if you're doing unpaired amplicon sequencing, you pick a length, discard all reads shorter than that, and truncate all the longer sequences at that length. It is essential to do this when using certain *de novo* OTU calling methods, and it's probably beneficial to do with reference-based OTU calling and or taxonomy assignment methods.

[^flyv]: Edgar & Flyvbjerg (doi:10.1093/bioinformatics/btv401)

### Merging

When doing paired-end sequencing, it's desirable for the two reads in the pair to overlap in the middle.

This produces a single full-length read whose quality in the middle positions
is hopefully greater than the quality of either of the two reads that produced
it. The process of combining the forward and reverse reads is called *merging*
(or "overlapping", "assembling", or "stitching").

![Merging aligns reads, makes a new sequence, and computes new quality scores. Adapted from the `usearch` manual (drive5.com/usearch/manual/merge_pair.html).](images/merge-quality.png)

Merging requires answering a few, fairly complex questions:

- *What is the "best" position for merging?* If you were sure all your
  amplicons are exactly the same size, then this is trivial: just overlap them
  at the right length.  However, even in amplicon sequencing, there are
  insertions and deletions in the 16S variable regions, so we can't be sure that
  all merged reads will be the exactly the same length.
- *Is the "best" position good enough?* If you have two reads that don't
  overlap at all, should you even include it in the downstream analysis?[^5]
  How good is good enough?
- *What are the quality scores of the merged nucleotides?* This requires some
  basic Bayesian statistics.[^bayesian]

[^5]: If you had two paired-end reads that didn't overlap but you were somehow sure of the final amplicon size, then you could insert a bunch of `N`'s in between.
[^bayesian]: Rodrigue *et al*. (doi:10.1371/journal.pone.0011840); Edgar & Flyvbjerg (doi:10.1093/bioinformatics/btv401)

## Phase III: Denoising (and chimera removal)

Denoising is the process of accounting for errors inherent in sequencing
technology, especially the Illumina platform. In short, denoising "corrects"
sequencing error, decreasing the diversity of sequences in the data that are
due to technological error rather than to true biological diversity.
Two important implementations of
denoising are DADA2[^dada] and
Deblur[^deblur].

[^dada]: Callahan *et al*. (doi:10.1038/nmeth.3869)
[^deblur]: Amir *et al*. (doi:10.1128/mSystems.00191-16)

The work of denoising
was previously done as a part of operational taxonomic unit (OTU) calling.
Denoising and OTU calling are sufficiently conceptually complex and
historically intertwined that I will discuss them separately in the next
chapter.

This step implicitly includes two other steps that were traditionally treated separately:

- *Dereplicating*. There are fewer *sequences* (strings of `ACGT`) than there
  are *reads*. This step identifies the set of unique sequences, which is
  usually much smaller than the number of reads.
- *Proveniencing* (or "mapping" or "indexing"). How many reads of each sequence
  were in each sample? (Only I call it "proveniencing"[^3]. I find all the
  other names I've heard confusing.)

[^3]: In archaeology, an artifact's _provenience_ is the place within the
  archaeological site where it was found.

### Chimera removal (or "slaying")

As mentioned early on, PCR can produce chimeric sequences.[^chimera] Depending
on your choices about OTU calling, you may want to remove chimeras after
dereplicating. Chimera removal checks to see which of your dereplicated sequences
can be made by joining the first part of one sequence (the "head") with the last
part of another sequence (the "tail").

Chimera removal methods come in two main flavors: *reference-based* and *de novo*.
In reference-based methods, you look for the head and tail sequences in some
database. Popular databses include Greengenes, SILVA,
the Broad Institute's ChimeraSlayer
(or "Gold") database, and the Ribosomal Database Project (RDP) "Gold"
database.

In *de novo* methods, you ask which of your sequences
have could be generated by combining other (typically more abundant) sequences
from that same dataset.
In the past, this was a computationally-expensive undertaking, but there are
ever-improving methods, notably, the UPARSE[^uparse] algorithm.

[^uparse]: Edgar (doi:10.1038/nmeth.2604)
[^chimera]: The Chimera was a monster in Greek mythology. It had the head of a lion and the tail of a snake. It was slain by the hero Bellerophon.

## Phase IV: OTU calling

As mentioned above, calling (or "picking") operational taxonomic units (OTUs)
is a conceptually and historically complex topic, so I will treat it in a
separate chapter. In short, OTU calling assigns every
dereplicated sequence to a group, or OTU. You can combine the sequence-to-OTU
information from OTU calling with the sequence-to-sample-counts information
from proveniencing to make an OTU table that shows how many reads mapping to each
OTU appear in each sample.

### Phase V: Analysis

The part where you actually use your data! Analysis is outside the scope of this work.
