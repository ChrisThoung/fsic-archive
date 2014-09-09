# An Accelerator-Multiplier Interaction model of an imaginary economy

## Setup

~~~{.ini}
NAME = AMI
DESCRIPTION = An Accelerator-Multiplier Interaction model of an imaginary economy
REFERENCE = Almon, C. (2014), *The craft of economic modeling*, 5th edition: http://www.inforum.umd.edu/papers/TheCraft.html
MAJOR = 0
MINOR = 1
PATCH = 0
DEV = Yes
~~~

## Equations

Consumption:

\begin{equation} \tag{1}
C_t = 0.6 * Y_{t-1} + 0.35 * Y_{t-2}
\end{equation}

Where $C$ is consumption and $Y$ is disposable income.

~~~{.python}
C = 0.6 * Y[-1] + 0.35 * Y[-2]
~~~

Fixed investment follows the 'accelerator' theory of investment:

\begin{equation} \tag{2}
I_t = R_t + 1.0 * \Delta PQ_{t-1} + 1.0 * \Delta PQ_{t-2}
\end{equation}

~~~{.python}
I = R + 1.0 * (PQ[-1] - PQ[-2]) + 1.0 * (PQ[-1] - PQ[-2])
~~~

Where $I$ is gross investment, $Q$ is output, $R$ is replacement investment and
PQ is peak output, defined as:

* $Q_t$, if $Q_t > PQ_{t-1}$
* $PQ_{t-1}$ otherwise

FSIC recognises Python function calls, so this equation can be represented as
follows:

~~~{.python}
PQ = max(Q, PQ[-1])
~~~

Imports are a function of demand for domestic production:

\begin{equation} \tag{4}
M_t = -380 + 0.2 * (C_t + I_t + X_t)
\end{equation}

~~~{.python}
M = -380 + 0.2 * (C + I + X)
~~~

The output identity is:

\begin{equation} \tag{5}
Q_t = C_t + I_t + G_t + X_t - M_t
\end{equation}

~~~{.python}
Q = C + I + G + X - M
~~~

Finally, disposable income is output minus taxes:

\begin{equation} \tag{6}
Y_t = 0.72 * Q_t
\end{equation}

~~~{.python}
Y = 0.72 * Q
~~~
