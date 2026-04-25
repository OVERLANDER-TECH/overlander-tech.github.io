---
title: "Chapter 9 — Differential Equations"
date: 2026-04-26
layout: post
categories: mathematics differential-equations
---

# Chapter 9: DIFFERENTIAL EQUATIONS

> *"He who seeks for methods without having a definite problem in mind seeks for the most part in vain."* — **D. Hilbert**

---

## 9.1 Introduction

In Class XI and in Chapter 5 of the present book, we discussed how to differentiate a given function $f$ with respect to an independent variable, i.e., how to find $f'(x)$ for a given function $f$ at each $x$ in its domain of definition. Further, in the chapter on Integral Calculus, we discussed how to find a function $f$ whose derivative is the function $g$, which may also be formulated as follows:

For a given function $g$, find a function $f$ such that

$$\frac{dy}{dx} = g(x), \text{ where } y = f(x) \tag{1}$$

An equation of the form (1) is known as a *differential equation*. A formal definition will be given later.

> **Henri Poincare (1854–1912)** — French mathematician who made fundamental contributions to pure and applied mathematics, mathematical physics, and celestial mechanics.

These equations arise in a variety of applications, may it be in Physics, Chemistry, Biology, Anthropology, Geology, Economics etc. Hence, an in-depth study of differential equations has assumed prime importance in all modern scientific investigations.

In this chapter, we will study some basic concepts related to differential equation, general and particular solutions of a differential equation, formation of differential equations, some methods to solve a first order - first degree differential equation and some applications of differential equations in different areas.

---

## 9.2 Basic Concepts

We are already familiar with the equations of the type:

$$x^2 - 3x + 3 = 0 \tag{1}$$

$$\sin x + \cos x = 0 \tag{2}$$

$$x + y = 7 \tag{3}$$

Let us consider the equation:

$$x\frac{dy}{dx} + y = 0 \tag{4}$$

We see that equations (1), (2) and (3) involve independent and/or dependent variable (variables) only but equation (4) involves variables as well as derivative of the dependent variable $y$ with respect to the independent variable $x$. Such an equation is called a *differential equation*.

In general, an equation involving derivative (derivatives) of the dependent variable with respect to independent variable (variables) is called a **differential equation**.

A differential equation involving derivatives of the dependent variable with respect to only one independent variable is called an **ordinary differential equation**, e.g.,

$$2\frac{d^2y}{dx^2} + \left(\frac{dy}{dx}\right)^3 = 0 \text{ is an ordinary differential equation} \tag{5}$$

Of course, there are differential equations involving derivatives with respect to more than one independent variables, called partial differential equations but at this stage we shall confine ourselves to the study of ordinary differential equations only. Now onward, we will use the term 'differential equation' for 'ordinary differential equation'.

> **Note:**
> 1. We shall prefer to use the following notations for derivatives:
>    $\frac{dy}{dx} = y'$, $\frac{d^2y}{dx^2} = y''$, $\frac{d^3y}{dx^3} = y'''$
> 2. For derivatives of higher order, it will be inconvenient to use so many dashes as supersuffix therefore, we use the notation $y_n$ for $n$th order derivative $\frac{d^ny}{dx^n}$.

---

### 9.2.1 Order of a differential equation

Order of a differential equation is defined as the order of the highest order derivative of the dependent variable with respect to the independent variable involved in the given differential equation.

Consider the following differential equations:

$$\frac{dy}{dx} = e^x \tag{6}$$

$$\frac{d^2y}{dx^2} + y = 0 \tag{7}$$

$$\left(\frac{d^3y}{dx^3}\right) + x^2\left(\frac{d^2y}{dx^2}\right)^3 = 0 \tag{8}$$

The equations (6), (7) and (8) involve the highest derivative of first, second and third order respectively. Therefore, the order of these equations are 1, 2 and 3 respectively.

---

### 9.2.2 Degree of a differential equation

To study the degree of a differential equation, the key point is that the differential equation must be a polynomial equation in derivatives, i.e., $y'$, $y''$, $y'''$ etc. Consider the following differential equations:

$$\frac{d^3y}{dx^3} + 2\left(\frac{d^2y}{dx^2}\right)^2 - \frac{dy}{dx} + y = 0 \tag{9}$$

$$\left(\frac{dy}{dx}\right)^2 + \left(\frac{dy}{dx}\right) - \sin^2 y = 0 \tag{10}$$

$$\frac{dy}{dx} + \sin\left(\frac{dy}{dx}\right) = 0 \tag{11}$$

We observe that equation (9) is a polynomial equation in $y'''$, $y''$ and $y'$, equation (10) is a polynomial equation in $y'$ (not a polynomial in $y$ though). Degree of such differential equations can be defined. But equation (11) is not a polynomial equation in $y'$ and degree of such a differential equation can not be defined.

By the **degree** of a differential equation, when it is a polynomial equation in derivatives, we mean the highest power (positive integral index) of the highest order derivative involved in the given differential equation.

In view of the above definition, one may observe that differential equations (6), (7), (8) and (9) each are of degree one, equation (10) is of degree two while the degree of differential equation (11) is not defined.

> **Note:** Order and degree (if defined) of a differential equation are always positive integers.

---

## Example 1

**Find the order and degree, if defined, of each of the following differential equations:**

**(i)** $\frac{dy}{dx} - \cos x = 0$

**(ii)** $xy\frac{d^2y}{dx^2} + x\left(\frac{dy}{dx}\right)^2 - y\frac{dy}{dx} = 0$

**(iii)** $y''' + y^2 + e^{y'} = 0$

### Solution

**(i)** The highest order derivative present in the differential equation is $\frac{dy}{dx}$, so its order is **one**. It is a polynomial equation in $y'$ and the highest power raised to $\frac{dy}{dx}$ is one, so its degree is **one**.

**(ii)** The highest order derivative present in the given differential equation is $\frac{d^2y}{dx^2}$, so its order is **two**. It is a polynomial equation in $\frac{d^2y}{dx^2}$ and $\frac{dy}{dx}$ and the highest power raised to $\frac{d^2y}{dx^2}$ is one, so its degree is **one**.

**(iii)** The highest order derivative present in the differential equation is $y'''$, so its order is **three**. The given differential equation is not a polynomial equation in its derivatives and so its degree is **not defined**.

---

## Exercise 9.1

**Determine order and degree (if defined) of differential equations given in Exercises 1 to 10.**

**1.** $\frac{d^4y}{dx^4} + \sin(y''') = 0$

**2.** $y' + 5y = 0$

**3.** $\left(\frac{ds}{dt}\right)^4 + 3s\frac{d^2s}{dt^2} = 0$

**4.** $\left(\frac{d^2y}{dx^2}\right)^2 + \cos\left(\frac{dy}{dx}\right) = 0$

**5.** $\frac{d^2y}{dx^2} = \cos 3x + \sin 3x$

**6.** $(y''')^2 + (y'')^3 + (y')^4 + y^5 = 0$

**7.** $y''' + 2y'' + y' = 0$

---
