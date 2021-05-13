# Workflow

This section illustrates my typical workflow in an analytics project. We refer to figure {numref}`workflow` which focuses on the tools and techniques in data science {cite}`wickham2016r`. We assume that we have completely defined our problem statement beforehand.

```{figure} ../images/workflow.png
:name: workflow

Project workflow
```

The first step, **Import**, falls under the domain of Data Engineering. Data in the real world does not come in tidy little csv files. Instead, it comes in messy, incomplete, and from various sources that sometimes require developing a separate infrastructure to import.

The next steps, **Transform**, **Visualize**, and **Model**, are the main processes and are iterative. We begin by transforming the data: selecting, mutating, filtering, interpolating, etc, to gain better insight into its structure.

We visualize the results, looking at different dimensions to uncover patterns and find correlations. We then develop models that attempt to emulate the system behavior and do tests to see if our hypothesis about the relationships between variables hold.

Domain knowledge and experience play a key role in choosing the modeling and visualization techniques suitable for the data.

Finally, through **Report** we provide the stakeholders with the results of the analysis for decision-making. To do this, we develop communication tools such as beautiful reports, online dashboards, and full-on applications that present the data with fresh insights.


## Bibliography

```{bibliography} ../_bibliography/references.bib
:filter: docname in docnames
:style: plain
```
