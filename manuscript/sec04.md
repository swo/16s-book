```
*Operational taxonomic units* (OTUs) were once the fundamental unit used
in 16S data analysis. In most data processing pipelines, OTUs and their
abundances in the samples were the output.

OTU-calling methods are (to my eyes) surprisingly diverse, and the choice of
method can have a huge impact on the the results of your analysis. Any
OTU-based information, plot, or analysis must be interpreted in the
context of how those OTUs were called.

A pet peeve of mine is when someone asks "how many OTUs" were in some sample.
That number, on its own, means very little. It matters how the OTUs were called.
Asking "how many OTUs" is like asking how many kinds of board games there are. The answer
depends on how you define "kinds".
```

# Denoising and OTU calling

## An abridged history of the OTU

In the 1980s, Carl Woese showed that the 16S gene could be used as a molecular
clock. Using 16S data, he [re-drew](http://dx.doi.org/10.1073/pnas.87.12.4576)
the tree of life, breaking up the older
Monera[^monera] into Bacteria and Archaea, showing that Eukaryotes and Archaea are closer
cousins than are Archaea and Bacteria. The 16S gene was therefore a promising
practical candidate for distinguishing bacterial *species*.[^known]

[^known]: In 1991, PCR-amplified portions of the 16S gene were used to identify known species. The paper has a prescient final sentence: "While this [i.e., PCR] should not be a routine substitute for growing bacteria, picking individual colonies, and confirming their phenotypic and biochemical identities, it will enable experiments to be performed that were not previously possible." ([Weisburg *et al.*](http://jb.asm.org/content/173/2/697.short), *J Bacteriol* **173** [1991])

[^monera]: I'm shocked that, attending public high school in the early 2000s, we were *still* taught about Monera and Protista rather than about Bacteria, Archaea, and Eukaryotes.

The species concept is easy to define for sexual macroorganisms: two
living things of opposite sex are in the same species if they can produce
fertile offspring together. Bacteria don't have sex, but they do perform
homologous recombination. Homologous recombination requires some sequence
similarity, so it [came about that](http://dx.doi.org/10.1098/rstb.2006.1920)
a common definition of a bacterial species was all
those strains whose isolated DNA was 70% DNA-DNA-hybridization similar.[^concept]

[^concept]: There is still a large debate about the microbial species "concept".

In the 1990s, people sequenced the 16S genes of the strains grouped into species
by the hybridization assay. It emerged as a rule of thumb that two bacteria were
the same species if their 16S genes had 97% nucleotide identity.

Because of this history, a lot of discussion around OTUs involves finding 97%
clusters, and "OTU" was often used as a shorthand for "97% clusters". To my
ears, the word "operational" in OTU means that an OTU is whatever group of
reads you choose to be the unit of analysis in your downstream work.[^minded]

[^minded]: This nomenclature is not universally accepted. For example, some people use "phylotype" to mean a group of sequences that was grouped together because of their similarity to a database sequence and reserve "OTU" for a group of sequences that was made by comparing sequences in a dataset against one another. This also means that I call [oligotyping](http://dx.doi.org/10.1111/2041-210X.12114) (doi:10.1111/2041-210X.12114), which is breaks your OTUs down into finer units, just another kind of OTU-calling.

## Denoising

Historically, people called OTUs because for a few reasons. A first and very
practical reason was data reduction. Dereplication can give you hundreds of
thousands of unique sequences, and doing analysis with hundreds of thousands of
unique units was computationally infeasible in the early days of 16S
sequencing.

A second important but still technical reason was denoising. Imperfect
technology means that one can never really be sure whether two reads have
different sequences because of technological error or because those two reads
arose from biologically different sequences in different bacteria. One way to
denoise data was to say that we couldn't really trust our equipment to be able
to distinguish sequences that were less than about 97% similar anyway, so we
might as well lump those sequences into one unit for analysis.

To give a sense of what denoising is about, consider this hypothetical example.
Say you are sequencing an amplicon that has only 10 nucleotides, and the
sequencer has an error rate of 1%, meaning that each base pair has an
independent, 1% chance of being misreported. This means that there is a
$(0.99)^10 = 90\%$ chance that all 10 nucleotides will be correctly reported, a
$(0.01) \times (0.99)^9 = 9.1\%$ chance that all but one base pairs will be
corretly reported, and an approximately 1% chance that there will be two or
more errors in any particular read.

In this example, if there was only one true sequence in the biological sample,
then we would expect 90% of reads to be that true sequence, while the remainder
would be split among the various erroroneous sequences. For example, of the
9.1% of reads, one in ten (i.e., 0.91% of the total reads) would have an error
in the first base pair, of which about one-third (i.e., 0.3% of the total reads)
would have each of the incorrect base pairs in it.

Percent of reads | Read sequence
--- | ---
90.4% | GACAGGTACA
0.3% | ***A***ACAGGTACA
0.3% | ***C***ACAGGTACA
0.3% | ***T***ACAGGTACA
0.3% | G***C***CAGGTACA
0.3% | G***G***CAGGTACA
0.3% | G***T***CAGGTACA
... | ...

On the other hand, if one of these sequences that could be explained as error
was more frequent than was expected given the statistical model for errors,
then we would conclude it is also a real, biological sequence. For example, if
the sequence `***A***ACAGGTACA` appeared as often as the original sequence
GACAGGTACA, then we would expect that they are both meaningful. However, our
ability to distinguish real biological variations from technological error is
limited by the abundance of these potentially erroneous sequences and the
sequencer error rate: if the error rate is high or the true variant sequence is
rare, we will not be able to determine that it is *not* simply an erroneous
read.

Denoisers look through the read sequences and how common they are to infer the
sequencer's error rate and, using that error rate, which observed read
sequences are likely erroneous deviations from other, more abundant, "true"
sequences. In this way, they can distinguish between similar sequences that are
likely to be truly biologically distinct, in a way that 97% OTU calling would
be unable to do.

![Algorithms like DADA2 take the opposite approach to denoising, compared to OTU calling. Rather than grouping related sequences in the hopes that they are erroneous variants of one another, explicity denoising algorithms correct the original errors using statistical error models. Reproduced from Callahan *et al*., doi:10.1038/nmeth.3869](images/dada2.png)

The output of denoising algorithms are called *amplicon sequence variants*
(ASVs). The combination of improved computing power and the potentially
substantial reduction in numbers of unique sequences that comes from denoising
means that, in many cases, calling OTUs is no longer a practical necessity.
However, because the OTU concept dominated 16S data processing for so long, it
is still common to say that an analysis uses "100% OTUs", which simply means
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

[^philo]: There is a [fun review](http://www.jstor.org/stable/10.1086/506237) (jstor:10.1086/506237) of the different ways ecological units are viewed from ontological and functional perspectives.

Regardless of how you call OTUs, I think you should call them in a way that
doesn't throw away information that could be useful or interesting. Only throw
away information that you are sure you won't find interesting for *any*
downstream analysis. Clustering your sequences into a small number of OTUs can
make it easier to think about your data, but beware: you want those clusters to
be meaningful. You want them to be the called in the way that makes them most
useful for answering the question you want to answer.

## OTU calling is not the same as lineage assignment

*Calling* OTUs means assigning your unique 16S sequences to OTUs. Often, each OTU has a
sequence associated with it. If an OTU's
sequence is the same as one of its members, that member is called the
*representative sequence*.

Often the OTU sequence itself is not very interesting. It's just a string of
letters. We'd rather know "who" that sequence is. A common way to get this
information is to assign *lineages* (or "taxonomies") to each OTU. A lineage is
usually an assignment of that sequence to the taxonomic *ranks:* kingdom (or
"domain"), phylum, class, order, family, genus, and species.[^ranks]

[^ranks]: Weird stuff can happen here: there are other ranks like subclass, and sometimes a sequence could, say, get assigned to a genus but not a class. (This is the difference between the two types of RDP classifier output: `allrank` and `fixrank`.)

Confusingly, in some cases, OTUs are in fact called using lineage assignments.
It's useful to keep these two concepts separate. For example, it's common to
call OTUs in some way, then assign lineages to OTUs, then do a second round of
OTU calling in which you merge OTUs that have the same lineage. Now the OTUs are
labelled by the lineages. This is how the ubiquitous taxa plots are made.

## OTU-calling methods

This is a survey of OTU-calling methods that are out there in the literature. This list is not exhaustive. The methods are listed are in the order I thought was easiest to explain.

### Amplicon sequence variants, or 100% identity OTUs

As discussed above, this approach, which was originally infeasible because of
computational and technical reasons, is becoming increasing popular. Lower
error rates from sequencers combined with sophisticated denoising algorithms
means that distinct amplicon sequence variants (ASVs), even ones that differ
from one another by only one nucleotide, may very well be biologically
distinct.

### *De novo* clustering

As the name suggests, *de novo* clustering means making your own OTUs from
scratch. There is an enormous diversity of *de novo* clustering methods, but
they all follow the same basic principle:
they try to identify a set of OTUs that are at some
"distance" from one another. (As you might guess, 97% OTUs are popular.) In some
cases, the OTU's representative sequence will be the sequence of its most
abundant member; in other cases, the OTU's representative sequence is some
mish-mash of its member sequences.

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
lots of the same sequences but our OTUs might differ.

The principle advantage of *de novo* clustering is that it won't throw out abundant sequences from your data. Why would that happen? Read on!

### Reference-based methods

In reference-based OTU calling, the OTUs are specified ahead of time. Usually
these OTUs are in a database like Greengenes, which was made by calling *de
novo* OTUs on some large set of data. Greengenes is such a popular database
that I often heard "OTU" used to mean "the 97% OTUs in Greengenes", although
that usage is becoming less common as denoising becomes more popular.

The principle advantages of reference-based calling are:

- *Stability*. Similar inputs should produce similar outputs, since you're just
comparing to a fixed reference.
- *Comparability*. If you and I called our OTUs using the same reference, it's
easy for us to check if we have similar sequences in our datasets. We can even
combine our datasets in a snap.
- *Computational cheapness*. Unlike *de novo* OTU calling, reference-based
methods only need to hold one sequence in memory at a time. This makes them
cheap (in terms of memory) and embarrassingly parallelizable[^embarr].
- *Chimeras need not be slain*. If you're only keeping sequences that align to
some database, which has hopefully been pre-screened for chimeras, then you
don't need to worry about them yourself.

[^embarr]: I didn't make that up; it's a real computer science term.

The major weakness of reference-based methods are insidious:
if a sequence in your query dataset doesn't match a sequence in the database, what do
you do? Frighteningly, many methods just throw it out without telling you. If
you work in the human gut microbiome, this might not bother you, since the gut
is the best-studied ecosystem and databases like Greengenes have heaps of gut
data baked into them. If you work in environmental microbiology or even in
mice, however, many of your sequences might not hit Greengenes.

Reference-based methods also suffer a converse problem: what if your sequence is
an equally good match to more than one database entry? This can happen in
amplicon sequencing: the Greengenes OTUs are the entire 16S gene (about 1400 bases), but you only
have a little chunk of it (say, 250 bases). The Greengenes OTUs are, say, 97% similar (i.e., 3%
dissimilar) across the *entire gene*, but they might be identical over the
stretch that aligns to your little chunk.

[USEARCH](http://www.drive5.com/usearch/), a popular algorithm[^usearch] for matching
sequences to a database (and one of QIIME's tool for reference-based OTU calling).
Because USEARCH is so popular and because it can have unexpected effects, I will
devote some space in the next chapter to discussing its workings.

[^usearch]: Confusingly, USEARCH is the name of an alignment algorithm and `usearch` is the name of the program that does USEARCH, UPARSE, and other stuff.

### Open-reference calling

The process I described about ---just throwing out non-matching sequences--- is
called  *closed-reference* calling. If you're interested in those non-matching
sequences, you could gather them up and group then into *de novo* clusters,
then combine your reference-based OTUs with your *de novo* OTUs.
This mix of reference-based and *de novo* is named *open-reference* calling.

### Lineage-based assignments

Reference OTUs tend to have unsatisfying names. For example, the Greengenes OTUs are labeled with numbers. It's common (but not necessarily good) practice to do a second round of OTU calling: the new OTUs are made by combining the old OTUs that have the same lineage.

How does this work? Greengenes associates a taxonomy with each of its OTUs.
This is relatively easy for sequences that came from isolates:
give that OTU the classification you would have given the
isolate. It gets more tricky for OTUs that aren't just taken from isolates: it
requires some sort of phylogenetic inference. This means that you construct a
tree of all your sequences, figure out where the taxonomic clades are, and
assign taxonomies to OTUs based on what you found.

Someone at Greengenes has done all the hard work of assigning taxonomies to their
reference OTUs, but I want to make it clear
that this is not a foolproof process. All lineage assignments should be treated
with a healthy skepticism.

The most popular alternative to Greengenes for lineage assignments is the
[Ribosomal Database Project](https://rdp.cme.msu.edu/) (RDP)
[Naive Bayesian Classifier](http://dx.doi.org/10.1128/AEM.00062-07). Rather than
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

### Distribution-based methods

All the algorithms mentioned only look at the list of unique sequences; they
don't take any notice of how those sequences are distributed among the samples.[^abund]
Some [Alm Lab work](http://dx.doi.org/10.1128/AEM.00342-13) has shown that you
get more accurate OTUs (i.e., OTUs that
better reflect the composition of a known, mock community) if you take the
sequence provenances into account. If an abundant sequence and a
sequence-similar, rare sequence are distributed the same way across samples, the
rare sequence is probably sequencing error and should be put in the same OTU
with the abundant one. Conversely, if two very similar sequence are never found
together, they probably represent ecologically-distinguishable bacteria, so they
should be kept in separate OTUs. This approach is confusingly called
*distribution-based* OTU calling or, less confusingly, *ecologically-based* OTU
calling.

[^abund]: This isn't stricly true: some *de novo* methods will take into account
the abundance of a sequence in the entire dataset and will treat more abundant
sequences differently from less abundant ones. As far as I know, however, the
algorithm described here is the only one that accounts for differences in the
distribution of each sequence across samples.

![Distribution-based OTU calling separates similar sequences if they are distributed differently across samples. Adapted from Preheim *et al.*](images/dbc.png)
