# Chapter 3: The simplest model with government money

Markdown file to demonstrate the FSIC model builder, using the example of Model
SIM from:

> Godley, W., Lavoie, M. (2007), *Monetary economics: an integrated approach to
> credit, money, income, production and wealth*, Palgrave Macmillan

## Instructions

This Markdown file defines Model SIM.

## Model

### Mechanisms adjusting supply and demand

The following four equations equalise demands and supplies, with whatever is
demanded in each period (variables with a subscript $d$) always supplied
(subscript $s$) in that same period. The equation numbers match those in Godley
and Lavoie (2007).

Household consumption:

\begin{equation} \tag{3.1}
C_s = C_d
\end{equation}

Government consumption:

\begin{equation} \tag{3.2}
G_s = G_d
\end{equation}

Taxes:

\begin{equation} \tag{3.3}
T_s = T_d
\end{equation}

Labour:

\begin{equation} \tag{3.4}
N_s = N_d
\end{equation}

The corresponding Python code, for FSIC, is as follows:

~~~{.python}
C_s = C_d
G_s = G_d
T_s = T_d
N_s = N_d
~~~

Note that in the raw Markdown, there are three tildes that fence the code block
before and after. The block has `.python` as a class attribute, to indicate the
programming language.

### Disposable income and taxes

Disposable income ($YD$) is the wage bill earned by households, minus taxes:

\begin{equation} \tag{3.5}
YD = W . N_s - T_s
\end{equation}

Taxes are a fixed share of income, at rate $\theta$:

\begin{equation} \tag{3.6}
T_d = \theta . W . N_s \qquad \theta < 1
\end{equation}

The corresponding Python code:

~~~{.python}
YD = W * N_s - T_s
T_d = theta * W * N_s
~~~
