# DC Power Flow

>Version: 0.0.1  
>Author: itaoxiaoran  
>E-mail: ta0ran@163.com  

>**Before read**
>If you cannot see the LaTex formula normally as following:
>$$
>\frac{d c}{d x}+\mu \frac{d h}{d x}=0
>$$
>You'd better install the Chrome plugin: [MathJax Plugin for Github](https://chrome.google.com/webstore/detail/mathjax-plugin-for-github/ioemnmodlmafdkllaclgeombjnmnbima/related) to view the formula.
>



View more solutions of **Power System Optimization**, you can [skip to](https://github.com/itaoxiaoran/power-system-optimization) my another repository.

## Contents

- [Introduction](#introduction)  
- [DC Power Flow Model](#dc-power-flow-model)  
- [How to Use this Code  ](#how-to-use-this-code)  
- [Example](#example)  
- [Code List](#code-list)
- [Module Required](#module-required)  

## Introduction

DC power flow model is a kind of imprecise power flow model, which is widely used in power system, especially in power system planning and contingency analysis. 

When you do not care the reactive power or voltage amplitude, the <u>DC Power Flow Model</u> will match your needs.

this project can help you calculating DC power flow in Python.

## DC Power Flow Model

> **if you are familiar with the DC Power Flow Model, you can skip this section**.

In DC Power Flow Model, nonlinear model of the AC system is simplified to a linear form through these assumptions:  

• Line resistances (active power losses) are negligible i.e. $R<<X$ .  
• Voltage angle differences are assumed to be small i.e. $sin(\theta) = \theta$ and
$cos(\theta)=1$.  
• Magnitudes of bus voltages are set to 1.0 per unit (flat voltage profile).  
• Tap settings are ignored.   

Based on the above assumptions, voltage angles and active power injections are
the variables of DC Power Flow. Active power injections are known in advance. Therefore
for each bus $i$ in the system is converted to
$$
P_{i}=\sum_{j=1}^{N} B_{i j}\left(\theta_{i}-\theta_{j}\right)
$$
in which $B_{ij}$ is the reciprocal of the reactance between bus $i$ and bus $j$. As
mentioned earlier, $B_{ij}$ is the imaginary part of $Y_{ij}$.
As a result, active power flow through transmission line $i$, between buses s and
$r$, can be calculated from.
$$
P_{L i}=\frac{1}{X_{L i}}\left(\theta_{s}-\theta_{r}\right)
$$
where $X_{Li}$ is the reactance of line $i$.

DC power flow equations in the matrix form and the corresponding matrix relation for flows through branches are represented as following:
$$
\begin{aligned}
&\theta=[\mathbf{B}]^{-1} \mathbf{P}\\
&\mathbf{P}_{\mathbf{I}}=(\mathbf{b} \times \mathbf{A}) \theta
\end{aligned}
$$
where

|                | Descriptions                                                 |
| -------------- | :----------------------------------------------------------- |
| $\mathbf{P}$   | $N \times 1$ vector of bus active power injections for buses $1, …, N$ |
| $\mathbf{B}$   | $N \times N$ admittance matrix with $R = 0$                  |
| $\theta$       | $N \times 1$ vector of bus voltage angles for buses $1, …, N$ |
| $\mathbf{P_L}$ | $M \times 1$ vector of branch flows ($M$ is the number of branches) |
| $\mathbf{b}$   | $M \times M$ matrix ($b_{kk}$ is equal to the susceptance of line $k$ and non-diagonal elements are zero) |
| $\mathbf{A}$   | $M \times N$ bus-branch incidence matrix                     |

Each diagonal element of $B$ (i.e. $B_{ii}$) is the sum of the reciprocal of the lines reactances connected to bus $i$. The off-diagonal element (i.e. $B_{ij}$) is the negative sum of the reciprocal of the lines reactances between bus $i$ and bus $j$. 

$\mathbf{A}$ is a connection matrix in which $a_{ij}$ is 1, if a line exists from bus $i$ to bus $j$; otherwise zero. Moreover, for the starting and the ending buses, the elements are 1 and -1, respectively.

Reference: More details read [this](https://link.springer.com/content/pdf/bbm%3A978-3-642-17989-1%2F1.pdf). (Actually, I just copy this PDF document.)

## How to Use this Code

First, you should clone the repository

if you don't have the case file, my repository: [**Transferring Matpower Case File to CSV Format**](https://github.com/itaoxiaoran/transfer-matpower-case-file) can help you transferring or download some case file, directly.

the output of dcpf.py is **f, t, F, Va** mean **fbus, tbus, branch flow and voltage angle(degrees)**, respectively.

## Code List

[getDataFrame.py](/getDataFrame.py) - you can read more details about this programming in my another repository: click [here](https://github.com/itaoxiaoran/transfer-matpower-case-file).

[dcpf.py](/dcpf.py) - can help you to calculate DC Power Flow. This Python file is slightly different from the previous section: [DC Power Flow Model](#dc-power-flow), but all roads lead to Rome. If you just want to calculating the DC power flow, I don't think you need to pay attention to how I achieve it.

## Example

Let the **caseName = case5**, **and write = 1**

run the dcpf.py, and you will see the results in your Python Console

![](/img/dcpf_results.png)

## Module Required

numpy, scipy, pandas, prettytable (if you want to output results in pretty way like the [Example](#example) in this page)