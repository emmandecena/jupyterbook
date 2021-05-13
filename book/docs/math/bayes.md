# Probability Theory

Working with these files can be a challenge, especially given their heterogeneous nature. Some preprocessing is required before they are ready for consumption by your CNN.

Fortunately, I participated in the LUNA16 competition as part of a university course on computer aided diagnosis, so I have some experience working with these files. At this moment we top the leaderboard there :)

**This article demonstrates aims to provide a comprehensive overview of useful steps to take before the data hits your ConvNet/other ML method.**

What we will cover:

1. Pre-processing: and adding missing metadata
2. Exploratory Data Analysis: and what tissue these unit values correspond to
3. Resampling to an isomorphic resolution to remove variance in scanner resolution.



Here we write Ω for the sample space of all possible outcomes of an experiment. Ω can be a set
containing anything (numbers, objects, colours etc.). An event is a subset of Ω. A probability
measure is a real-valued function Pr defined on 2Ω (this is a power set, the set of all subsets of
Ω), satisfying the following axioms


$$
  \int_0^\infty \frac{x^3}{e^x-1}\,dx = \frac{\pi^4}{15}
$$ (label3)

A link to an equation directive: {eq}`my_label`

A link to an equation directive: {eq}`label3`


```{math}
:label: my_label
w_{t+1} = (1 + r_{t+1}) s(w_t) + y_{t+1}
```

---

## Bibliography

```{bibliography} ../_bibliography/references.bib
:filter: docname in docnames
:style: plain
```
