# Chapter 3: The simplest model with government money

Markdown file to demonstrate how to use `fsic-build.py`, using the example of
Model SIM from Godley and Lavoie (2007).

## Instructions

This Markdown file defines Model SIM.

## Setup

The block below defines various pieces of descriptive information about the
model, including its:

* `NAME`
* `DESCRIPTION`
* `REFERENCE` to the corresponding documentation or academic paper, if
  applicable
* Version number, comprising:
    * `MAJOR` version number
    * `MINOR` version number
    * `PATCH` number
	* Whether this is a `DEV`elopment version or not

~~~{.ini}
NAME = SIM
DESCRIPTION = The simplest model with government money
REFERENCE = Godley, W. and Lavoie, M. (2007), *Monetary economics: an integrated approach to credit, money, income, production and wealth*, Palgrave Macmillan
MAJOR = 0
MINOR = 0
PATCH = 0
DEV = Yes
~~~

## Equations of Model SIM

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

### Consumption function

\begin{equation} \tag{3.7}
C_d = \alpha_1 . YD + \alpha_2 . H_{h-1} \qquad 0 < \alpha_2 < \alpha_1 < 1
\end{equation}

In Python:

~~~{.python}
C_d = alpha_1 * YD + alpha_2 * H_h[-1]
~~~

### Government debt/household holdings of cash

The government surplus/deficit (the change in debt) is the difference between
(consumption) expenditure and (tax) revenue:

\begin{equation} \tag{3.8}
\Delta H_s = H_s - H_{s-1} = G_d - T_d
\end{equation}

Alternatively, household holdings of that debt are a vehicle for savings:

\begin{equation} \tag{3.9}
\Delta H_h = H_h - H_{h-1} = YD - C_d
\end{equation}

These equations are more conveniently represented in terms of the stock of debt,
rather than as flows:

~~~{.python}
H_s = H_s[-1] + G_d - T_d
H_h = H_h[-1] + YD - C_d
~~~

### National income identity

In output terms:

\begin{equation} \tag{3.10}
Y = C_s + G_s
\end{equation}

Or, in income terms:

\begin{equation} \tag{3.11A}
Y = W . N_d
\end{equation}

Which by re-arrangement, gives labour demand:

\begin{equation} \tag{3.11}
N_d = \frac{Y}{W}
\end{equation}

The corresponding Python equations are:

~~~{.python}
Y = C_s + G_s
N_d = Y / W
~~~

### The hidden/redundant equation

\begin{equation} \tag{3.12}
\Delta H_h = \Delta H_s
\end{equation}

As for the changes in debt/cash, this is better represented as equality of
stocks:

~~~{.python .hidden}
H_h = H_s
~~~
