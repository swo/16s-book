# Foreword

## Where this document came from

I wrote an early form of this document as a teaching aid for a workshop on 16S data processing that I gave for my research group, the Alm Lab at MIT. I eventually put this document up for the larger world because it was starting to be shared in wider circles.

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

This document is not perfect. It is full of my own igorance, ideas, and opinions. Take it with a grain of salt. If you find errors, blame me and not my adviser or the other members of my lab. And do point them out to me!

This document is also not intended to be a literature review. Next-generation
sequencing for microbial ecology
is an enormous field, and here I just scratch the surface of
that field. Some specific methods are included and they show my biases: I'm more
familiar with my lab's work and with the way my labmates and I process our data.

This document is not a tutorial. If you desperately need to turn some raw
data into OTU tables in the next 10 hours, don't read this document. If you
wat to know something more principled about *how* to turn fastqs into
OTU tables, read on.
