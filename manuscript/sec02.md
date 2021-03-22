# Where 16S data comes from

By "16S data" I mean amplicon sequencing of some section of the bacterial 16S rRNA
gene. A lot of what I discuss in this document may also apply to other types of
taxonomic marker sequences like the eukaryotic 18S or the fungal ITS.

## The 16S gene

All bacteria (and archaea)[^chloro] have at least one copy of the 16S gene in
their genome.[^kembel] The gene has some sections that are *conserved*, meaning
that they are very similar across all bacteria, and some sections that are
*variable* (or "hypervariable"). The idea behind 16S sequencing is that the variable regions are not
under strong evolutionary pressure, so random mutations accumulate there.
Closely-related bacteria will have more similar variable regions than
distantly-related bacteria.

To get a feel for the variability at different positions in the gene, I looked
at the aligned 94% OTUs in [Greengenes](dx.doi.org/10.1128/AEM.03006-05).
"Variability" (which I made up for the purposes of this figure) at a position in the gene is
one minus the fraction of OTUs that had the most common nucleotide at that
position. For example, if all OTUs had `A` at a position, the "variability" is
0. If half of the OTUs had `A` at that position, the "variability" is
0.5. The actual plot is very spiky, so I smoothed over 50 nucleotide
windows. This shows you that there are subsequences of the gene that are more
variable than others.

![The 16S gene has variable regions.](images/variab.png)

[^chloro]: Chloroplasts, found in algae and other eukaryotes, have a ribosomal gene that is very similar to 16S and often ends up getting amplified in 16S data sets.

[^kembel]: It's not unusual for bacteria to have multiple copies of the 16S gene, and those copies might not be identical to one another. Some people are concerned by the effect this could have on interpretations of 16S data (e.g., [Kembel *et al*.](http://dx.doi.org/10.1371/journal.pcbi.1002743); doi:10.1371/journal.pcbi.1002743 and [Case *et al.*](http://dx.doi.org/10.1128/AEM.01177-06); doi:10.1128/AEM.01177-06).

## Getting DNA from a sample

After a sample is taken, the cells in the sample are lysed, typically using some combination of chemical membrane-dissolving and physical membrane-busting. The DNA in the sample is *extracted*, meaning that all the protein, lipids, and other stuff in the sample is thrown away. From this pile of DNA spaghetti, we aim to collect information about the bacteria that were in the original sample.

## Amplifying the gene

In the amplicon sequencing approach, polymerase chain reaction (PCR) is used to amplify a section of the
16S gene. The size of the sequenced section is limited by the length of reads
produced by high-throughput sequencing. The sections of the 16S gene that are
amplified are named according to what variable regions of the gene are covered.
There are nine variable regions, but there isn't an exact definition of where
they begin and end. Different regions can provide different taxonomically
resolution for different parts of the microbial tree of life.

Some regions I've seen amplified include:

- *V1-V2* (the first two variable regions). This section of the gene provides better taxonomic resolution for some bacteria associated with the skin microbiome, so skin studies sometimes sequence V1-V2.
- *V4* (variable region 4). This section of the gene provides good taxonomic resolution for bacteria associated with the gut microbiome, so it is the most popular section. I get the sense that V4 is also the best "catch-all" region, but I don't know of a good reference to back up that sense.
- *V5-V6*. I've only seen this section in projects that aim to be particularly complete (e.g., the [Human Microbiome Project](http://www.hmpdacc.org)).

PCR reactions on these regions have primers that match the constant regions around the variable regions. Papers should always mention which primers they used, and they usually also mention the amplified region. The primers have names like 8F (meaning, a forward primer starting at nucleotide 8 in the gene) and 1492R (meaning, a reverse primer starting at nucleotide 1492).

### Amplicon sequencing vs. shotgun ("metagenomic") sequencing

First, a note on terminology.
Technically, "metagenomic" means "related to more than one genome", that is,
sampling from an entire community rather than from a single cell or a single
colony. In common speech, I hear "metagenomics" used to mean
_shotgun_ metagenomics (i.e., trying to sequence all the DNA in a sample),
as opposed to amplicon sequencing (even though amplicon sequencing,
as we're talking about, is metagenomic, since it usually involves many different
species).

