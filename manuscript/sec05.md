# Using QIIME 2

In previous versions of this primer, I essentially encouraged readers to
develop their own scripts for 16S data processing. I did this in part because
the two, most user-friendly pipelines at the time, QIIME 1 and mothur, had
characteristics that left me very unsatisfied. The field was also younger, and
the methodology was more in flux, so it seemed wiser to get closer to the nuts
and bolts of things. Now, however, I enthusiastically recommend using QIIME 2
for 16S data processing.[^why]

[^why]: The two important changes for me were the plugin system and advances in
  virtualization software and virtual environment management.

QIIME 2 has extensive and ever-improving online documentation. Rather than
repeat that material here, I will emphasize a few important points about
working with QIIME 2.

## Key concepts in QIIME 2

### QIIME 2 consists of plugins

The QIIME 2 documentation describes it as a "decentralized microbiome analysis
package". It is a collection of individual tools, called *plugins*, with common
interfaces. For example, there is a plugin called *quality-filter* that has a
"method" *q-score* that filters 16S sequences in a fastq file based on quality
scores. Another plugin *vsearch* has a method *cluster-features-de-novo* that
does *de novo* OTU clustering. Every step in the 16S analysis process maps onto
a method in one of the QIIME 2 plugins.

### QIIME 2 packages data in artifacts

QIIME 2 methods do not run on human-readable data files like fastq's and
fasta's. Instead, those human-readable files need to be *imported* into QIIME 2
*artifacts*. This importing process compresses the original data and also adds
some helpful metadata, called a *provenance*, which tracks the history of what
methods have been run on a set of data.[^prov2] If you want to directly interact
with the data at any step in a QIIME 2 analysis, you will need to export it
out of the artifact form.

[^prov2]: In the art world, *provenance* refers to the history of custody and
  ownership of a work of art. A reliable provenance is an important part of how
  you determine if a work of art is authentic.

### QIIME 2 runs in compartmentalized computing environments

A challenge with a complex software project with QIIME 2 is that its software
dependencies can conflict with other software dependencies. QIIME 2 avoids
these problems using the modern solution, which is to use a compartmentalized
environment, either a virtual environment (via `conda` or a similar tool) or a
virtual machine (such as Docker). As a user, this may introduce a greater
learning curve to figure out how to initially install the software, but it will
reduce downstream problems.

## QIIME 2 still relies underlying algorithms and your parameter choices

The plugin concept means that QIIME 2's underlying algorithms are fairly
transparent. This does not mean, however, that everything that nothing that
QIIME 2 does will be surprising or, to put it bluntly, bad. QIIME 2 is only as
good as its underlying algorithms and the appropriateness of the parameters you
supply it.

For example, most pipeline software, QIIME 2 included, will allow many
parameters to have default values. In many cases, these values will be
appropriate for your data. In others, they may lead to very different results.
The onus is on you as a researcher to understand the merit of the parameter
values you selected, even if you selected the default ones.

As a second example, some of the methods in QIIME 2 rely on the USEARCH
algorithm[^edgar] to match query sequences to database sequences, such as when
performing reference-based OTU calling. At the risk of making a mountain of a
molehill, I dive a bit into this example, to demonstrate the complexity that
can underlie QIIME 2's pleasant user interface.

[^edgar]: Edgar (doi:10.1093/bioinformatics/btq461)

Critically, USEARCH is a *heuristic* algorithm. This means that it applies
shortcuts to achieve faster speed:

1. Search for a match according to a decreasing expected sequence similarity.
2. Use heuristics to speed up the sequence alignments.
3. Apply stopping criteria. The default is to stop after a single hit that meets the accepting criteria.

The first rule means that your query sequence will be compared to database
sequences according to some order; the third rule means that the first of these
database sequences that is a sufficiently good match to your query will be
delivered as the result. For example, if you are assigning your OTUs by making
a search to the 97% OTUs in Greengenes, then the first database sequence that
is at least 97% similar to your query will be considered its parent OTU.

This would be of no concern if the comparisons were performed in the order of
decreasing sequence similarity. Then the first hit would be the best one.
This, however, puts the cart before the horse: you need to somehow *guess*
which sequence will be the best match before actually performing the alignment.

USEARCH guesses the sequence similarity between two sequences using the *U*
value (which is the U in USEARCH). *U* is the number of unique *words* shared
by two sequences. You get these words by looking for length *w* (default is 8)
subsequences starting at positions spaced $\mu$ apart. For example, if
$\mu = 1$, then your words are all the *w*-mers in the sequence. If
$\mu = w$, then your words are the first *w* nucleotides, the next *w*
nucleotides, and so forth. Conveniently, sensible values for $\mu$
are inferred using tables of optimal choices derived from running USEARCH
on databases of sequences using different values of the identity threshold.

This heuristic selection of database entries for comparison can lead to some
quirky results, which I described in detail elsewhere[^devil]. In short,
even reference-based OTU calling, which is expected to be stable and replicable,
does not necessarily produce the results you might *a priori* think it should.
The take-away is that a user-friendly interface cannot make the underlying
algorithms user-friendly. The cutting edge is often sharp.

[^devil]: Tsou *et al*. (doi:10.1080/19490976.2020.1747336)
