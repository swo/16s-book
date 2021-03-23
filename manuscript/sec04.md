
# Denoising and OTU calling

As mentioned in the last chapter, denoising and OTU calling are complex and
intertwined topics, so I discuss them separately here.

## An abridged history of the OTU

In the 1980s, Carl Woese showed that the 16S gene could be used as a molecular
clock. Using 16S data, he re-drew
the tree of life, breaking up the older
Monera[^monera] into Bacteria and Archaea, showing that Eukaryotes and Archaea are closer
cousins than are Archaea and Bacteria.[^woese] The 16S gene was therefore a promising
practical candidate for distinguishing bacterial species.[^known]

[^woese]: Woese, Kandler, Wheelis (doi:10.1073/pnas.87.12.4576)

[^known]: In 1991, PCR-amplified portions of the 16S gene were used to identify known species (Weisburg *et al*. [doi:10.1128/jb.173.2.697-703.1991]). The paper has a prescient final sentence: "While [PCR] should not be a routine substitute for growing bacteria, picking individual colonies, and confirming their phenotypic and biochemical identities, it will enable experiments to be performed that were not previously possible."

[^monera]: I'm shocked that, attending public high school in the early 2000s, we were *still* taught about Monera and Protista rather than about Bacteria, Archaea, and Eukaryotes.

The species concept is easy to define for sexual macroorganisms: two
living things of opposite sex are in the same species if they can produce
fertile offspring together. Bacteria don't have sex, but they do perform
homologous recombination. Homologous recombination requires some sequence
similarity, so it came about that
a common definition of a bacterial species was all
those strains whose isolated DNA was 70% DNA-DNA-hybridization similar.[^concept]

[^concept]: Konstantinidis, Ramette, Tiedje (doi:10.1098/rstb.2006.1920). To this day there is still a large debate about the microbial species "concept".

In the 1990s, people sequenced the 16S genes of the strains grouped into species
by the hybridization assay. It emerged as a rule of thumb that two bacteria were
the same species if their 16S genes had 97% nucleotide identity.
Because of this history, a lot of discussion around OTUs involves finding 97%
clusters, and "OTU" was often used as a shorthand for "97% clusters".

Personally, the word "operational" in OTU makes me think that an OTU is a good
name for whatever group of sequencing reads you choose to be the unit of
analysis in your downstream work. This, however, is not the standard nomenclature
and various other terms like "phylotype" and "oligotype"[^oligo] have been used for
groupings related to but conceptually distinct from "OTUs".

[^oligo]: Eren *et al*. (doi:10.1111/2041-210X.12114)

## Denoising

Historically, people called OTUs because for a few reasons. A first and very
practical reason was data reduction. Dereplication can give you hundreds of
thousands of unique sequences, and doing analysis with hundreds of thousands of
unique units was computationally infeasible in the early days of 16S
sequencing.

A second important and related reason was *denoising*. Imperfect
technology means that one can never really be sure whether two reads have
different sequences because of technological error or because those two reads
arose from biologically different sequences in different bacteria. One way to
denoise data was to say that we couldn't really trust our equipment to be able
to distinguish sequences that were less than about 97% similar anyway, so we
might as well lump those sequences into one unit for analysis.

To give a sense of what denoising is about, consider this hypothetical example.
Say you are sequencing an amplicon that has only 10 nucleotides, and the
sequencer has an error rate of 1%, meaning that each base pair has an
independent, 1% chance of being misreported. Some straightforward math shows
that there is a 90% chance tha tall 10 nucleotides will be correctly reported,
a 9.1% chance that 9 of 10 nucleotides will be correct (i.e., 1 will be
incorrect), and a 0.9% chance that 2 or more nucleotides will be incorrect.

