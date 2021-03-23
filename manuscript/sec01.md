# Foreword

## Where this document came from

I wrote the first edition of this document as a graduate student for use by my
research group, the Alm Lab at MIT. In 2018, I published the second edition online.
Now, in 2021, I'm
updating this document with a third edition in order to reorganize the material
and to include two important new developments: denoising and QIIME 2. I'm
grateful to OpenBiome, which gave me the opportunity to do this revision as
part of a microbiome science seminar course for Aga Khan University.

## What this document is for

My goal for this document is to help you understand the theory behind 16S data
processing.
Processing 16S data involves a lot of very small decisions (that probably
have a small effect on your results) and a few big decisions (that certainly have
a big effect on your results). The nice pipelines make it possible for you to shut your
eyes to these complications. In contrast, I want to empower you to be able to
critique and doubt other people's methods.

## What this document is not

This document is not perfect. It is full of my own ignorance, ideas, and
opinions. Take it with a grain of salt.

This document is not a literature review. Next-generation
sequencing for microbial ecology
is a large field, and here I just scratch the surface.

This document is not a tutorial. If you desperately need to turn some raw
data into OTU tables in the next 10 hours, don't read this document. If you
want to know something more principled about *how* to turn fastq's into
OTU tables, read on.
