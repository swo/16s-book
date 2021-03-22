# Foreword

## Where this document came from

I wrote an early form of this document as a teaching aid for a workshop on 16S
rRNA data processing that I gave as a graduate student for my research group,
the Alm Lab at MIT. I finished my PhD in 2016. In 2018, I put this document up
for the larger world because it was starting to be shared in wider circles.
Now, in 2021, I'm updating this document to reflect two important new
developments: denoising and QIIME 2.

## What this document is for

My goal for this document is to help you understand the theory behind 16S data
processing. I want you to be able to do the analysis that makes the most sense
for you. Processing 16S data involves a lot of very small decisions (that probably
have a small effect on your results) and a few big decisions (that certainly have
a big effect on your results). The nice pipelines make it possible for you to shut your
eyes to these complications. In contrast, I want to empower you to be able to
critique and doubt other people's methods. That's part of how science advances!

## Who this document is for

This document should be a fun read for advanced undergraduates, graduate
students, and postdocs who are interested in getting down and dirty with 16S
data. I expect you to already know that you want to use 16S data or you
already have 16S data in hand and are trying to figure out what to make of
it.

If you know too much, I expect this document will annoy you, because you
will recognize its shortcomings.

## What this document is not

This document is not perfect. It is full of my own ignorance, ideas, and
opinions. Take it with a grain of salt.

This document is also not intended to be a literature review. Next-generation
sequencing for microbial ecology
is a large field, and here I just scratch the surface.
Some specific methods are included and they show my biases: I'm more
familiar with my lab's work and with the way my colleagues and I process our data.

This document is not a tutorial. If you desperately need to turn some raw
data into OTU tables in the next 10 hours, don't read this document. If you
want to know something more principled about *how* to turn fastq's into
OTU tables, read on.
