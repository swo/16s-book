# Where 16S data comes from

By "16S data" I mean amplicon sequencing of some section of the bacterial 16S gene. A lot of what I discuss in this document may also apply to other types of taxonomic marker sequences like the eukaryotic 18S or the fungal ITS.

## The 16S gene

All bacteria (and archaea) have at least one copy of the 16S gene in their genome.[^kembel] The gene has some sections that are *conserved*, meaning that they are very similar across all bacteria, and some sections that are *variable*. The idea behind 16S sequencing is that the variable regions are not under strong evolutionary pressure, so random mutations accumulate there. Closely-related bacteria will have more similar variable regions than distantly-related bacteria.

![**The 16S gene has variable regions.** These are nucleotide positions in the aligned 94% OTUs in [Greengenes](http://dx.doi.org/10.1128/AEM.03006-05). "Variability" (which I made up for the purposes of this figure) at a position is {$$}1-{/$$} the fraction of OTUs that had the most common nucleotide at that position. For example, if all OTUs had `A` at a position, the "variability" is 0. If half of the OTUs had `A` at that position, the "variability" is {$$}0.5{/$$}. The actual plot is very spiky, so I smoothed over 50 nucleotide windows. This shows you that there are subsequences of the gene that are more variable than others.](fig/variab.pdf)

[^kembel]: It's not unusual for bacteria to have multiple copies of the 16S gene, and those copies might not be identical to one another. Some people are concerned by the effect this could have on 16S data (e.g., [Kembel *et al*.](http://dx.doi.org/10.1371/journal.pcbi.1002743)

## Amplifying the gene

After a sample is taken, the cells in the sample are lysed, typically using some combination of chemical membrane-dissolving and physical membrane-busting. The DNA in the sample is *extracted*, meaning that all the protein, lipids, and other stuff in the sample is thrown away. From this pile of DNA spaghetti, we aim to collect information about the bacteria that were in the original sample.

In theory, sequencing all the DNA in the sample at some depth will give as much information as just sequencing the 16S gene alone. In practice, this approach is more expensive and, in terms of the bioinformatics, much more complex. You'll need to go elsewhere to learn about the theory and practice of metagenomic sequencing. (Confusingly, the adjective "metagenomic" is also applied to 16S amplicon sequencing of bacterial communities, since these samples have more than one genome.)

In the amplicon sequencing approach, PCR is used to amplify a section of the 16S gene. The size of the sequenced section is limited by the length of reads produced by high-throughput sequencing. The sections of the 16S gene that are amplified are named according to what variable regions of the gene are covered. There are nine variable regions, but there isn't an exact definition of where they begin and end.

- *V1-V2* (the first two variable regions). This section of the gene provides better taxonomic resolution for some bacteria associated with the skin microbiome, so skin studies sometimes sequence V1-V2.
- *V4* (variable region 4). This section of the gene provides good taxonomic resolution for bacteria associated with the gut microbiome, so it is the most popular section. I get the sense that V4 is also the best "catch-all" region, but I don't know of a good reference to back up that sense.
- *V5-V6*. I've only seen this section in projects that aim to be particularly complete (e.g., the [Human Microbiome Project](http://hmpdacc.org/)).

PCR reactions on these regions have primers that match the constant regions around the variable regions. Papers should always mention which primers they used, and they usually also mention the amplified region. The primers have names like 8F (meaning, a forward primer starting at nucleotide 8 in the gene) and 1492R (meaning, a reverse primer starting at nucleotide 1492).

Compared to the metagenomic approach, the amplicon-based approach has some advantages. First, as mentioned above, it is cheaper. Second, because only bacteria have the 16S gene, all your sequencing reads go toward sequencing bacteria. In contrast, the majority of metagenomic reads from a swab of human skin will be reads of human DNA. Third, your reads come "pre-aligned". (They're not *actually* "aligned" in the bioinformatic sense, but it's a good analogy.) This means that you know where each read came from: the 16S gene, from this nucleotide position to that nucleotide position. Every read therefore provides, roughly speaking, an equal amount of information about the composition of the sample's bacterial community.

## The amplified DNA is not exactly like the original DNA

The process of extracting DNA from bacterial cells and then amplifying a 16S region introduces certain biases into the resulting sequence data. These effects mean its better to look for changes in bacterial community structure rather than assert that such-and-such a species is more abundant than other-and-such a species. It also means that large effects, like variations over orders of magnitude, are to be trusted far more than smaller changes. These grains of salt to be kepts in mind are
*extraction bias*, *PCR bias*, and PCR *chimeras*.

The strongest effect is from extraction bias: different cells respond differently to different extraction protocols. Splitting a sample and using different extraction protocols on the different parts will produce markeldy different results. The original HMP effort suffered a big surprise during early data analysis: no matter how you slice it, the biggest signal in the HMP data is "center". Each sample in HMP was processed at one of the three sequencing centers, each of which used their own extraction protocol. The thing that makes two samples most different in the HMP data is if they were sequenced at different centers.

*PCR bias* is less important than extraction bias. I don't think PCR bias is a huge problem, but it's good to have heard about it. First, even though the PCR primers bind a "constant" region, some bacteria in the sample will have different nucleotides there, meaning that the PCR primers will bind with different affinities to the DNA of different bacteria. This effect decreases the number of reads from bacteria whose constant regions don't perfectly match the primer.[^2] Second, it's known that PCR has different efficiencies for different types of sequences, meaning that some 16S variable regions will amplify better than others. Third, statistical fluctuations can occur, especially in low-diversity samples. This means that a sequence that, by chance, gets lots of amplification in early PCR cycles could dominate the sample in late PCR cycles.

[^2]: It may be that there are a lot of interesting bugs whose 16S sequences are so divergent that they don't match the typical primers (cf. doi:10.1038/nature14486).

In general, PCR bias is not as bad when there is more DNA and (relatedly) when the PCR is run for fewer cycles.

In the lab we've run experiments to quantify PCR bias: we synthesize some DNA that looks like bacterial 16S genes, mix them in known proportions, do the amplification and sequencing, and compare the sequencing data to the known proportions. The errors are somewhere in the neighborhood of 1% to 10%. Not enough to make you think that 16S data is all garbage, but high enough to make you doubt small changes in composition.

PCR also creates a weird artifact called *chimeras*. When using PCR to amplify two DNA sequences *a* and *b*, you'll get a lot of *a*, a lot of *b*, and some sequences that have an *a* head and *b* tail (or vice versa). There are some things about your PCR protocol that you can adjust to decrease the prevalence of chimeras, but they are beyond the scope of this document.

There are also biases that arise from *any* DNA-based experiment, like the biases that result from the method of collection or storage. Some people run mini-studies to ask about the effects of storage at different temperatures for different times, the effect of the buffer used, etc. Regardless of what method of collection and storage is used, using the same method for every sample in a study is a good way to reduce biases.

## Multiplexing helps evaluate contamination (or other weirdness)

Next-generation sequencing wasn't that helpful to microbial ecology until *sample multiplexing* (or "barcoding") was worked out. The first paper to use multiplexed bacterial samples came out in 2008. Before multiplexing, every sample had to be run on its own sequencing lane. This was expensive and bioinformatically annoying, since, especially in those dark ages of sequencing, weird stuff would frequently happen during sequencing runs, and it was hard to distinguish a bad lane from a
weird sample.

In contrast, multiplexing adds a barcode or "tag" to the 16S amplicon. Each barcode corresponds to a sample, and all amplicons in that sample get that barcode. It's now common to multiplex 96 (or 384) samples and sequence them in one lane. Aside from making the sequencing 100-fold cheaper, multiplexing means that it's easier to include some controls in each lane:

- *Negative controls*: Usually just vehicle with no DNA, as a way to check for contamination from reagents or poor sample preparation.
- *Positive controls*: Mock communities of known composition, which can be used to check that the sequencing was not "weird". If you have a lot of samples from the same project and you need to run them in more than one lane, you can use the positive controls as an internal check that sequencing proceeded similarly across lanes.

The bioinformatic cost of multiplexing is that the reads must be *demultiplexed* in the analysis stage. This is not very difficult.

## Sequencing

A little more work has to be done before putting the sample in the sequencer. These steps will depend on the sequencing platform. Here I'll talk about Illumina because it's popular and I have experience with it.

Samples to be sequenced on an Illumina machine need to have Illumina-specific *adapters* added in another PCR. These adapters allow the DNA amplicons to bind the flowcell where they are sequenced. It is sometimes also desirable to have a *diversity region* added between the adapter and the 16S primer. The Illumina sequencers expect to see a diversity of nucleotides at every read position. In amplicon sequencing, almost all the reads are the same through the primer region, which freaks out the sequencer. A diversity region is just some random nucleotides that helps the sequencer do its job. In our lab we use `YRYR`, where `Y` means `T` or `C` and `R` means `G` or `A`.

All of these pieces --the 16S region you're interested in, forward and reverse primers, barcodes, diversity region, and Illumina adapters-- are all made into a single *PCR construct*, which is a single piece of DNA. The sequencer reads the nucleotides in the construct and uses its knowledge about the arrangement of the construct to infer which nucleotides are the region of interest and which are the barcode.

![**An example PCR construct.** The parts labeled on top are interesting only for technical reasons. The parts on the bottom have information that's useful for someone analyzing sequence data.](fig/pcr-construct.pdf)