In this example, if there was only one true sequence in the biological sample,
then we would expect 90% of reads to be that true sequence, while the remainder
would be split among the various erroroneous sequences. For example, of the
9.1% of reads, one in ten (i.e., 0.91% of the total reads) would have an error
in the first base pair, of which about one-third (i.e., 0.3% of the total reads)
would have each of the incorrect base pairs in it.

Percent of reads | Read sequence
--- | ---
90% | GACAGGTACA
0.3% | ***A***ACAGGTACA
0.3% | ***C***ACAGGTACA
0.3% | ***T***ACAGGTACA
0.3% | G***C***CAGGTACA
0.3% | G***G***CAGGTACA
0.3% | G***T***CAGGTACA
... | ...

Table: Hypothetical example in which there is a single 10 nucleotide sequence
present in the sample DNA, a 1% error rate, and an even distribution among
errors.

On the other hand, if one of these sequences that could be explained as error
was more frequent than was expected given the statistical model for errors,
then we would conclude it is also a real, biological sequence. For example, if
the first erroneous sequence (i.e., [aacaggtaca]{.smallcaps}) appeared as often
as the original sequence ([gacaggtaca]{.smallcaps}), then we would expect that
they are both meaningful. However, our ability to distinguish real biological
variations from technological error is limited by the abundance of these
potentially erroneous sequences and the sequencer error rate: if the error rate
is high or the true variant sequence is rare, we will not be able to determine
that it is not simply an erroneous read.

Denoisers use the sequencing data to infer the
sequencer's error rate and to infer which observed read
sequences are likely erroneous deviations from other, more abundant, "true"
sequences. In this way, denoisers can distinguish between similar sequences that are
likely to be truly biologically distinct, in ways that 97% OTU calling cannot.

![Denoising algorithms like DADA2 correct the original sequencing data using
statistical error models. OTU calling, by contrast, simply groups similar
sequences. In this illustration, a denoiser can eliminate erroneous variants
(the small dots) while also distinguishing two similar sequences (red versus
green). OTU calling removes the erroneous sequences but at the cost of lumping
together meaningfully different sequences (red versus green, dark blue versus
light blue). Reproduced from Callahan *et al*.,
doi:10.1038/nmeth.3869](images/dada2.png)

The output of denoising algorithms are called *amplicon sequence variants*
(ASVs), which are estimates of the true sequences that were presented in the original DNA.
The potentially substantial reduction in numbers of unique sequences that comes from denoising,
combined with improved computing power,
means that, in many cases, calling OTUs is no longer a practical necessity.
However, because the OTU concept dominated 16S data processing for so long, it
is still common to say that an analysis uses "100% identity OTUs", which simply means
that each sequence or ASV was treated as its own OTU. In other words, "100% OTUs"
means that OTUs weren't called at all!

## Philosophical reasons for OTU calling

Although it is no longer stricly necessary to call OTUs, there are still
philosophical[^philo] and analytical for doing so, depending on your study's purpose. If you want to study
bacterial species and are a firm believer in the idea that a 97% cluster is the
best approximation of a species, then you'd want to organize your data into
those approximate-species and go from there.

More generally, you'll want to organize your sequences into some operational
unit (i.e., OTU) that works well with the kind of analysis you want to do.  For
example, to examine very broad broad changes in community composition, you
might want to call OTUs that are your best approximations of phyla. If you're
interested in what individual organisms are doing, you'll probably want to do
very little (if any) grouping of sequences into OTUs, since the unique
sequences are, in a sense, the best information you have about those organisms.

[^philo]: Jax (doi:10.1086/506237) reviews the different ways ecological units
  are viewed from ontological and functional perspectives.

Regardless of how you call OTUs, I think you should call them in a way that
doesn't throw away information that could be useful or interesting. Only throw
away information that you are sure you won't find interesting for *any*
downstream analysis. Clustering your sequences into a small number of OTUs can
make it easier to think about your data, but beware: you want those clusters to
be meaningful. You want them to be the called in the way that makes them most
useful for answering the question you want to answer.

## OTU-calling methods

