

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
