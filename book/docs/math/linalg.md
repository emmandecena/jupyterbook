# Linear Algebra

Linear Algebra is perhaps the _most important_ branch of mathematics to learn because of its applications in several engineering disciplines.

**This article assumes some background in abstract algebra and set theory**

```{image} ../../images/620by500.jpg
:alt: ID
:class: bg-primary mb-1
:align: center
```

## What is an algebra?

**Algebra** is the study of mathematical **objects** and the **rules** to manipulate those objects.
- An **algebraic structure** consists of an arbitrary **set** with certain **operations** defined on that set.
- An **operation** is a rule or a way of combining any two members of the set to produce a unique third member of the set.

**Linear algebra** is the study of **vector spaces** -- an algebraic structure consisting of **fields** and its **operations**.

## Vector Spaces

First, we define a vector space -- the primary mathematical structure that we will be studying.

```{admonition} Definition
A **vector space** is a set **V** along with an **addition** on **V** and a **scalar multiplication** on **V** such that the following properties hold:

- commutativity
- associativity
- additive identity
- additive inverse
- multiplicative identity
- distributive properties
```

**We take a look of some examples of sets and operations that fit the definition of vector spaces.**

1. The set of Real Numbers $\mathbb{R}$

Let $a, b \in \mathbb{R}$.

2. The set of Complex Numbers

denoted by  $\mathbb{F}^{2}$

3. The set of n-tuples of real numbers

denoted by $\mathbb{F}^{n}$


## Finite-Dimensional Vector Spaces

```{admonition} Definition
The **span** of a vector space
```

linear independence
bases
dimension

## Linear Maps

### Matrices

```{admonition} Definition
An **m-by-n matrix** is a rectangular array of elements of the field $F$ with $m$ rows and $n$ columns:

```{math}
:label: matrix
\begin{bmatrix} A_{1,1} & \ldots & A_{1,n} \\ \vdots &  & \vdots \\ A_{m,1} & \ldots & A_{m,n} \end{bmatrix}
```

### Matrix of a Linear Map

```{admonition} Definition
Given a linear map $T \in \mathcal{L} \left( V, W \right)$ where $v_{1},\ldots,v_{n}$ is a basis of $V$ and $w_{1}, \ldots ,v_{m}$ is a basis of $W$, then the **matrix of T** consists of the scalars $A_{1,k}, \ldots  ,A_{m,k}$ needed to write the $k$th basis of $V$ as a linear combination of the basis vectors in $W$.
```{math}
:label: matrixoflinearmap
Tv_{k} = A_{1,k}w_{1} + \ldots + A_{m,k}w_{m}
```

#### Example
Suppose $T \in \mathcal{L}(\mathbf{F^{2},F^{3}}) $ is defined by:

$$
T(x, y) = (x+2y, 3x+4y, 5x+6y)
$$

This is a linear map that takes a 2-dimensional vector $v \in V$ into 3-dimensional space $w \in W$. The basis vectors of $V$ are $ \left[ \begin{smallmatrix} 1 \\ 0 \end{smallmatrix} \right] $ and $ \left[ \begin{smallmatrix} 0 \\ 1 \end{smallmatrix} \right] $ while basis vectors of $W$ are $ \left[ \begin{smallmatrix} 1 \\ 0 \\ 0 \end{smallmatrix} \right] $ , $ \left[ \begin{smallmatrix} 0 \\ 1 \\ 0\end{smallmatrix} \right] $ and $ \left[ \begin{smallmatrix} 0 \\ 0 \\ 1\end{smallmatrix} \right] $.

Applying the map to the first basis vector in $V:$

$$
T(1, 0) = (1+0, 3+0, 5+0)
$$

Which can be written as a **linear combination** of the basis vectors in $W$:

$$
T\left[ \begin{smallmatrix} 1 \\ 0 \end{smallmatrix} \right] = 1\left[ \begin{smallmatrix} 1 \\ 0 \\ 0\end{smallmatrix} \right] + 3\left[ \begin{smallmatrix} 0 \\ 1 \\ 0\end{smallmatrix} \right] + 5\left[ \begin{smallmatrix} 0 \\ 0 \\ 1\end{smallmatrix} \right]
$$

Thus the matrix of this linear map $T$ is:

$$
\mathcal{M}(T) = \begin{bmatrix} 1 & 2 \\ 3 & 4 \\ 5 & 6\end{bmatrix}
$$

A link to an equation directive: {eq}`matrixoflinearmap`

---

## Bibliography

```{bibliography} ../_bibliography/references.bib
:filter: docname in docnames
:style: plain
```