There are multiple ways to group sequences into OTUs. Here I review the most
important ones, in the order I thought was easiest to explain.

### Amplicon sequence variants, or 100% identity OTUs

As discussed above, this approach, which was originally infeasible because of
computational and technical reasons, is becoming increasing popular. Lower
error rates from sequencers combined with sophisticated denoising algorithms
means that distinct amplicon sequence variants (ASVs), even ones that differ
from one another by only one nucleotide, may very well be biologically
distinct.

### *De novo* clustering

As the name suggests, *de novo* clustering means making your own OTUs from
scratch. There are many approaches to *de novo* clustering methods, but
they all follow the same basic principle:
they try to identify a set of OTUs that are at some maximum dissimilarity
relative to one another. (As you might guess, 97% OTUs are popular.) Every
OTU will be assigned a *representative sequence*, which is either one of the
OTU's member sequences or a composite sequence based on the members.

*De novo* clustering suffers from some insidious and very serious disadvantages.
First, *de novo* methods are more computationally expensive than other methods.
Second, it is becoming [increasingly clear](http://dx.doi.org/10.1186/s40168-015-0081-x)
that many methods produce *de novo*
OTUs that are not *stable*, meaning that small changes in the sequence data you
feed into the algorithm can lead to large changes in the number of OTUs, the
OTUs' representative sequences, and the assignment of reads to OTUs. Third, it
is difficult to incorporate new data into a dataset that has been processed
into *de novo* OTUs. It usually requires calling OTUs all over again. It's
also difficult to compare *de novo* OTUs across datasets: you and I might have
lots of the same sequences, but our *de novo* OTUs might differ.

The principle advantage of *de novo* clustering is that it won't throw out
abundant sequences from your data.

### Reference-based methods

In reference-based OTU calling, the OTUs' representative sequences are
specified ahead of time, and each sequence in your query dataset is assigned to
one of the sequences in the reference dataset based on their sequence
similarity.
Usually
these sequences are in a database like Greengenes, which was made by calling *de
novo* OTUs on some large set of data. Greengenes has been such a popular database
that I often heard "OTU" used to mean "the 97% OTUs in Greengenes", although
that usage is becoming less common as denoising becomes more popular.

The principle advantages of reference-based calling are:

- *Stability*. Similar inputs should produce similar outputs, since you're just
comparing to a fixed reference.
- *Comparability*. If you and I called our OTUs using the same reference, it's
easy for us to check if we have similar sequences in our datasets. We can even
combine our datasets in a snap.
- *Computational cheapness*. Unlike *de novo* OTU calling, reference-based
methods only need to hold one sequence in memory at a time, so they require
less RAM and are easy to parallelize.
- *Chimeras need not be slain*. If you're only keeping sequences that align to
some database, which has hopefully been pre-screened for chimeras, then you
don't need to worry about them yourself.

The major weakness of reference-based methods is insidious: if a sequence in
your query dataset doesn't match a sequence in the database, what do you do?
Frighteningly, many methods just throw it out without telling you. If you work
in the human gut microbiome, this might not bother you, since the gut is the
best-studied ecosystem and databases like Greengenes have heaps of gut data in
them. However, if you work in environmental microbiology or even in mice, many
of the sequences in your studied bacterial community might not be sufficiently
similar to a sequence in Greengenes to be assigned to a reference OTU.

Reference-based methods also suffer a converse problem: what if your sequence is
an equally good match to more than one database entry? This can happen in
amplicon sequencing: the Greengenes OTUs are the entire 16S gene (about 1400 bases), but you only
have a little chunk of it (say, 250 bases). The Greengenes OTUs are, say, 97% similar (i.e., 3%
dissimilar) across the *entire gene*, but they might be identical over the
stretch that aligns to your little chunk.

### Open-reference calling

The process I described about ---just throwing out non-matching sequences--- is
called  *closed-reference* calling. If you're interested in those non-matching
sequences, you could gather them up and group then into *de novo* clusters,
then combine your reference-based OTUs with your *de novo* OTUs.
This mix of reference-based and *de novo* is named *open-reference* calling.

### Taxonomy-based assignment

ASVs, 100% identity OTUs, and *de novo* OTUs can be hard to make sense of,
since they are essentially one or more strings of `ACGT`. Reference OTUs also
tend to have unilluminating names. For example, the Greengenes OTUs are labeled
with numbers. To help interpret the raw sequences, it's very common to do *taxonomy assignment* (or "lineage" assignment), which means determining a sequences domain, phylum, class, order, family, genus, and species.[^ranks]

[^ranks]: 16S rarely has sufficient resolution to identify species, and it often lacks information to determine placement at even higher levels. It is also worth noting that there are intermediate ranks (like subclass).

Taxonomy assignment requires comparing query sequences with a database of sequences that already have taxonomies associated with them. For example, the Greengenes database has taxonomies associated with all its OTU representative sequences.[^ggredux] Thus, reference-based OTUs called using the Greengenes database automatically have taxonomies assigned to them.

[^ggredux]: The last update of the Greengenes database was in 2013. Bioinformatic methods have evolved since then, and the quality of the taxonomy assignments in the database is open to question. Cf., e.g., Yokono, Satoh, Tanaka (doi:10.1038/s41598-018-25090-8).

Another popular method for taxonomy assignment is the
Ribosomal Database Project's (RDP) naive Bayesian classifier[^nbc]
Rather than
comparing a sequence to existing OTUs, the RDP classifier breaks up the sequence
into *k*-mers (all subsequences of the original sequence that have length *k*)
and compares the *k*-mer content of that sequence to a big database that knows
how *k*-mer content relates to taxonomy. The practical advantage to this is that
RDP gives *confidences* to each level of the taxonomic assignment. For example,
a sequence might definitely be from some phylum (99%), but it might be difficult
to specify its class (80%) and nearly impossible to identify its order (30%). In
contrast, using the Greengenes approach, the same sequence might happen to hit
an OTU that is classified all the way down to the species, and you would mistakenly
think that your sequence had a lot of taxonomic information in it.

[^nbc]: Wang *et al*. (doi:10.1128/AEM.00062-07)

Regardless of how taxonomy assignment is performed, it is important to remember that it is a distinct process from OTU calling. One can call OTUs without assigning taxonomies, or one can actually call OTUs by grouping sequences that are all assigned to the same taxonomic rank, for example, all sequences in the same phylum. Whether grouping sequences and doing analyses by taxonomic groupings constitutes re-calling OTUs is a question of semantics.

### Distribution-based methods

All the algorithms mentioned only look at the list of unique sequences; they
mostly don't take notice of how those sequences are distributed among the
samples. Preheim *et al*. (doi:10.1128/AEM.00342-13) showed that you get OTUs
that better reflect the composition of a known, mock community if you take the
sequence provienances into account. If an abundant sequence and a
sequence-similar, rare sequence are distributed the same way across samples,
the rare sequence is probably sequencing error and should be put in the same
OTU with the abundant one. Conversely, if two very similar sequence are never
found together, they probably represent ecologically-distinguishable bacteria,
so they should be kept in separate OTUs. This approach is called
*ecologically-based* (or "distribution-based") OTU calling, but it is
essentially also a form of ecologically-informed denoising.

![Distribution-based OTU calling separates similar sequences if they are distributed differently across samples. Adapted from Preheim *et al.*](images/dbc.png)

## How many OTUs?

A pet peeve of mine is when someone asks "how many OTUs" were in some sample.
That number, on its own, means very little; it matters how the OTUs were
called. Asking "how many OTUs" is like asking how many kinds of books I read
last year.  Do I answer 2, fiction and nonfiction? Or do I put each book into
its own category, because each one had its own author?