In theory, amplicon sequencing gives you strictly less information that shotgun
sequencing. If you shotgun sequence at a great enough sequencing depth, you should
be able to reconstruct all the information that you could get from 16S amplicon
sequencing.

In practice, the amplicon-based approach has some advantages.
Because only bacteria and archaea have the 16S gene, a tube of 16S amplicon DNA
mostly carries information about microbes. In contrast, the majority of shotgun reads from,
say, a swab of human
skin will be human DNA. This means that, for the same depth of sequencing,
16S amplicon sequencing will provide much more information about the bacterial
community structure than will shotgun sequencing. Shotgun sequencing projects
tend to be more expensive, since they need to sequence deeper to get the
interesting information.

Amplicon sequence data is also easier to work with from a bioinformatic point of
view. Amplicon sequences come "pre-aligned". (They're
not *actually* "aligned" in the bioinformatic sense, but it's a good analogy.)
This means that you know where each read came from: the 16S gene, starting and ending
at the parts of the gene the primers were designed to target.
Every read therefore provides,
roughly speaking, an equal amount of information about the composition of the
sample's bacterial community. Shotgun sequences, in contrast, need to be
assembled, which is far more complicated bioinformatic process than anything
you will find in this document.

## The amplified DNA is not exactly like the original DNA

The process of extracting DNA from bacterial cells and then amplifying a 16S
region introduces certain biases into the resulting sequence data. These effects
mean that it's better to look for changes in bacterial community structure rather than
assert that such-and-such a species is more abundant than other-and-such a
species. It also means that large effects, like variations over orders of
magnitude, are to be trusted far more than smaller changes. The grains of salt
to be kept in mind are *extraction bias*, *PCR bias*, PCR *chimeras*, and
lab-specific effects.

### Extraction bias

Different cells respond differently to different extraction protocols. Splitting
a sample and using different extraction protocols on the different parts can
produce markedly different results. There are many papers about this[^extract].
My takeaway is that, if you're comparing two data sets, it's important to know
if they used the same extraction methodology, since differences in the 16S
data could be due to differences in the microbes themselves or just in the methods
used to extract the DNA.

[^extract]: A quick web search gave me: [Salter *et al.*](http://dx.doi.org/10.1186/s12915-014-0087-z) (doi:10.1186/s12915-014-0087-z), [Walker *et al.*](http://dx.doi.org/10.1371/journal.pone.0088982) (doi:10.1371/journal.pone.0088982), [Rochelle *et al.*](http://dx.doi.org/10.1016/0378-1097(92)90188-T) (doi:10.1016/0378-1097(92)90188-T), etc. But compare [Rubin *et al.*](http://dx.doi.org/10.1002/mbo3.216) (doi:10.1002/mbo3.216).

### PCR bias

I don't think *PCR bias* is a
huge problem, but it's good to have heard about it. First, although we say the PCR
primers bind a "constant" region, there is still variation in those regions.
Thus, some bacteria in the sample will have
different nucleotides at the primer binding site, meaning that the PCR primers will bind with
different affinities to the DNA of different bacteria. This effect decreases
the number of reads from bacteria whose constant regions don't match
the primer.[^2]

"PCR bias" encompasses other things beyond primer site binding bias.
It's known that PCR has different efficiencies for different types of
sequences, meaning that some 16S variable regions will amplify better than
others. Also, statistical fluctuations can occur, especially in low-diversity
samples. This means that a sequence that, by chance, gets lots of amplification
in early PCR cycles could dominate the sample in late PCR cycles.

[^2]: It may be that there are a lot of interesting bugs whose 16S sequences are so divergent that they don't match the typical primers (cf. [Brown *et al.*](http://dx.doi.org/10.1038/nature14486); doi:10.1038/nature14486).

In general, PCR bias is not as bad when there is more DNA and (relatedly) when the PCR is run for fewer cycles.

In my PhD lab, some folks ran unpublished experiments to quantify PCR bias: they synthesized
some DNA that looks like bacterial 16S genes, mixed that DNA in known proportions,
amplified the mixture, sequenced the amplified DNA, and compared the sequencing data to the known
proportions of input DNA. The errors are somewhere in the neighborhood of 1% to 10%.
It's not high enough to make me think that 16S data is all garbage, but it is
high enough to make me doubt small (say, two-fold) changes in composition.

### Chimeras

PCR also creates weird artifacts called *chimeras*. When using PCR to amplify
two DNA sequences *a* and *b*, you'll get a lot of *a*, a lot of *b*, and some
sequences that have an *a* head and *b* tail (or vice versa). There are some
things about your PCR protocol that you can adjust to decrease the prevalence
of chimeras.

### Lab-specific effects

There are also biases that arise from *any* DNA-based experiment, like the
biases that result from the method of collection or storage. Some people run
mini-studies to ask about the effects of storage at different temperatures for
different times, the effect of the buffer used, etc. Regardless of what method
of collection and storage is used, using the same method for every sample in a
study is a good way to reduce biases.

I suspect that a stronger signal comes from reagent or lab-specific contamination.
Commercial reagents often come pre-loaded with bacteria. (Like, not in a good way.)
In my PhD lab, we often found
_Halomonas_ and _Shewanella_ species where they shouldn't be.
The effect appeared to depend on the particular extraction kit used.

## Multiplexing helps evaluate contamination (or other weirdness)

Next-generation sequencing became more helpful to microbial ecology when
*sample multiplexing* (or "barcoding") was worked out in the early
2000s.[^multi] Before multiplexing, every sample had to be run on its own
sequencing lane. This was expensive and bioinformatically annoying, since,
especially in those dark ages of sequencing, weird stuff would frequently happen
during sequencing runs, and it was hard to distinguish a bad lane from a weird
sample.

[^multi]: Cf., e.g., [Binladen *et al.*](http://dx.doi.org/10.1371/journal.pone.0000197) (doi:10.1371/journal.pone.0000197).

Multiplexing, by contrast, adds a barcode or "tag" to the 16S amplicon. Each
barcode corresponds to a sample, and all amplicons in that sample get that
barcode. It's now common to multiplex 96 (or 384) samples and sequence them in
one lane. Aside from making the sequencing 100-fold cheaper, multiplexing means
that it's easier to include some controls in each lane:

- *Negative controls*: Usually just vehicle with no DNA, as a way to check for contamination from reagents or poor sample preparation.
- *Positive controls*: Mock communities of known composition, which can be used to check that the sequencing was not "weird". If you have a lot of samples from the same project and you need to run them in more than one lane, you can use the positive controls as an internal check that sequencing proceeded similarly across lanes.

The bioinformatic cost of multiplexing is that the reads must be *demultiplexed*
in the analysis stage. This is easy.

## Sequencing

A little more work has to be done before putting the sample in the sequencer.
These steps will depend on the sequencing platform. Here I'll talk about
Illumina because it's popular[^roche] and I have experience with it. If you're using
a different sequencing platform, then you'll need to learn about the quirks
of that platform elsewhere.

[^roche]: Interestingly, it wasn't that long ago that 454 (or "Roche") sequencing led the next-generation field. Plenty of papers use "pyrosequencing" (the technical word for 454's sequencing methodology) as a synonym for "next-generation sequencing".

Samples to be sequenced on an Illumina machine need to have Illumina-specific
*adapters* added in a third PCR (one for amplification, one to add the barcodes,
and one to add the adapters). These adapters allow the DNA amplicons to bind
the flowcell, where they are sequenced. It is sometimes also desirable to have a
*diversity region* added between the adapter and the 16S primer. The Illumina
sequencers expect to see a diversity of nucleotides at every read position. In
amplicon sequencing, almost all the reads are the same through the primer
region, which freaks out the sequencer. A diversity region is just some random
nucleotides that helps the sequencer do its job. In our lab we use `YRYR`,
where `Y` means `T` or `C` and `R` means `G` or `A`.

All of these pieces ---the 16S region you're interested in, forward and reverse
primers, barcodes, diversity region, and Illumina adapters--- are all made into
a single *PCR construct*, which is a single piece of DNA. The sequencer reads
the nucleotides in the construct and uses its knowledge about the arrangement of
the construct to infer which nucleotides are the region of interest and which
are the barcode.

![An example PCR construct.](images/pcr-construct.png)
