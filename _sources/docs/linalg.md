# Linear Algebra

This article assumes background in set theory and abstract algebra.

An algebraic structure consists of an arbitrary **set** with certain _operations_ defined on that set. An **operation** is a rule or a way of combining any two members of the set to produce a unique third member of the set.

This articles discusses concepts from **linear algebra**, the study of vector spaces, an algebraic structure consisting of fields and its operations.

## Vector Spaces

Formally, the definition of a vector space is given below:

```{admonition} Definition
A **vector space** is a set **V** along with an **addition** on **V** and a **scalar multiplication** on **V** such that the following properties hold:

- commutativity
- associativity
- additive identity
- additive inverse
- multiplicative identity
- distributive properties
```

## Finite-Dimensional Vector Spaces

span
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
