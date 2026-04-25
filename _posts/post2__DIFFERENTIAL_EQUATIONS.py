"""
post2__DIFFERENTIAL_EQUATIONS.py
=================================
Python module that solves and classifies differential equations from
NCERT Class 12 Mathematics — Chapter 9: Differential Equations.

Source markdown:
    /home/dhankar/temp/26_07__1/oland/git_up/overlander-tech.github.io/
    _posts/post2__DIFFERENTIAL_EQUATIONS.md

This module:
    1. Classifies every equation listed in Chapter 9 by ORDER and DEGREE.
    2. Solves all solvable ODEs using sympy.dsolve.
    3. Emits structured log messages via the shared util_logger setup_logger().
    4. Prints intermediate results to the terminal for interactive debugging.

Logger source:
    /home/dhankar/temp/26_07__1/26_07__v2/agent_eval__1/util_logger.py

Usage:
    python post2__DIFFERENTIAL_EQUATIONS.py

Dependencies:
    sympy  (pip install sympy)
"""

# ---------------------------------------------------------------------------
# PATH SETUP — must come before any local imports
# ---------------------------------------------------------------------------
import sys
import os

# Insert the util_logger package directory at the front of sys.path so that
# `from util_logger import setup_logger` resolves correctly regardless of the
# directory from which this script is invoked.
_LOGGER_DIR = "/home/dhankar/temp/26_07__1/26_07__v2/agent_eval__1"
if _LOGGER_DIR not in sys.path:
    sys.path.insert(0, _LOGGER_DIR)

# ---------------------------------------------------------------------------
# STANDARD / THIRD-PARTY IMPORTS
# ---------------------------------------------------------------------------
from util_logger import setup_logger

from sympy import (
    symbols,          # create symbolic variables
    Function,         # create symbolic functions
    Eq,               # build symbolic equations  Eq(lhs, rhs)
    dsolve,           # solve ODEs symbolically
    exp,              # e^x
    cos,              # cosine
    sin,              # sine
    Derivative,       # explicit derivative objects  Derivative(y(x), x)
    classify_ode,     # classify an ODE (returns tuple of method strings)
    pprint,           # pretty-print to terminal
    oo,               # infinity (unused here but useful for context)
)

# ---------------------------------------------------------------------------
# MODULE-LEVEL LOGGER
# ---------------------------------------------------------------------------
logger = setup_logger("diff_equations")

# ---------------------------------------------------------------------------
# SYMBOLIC VARIABLES & FUNCTIONS used throughout the module
# ---------------------------------------------------------------------------
# Primary independent variable
x = symbols("x")

# Secondary independent variable (Exercise 3 uses s and t)
t = symbols("t")

# Primary dependent function
y = Function("y")

# Secondary dependent function (Exercise 3)
s_func = Function("s")

# ---------------------------------------------------------------------------
# HELPER: degree-not-defined sentinel
# ---------------------------------------------------------------------------
DEGREE_NOT_DEFINED = "NOT DEFINED"


# ===========================================================================
# MAIN CLASS
# ===========================================================================

class DifferentialEquationSolver:
    """
    Solves and classifies differential equations from NCERT Chapter 9.

    Two public entry points:
        run_all_classifications()  — prints order / degree for every equation.
        run_all_solutions()        — calls sympy.dsolve on every solvable ODE.

    The class stores results internally in:
        self.classification_results  (list of dicts)
        self.solution_results        (list of dicts)

    All methods log entry / exit via logger.info() and surface intermediate
    values with print() so the terminal shows a human-readable trace.
    """

    # -----------------------------------------------------------------------
    def __init__(self):
        """
        Initialise the solver, set up result containers, and confirm readiness.

        Stores:
            self.classification_results : list[dict]  — populated by
                                          run_all_classifications()
            self.solution_results       : list[dict]  — populated by
                                          run_all_solutions()
        """
        logger.info("DifferentialEquationSolver.__init__() — initialising solver")
        print("\n" + "=" * 70)
        print("  DifferentialEquationSolver — NCERT Chapter 9")
        print("=" * 70)

        self.classification_results: list = []
        self.solution_results: list = []

        print("[INIT] Solver object created successfully.")
        print(f"[INIT] SymPy symbolic variable x = {x}")
        print(f"[INIT] SymPy symbolic function y = y(x)")
        logger.info("DifferentialEquationSolver.__init__() — complete")

    # -----------------------------------------------------------------------
    def classify_equation(
        self,
        eq_label: str,
        ode_eq,
        order: int,
        degree,
        degree_defined: bool = True,
    ) -> dict:
        """
        Record and display the order and degree classification for one ODE.

        This method does NOT call sympy.classify_ode() for the degree because
        SymPy's classify_ode targets *solution methods*, not the textbook
        order/degree taxonomy.  Instead the caller supplies the textbook-correct
        values derived directly from the equation structure, mirroring the
        NCERT solution manual.

        Parameters
        ----------
        eq_label : str
            Human-readable label, e.g. "Eq 4", "Exercise 2".
        ode_eq : sympy.Expr or sympy.Eq
            The symbolic representation of the ODE (for display only).
        order : int
            The order of the highest derivative present in the equation.
        degree : int or str
            The degree (highest power of the highest-order derivative) or
            the sentinel string DEGREE_NOT_DEFINED when the equation is not
            a polynomial in its derivatives.
        degree_defined : bool
            Pass False when the equation involves transcendental functions of
            derivatives (e.g. sin(y'), e^{y'}), making degree undefined.

        Returns
        -------
        dict
            {
                "label"          : str,
                "order"          : int,
                "degree"         : int | str,
                "degree_defined" : bool,
                "equation"       : sympy expression,
            }
        """
        logger.info(
            "classify_equation() ENTRY — label=%s, order=%d, degree_defined=%s",
            eq_label, order, degree_defined,
        )

        degree_display = degree if degree_defined else DEGREE_NOT_DEFINED

        print(f"\n  [{eq_label}]")
        print(f"    Equation : ", end="")
        try:
            pprint(ode_eq, use_unicode=True)
        except Exception as pprint_err:
            logger.error(
                "classify_equation() — pprint failed for %s: %s", eq_label, pprint_err
            )
            print(f"(display error: {pprint_err})")

        print(f"    Order    : {order}")
        print(f"    Degree   : {degree_display}")

        result = {
            "label": eq_label,
            "order": order,
            "degree": degree_display,
            "degree_defined": degree_defined,
            "equation": ode_eq,
        }
        self.classification_results.append(result)

        logger.info(
            "classify_equation() EXIT — %s  order=%d  degree=%s",
            eq_label, order, degree_display,
        )
        return result

    # -----------------------------------------------------------------------
    def solve_equation(self, eq_label: str, ode_eq, func, var) -> dict:
        """
        Solve a single ordinary differential equation using sympy.dsolve.

        The solution is stored in self.solution_results and pretty-printed to
        the terminal.  On failure the exception is caught, logged, and a
        partial result dict with status="FAILED" is stored so that the run
        continues with the remaining equations.

        Parameters
        ----------
        eq_label : str
            Human-readable label, e.g. "Eq 6", "Exercise 5".
        ode_eq : sympy.Eq
            The ODE expressed as a SymPy Eq() object.
        func : sympy.core.function.AppliedUndef
            The dependent function to solve for, e.g. y(x).
        var : sympy.Symbol
            The independent variable, e.g. x.

        Returns
        -------
        dict
            {
                "label"    : str,
                "ode"      : sympy.Eq,
                "solution" : sympy.Eq | None,
                "status"   : "OK" | "FAILED",
                "error"    : str | None,
            }
        """
        logger.info(
            "solve_equation() ENTRY — label=%s, func=%s, var=%s",
            eq_label, func, var,
        )

        print(f"\n  [{eq_label}] Solving …")
        print("    ODE : ", end="")
        try:
            pprint(ode_eq, use_unicode=True)
        except Exception as pprint_err:
            logger.error(
                "solve_equation() — pprint(ode) failed for %s: %s",
                eq_label, pprint_err,
            )
            print(f"(display error: {pprint_err})")

        solution = None
        status = "OK"
        error_msg = None

        try:
            logger.info("solve_equation() — calling dsolve for %s", eq_label)
            solution = dsolve(ode_eq, func)

            print("    Solution : ", end="")
            pprint(solution, use_unicode=True)
            logger.info(
                "solve_equation() — dsolve succeeded for %s: %s",
                eq_label, solution,
            )

        except Exception as solve_err:
            status = "FAILED"
            error_msg = str(solve_err)
            logger.error(
                "solve_equation() — dsolve FAILED for %s: %s",
                eq_label, solve_err,
            )
            print(f"    [ERROR] dsolve failed: {solve_err}")

        result = {
            "label": eq_label,
            "ode": ode_eq,
            "solution": solution,
            "status": status,
            "error": error_msg,
        }
        self.solution_results.append(result)

        logger.info(
            "solve_equation() EXIT — label=%s  status=%s", eq_label, status
        )
        return result

    # -----------------------------------------------------------------------
    def run_all_classifications(self):
        """
        Run order/degree classification for every equation listed in Chapter 9.

        Equations covered
        -----------------
        Textbook equations  : Eq 4 – Eq 10  (9.2 Basic Concepts)
        Example 1           : parts (i) and (ii)
        Exercise 9.1        : Exercises 1 – 7

        Degree NOT DEFINED cases (equation not a polynomial in derivatives):
            Exercise 1  — sin(y''') prevents polynomial form in y''''
            Exercise 4  — cos(dy/dx) prevents polynomial form in y'

        The method iterates over a list of (label, eq_sympy, order, degree,
        degree_defined) tuples, delegating display/storage to
        classify_equation().
        """
        logger.info("run_all_classifications() ENTRY — processing %d equations", 17)
        print("\n" + "=" * 70)
        print("  SECTION 1: ORDER & DEGREE CLASSIFICATION")
        print("=" * 70)

        # ------------------------------------------------------------------
        # Build symbolic ODE expressions for display purposes.
        # We use Derivative() objects so pprint renders them as d/dx notation.
        # ------------------------------------------------------------------

        dy_dx   = Derivative(y(x), x)
        d2y_dx2 = Derivative(y(x), x, 2)
        d3y_dx3 = Derivative(y(x), x, 3)
        d4y_dx4 = Derivative(y(x), x, 4)

        ds_dt   = Derivative(s_func(t), t)
        d2s_dt2 = Derivative(s_func(t), t, 2)

        # ------------------------------------------------------------------
        # Each entry: (label, sympy_expression, order, degree, degree_defined)
        # ------------------------------------------------------------------
        equations = [
            # --- Section 9.2 numbered equations ----------------------------
            (
                "Eq 4  — x·(dy/dx) + y = 0",
                Eq(x * dy_dx + y(x), 0),
                1, 1, True,
            ),
            (
                "Eq 5  — 2·(d²y/dx²) + (dy/dx)³ = 0",
                Eq(2 * d2y_dx2 + dy_dx**3, 0),
                2, 1, True,
            ),
            (
                "Eq 6  — dy/dx = e^x",
                Eq(dy_dx, exp(x)),
                1, 1, True,
            ),
            (
                "Eq 7  — d²y/dx² + y = 0",
                Eq(d2y_dx2 + y(x), 0),
                2, 1, True,
            ),
            (
                "Eq 8  — (d³y/dx³) + x²·(d²y/dx²)³ = 0",
                Eq(d3y_dx3 + x**2 * d2y_dx2**3, 0),
                3, 1, True,
            ),
            (
                "Eq 9  — d³y/dx³ + 2·(d²y/dx²)² − dy/dx + y = 0",
                Eq(d3y_dx3 + 2 * d2y_dx2**2 - dy_dx + y(x), 0),
                3, 1, True,
            ),
            (
                "Eq 10 — (dy/dx)² + (dy/dx) − sin²(y) = 0",
                Eq(dy_dx**2 + dy_dx - sin(y(x))**2, 0),
                1, 2, True,
            ),
            # --- Example 1 -------------------------------------------------
            (
                "Example 1(i)  — dy/dx − cos(x) = 0",
                Eq(dy_dx - cos(x), 0),
                1, 1, True,
            ),
            (
                "Example 1(ii) — xy·(d²y/dx²) + x·(dy/dx)² − y·(dy/dx) = 0",
                Eq(x * y(x) * d2y_dx2 + x * dy_dx**2 - y(x) * dy_dx, 0),
                2, 1, True,
            ),
            # --- Exercise 9.1 ----------------------------------------------
            (
                "Exercise 1 — d⁴y/dx⁴ + sin(y''') = 0  [degree NOT DEFINED]",
                Eq(d4y_dx4 + sin(d3y_dx3), 0),
                4, DEGREE_NOT_DEFINED, False,
            ),
            (
                "Exercise 2 — y' + 5y = 0",
                Eq(dy_dx + 5 * y(x), 0),
                1, 1, True,
            ),
            (
                "Exercise 3 — (ds/dt)⁴ + 3s·(d²s/dt²) = 0",
                Eq(ds_dt**4 + 3 * s_func(t) * d2s_dt2, 0),
                2, 1, True,
            ),
            (
                "Exercise 4 — (d²y/dx²)² + cos(dy/dx) = 0  [degree NOT DEFINED]",
                Eq(d2y_dx2**2 + cos(dy_dx), 0),
                2, DEGREE_NOT_DEFINED, False,
            ),
            (
                "Exercise 5 — d²y/dx² = cos(3x) + sin(3x)",
                Eq(d2y_dx2, cos(3 * x) + sin(3 * x)),
                2, 1, True,
            ),
            (
                "Exercise 6 — (y''')² + (y'')³ + (y')⁴ + y⁵ = 0",
                Eq(d3y_dx3**2 + d2y_dx2**3 + dy_dx**4 + y(x)**5, 0),
                3, 2, True,
            ),
            (
                "Exercise 7 — y''' + 2y'' + y' = 0",
                Eq(d3y_dx3 + 2 * d2y_dx2 + dy_dx, 0),
                3, 1, True,
            ),
        ]

        logger.info(
            "run_all_classifications() — iterating over %d equation entries",
            len(equations),
        )

        for label, eq_expr, order, degree, deg_defined in equations:
            try:
                self.classify_equation(
                    eq_label=label,
                    ode_eq=eq_expr,
                    order=order,
                    degree=degree,
                    degree_defined=deg_defined,
                )
            except Exception as err:
                logger.error(
                    "run_all_classifications() — unexpected error for '%s': %s",
                    label, err,
                )
                print(f"  [ERROR] Could not classify '{label}': {err}")

        print("\n" + "-" * 70)
        print(
            f"  Classification complete. {len(self.classification_results)} "
            f"equations processed."
        )
        logger.info(
            "run_all_classifications() EXIT — %d results stored",
            len(self.classification_results),
        )

    # -----------------------------------------------------------------------
    def run_all_solutions(self):
        """
        Solve all solvable differential equations using sympy.dsolve.

        Equations solved
        ----------------
        1.  Eq 4   : x*(dy/dx) + y = 0          (first-order linear, separable)
        2.  Eq 6   : dy/dx = e^x                 (direct integration)
        3.  Eq 7   : d²y/dx² + y = 0             (second-order, constant coeff.)
        4.  Ex 1i  : dy/dx − cos(x) = 0          (direct integration)
        5.  Ex 2   : y' + 5y = 0                 (first-order linear)
        6.  Ex 5   : d²y/dx² = cos(3x)+sin(3x)  (direct double integration)
        7.  Ex 7   : y'''+2y''+y'=0              (third-order, constant coeff.)

        Each call delegates to self.solve_equation() which wraps dsolve in a
        try/except block and emits logger.info / logger.error appropriately.
        """
        logger.info("run_all_solutions() ENTRY — solving 7 ODEs")
        print("\n" + "=" * 70)
        print("  SECTION 2: SOLVING DIFFERENTIAL EQUATIONS  (sympy.dsolve)")
        print("=" * 70)

        # Convenience derivative objects
        dy_dx   = Derivative(y(x), x)
        d2y_dx2 = Derivative(y(x), x, 2)
        d3y_dx3 = Derivative(y(x), x, 3)

        # ------------------------------------------------------------------
        # 1. Eq 4 : x*(dy/dx) + y = 0
        # ------------------------------------------------------------------
        print("\n--- Equation 4  [x*(dy/dx) + y = 0] ---")
        logger.info("run_all_solutions() — building Eq4 symbolic form")
        eq4 = Eq(x * dy_dx + y(x), 0)
        print("[Eq4] Symbolic form constructed.")
        print(f"[Eq4] ode_eq = {eq4}")
        self.solve_equation(
            eq_label="Eq 4  — x·(dy/dx) + y = 0",
            ode_eq=eq4,
            func=y(x),
            var=x,
        )

        # ------------------------------------------------------------------
        # 2. Eq 6 : dy/dx = e^x
        # ------------------------------------------------------------------
        print("\n--- Equation 6  [dy/dx = e^x] ---")
        logger.info("run_all_solutions() — building Eq6 symbolic form")
        eq6 = Eq(dy_dx, exp(x))
        print(f"[Eq6] ode_eq = {eq6}")
        self.solve_equation(
            eq_label="Eq 6  — dy/dx = e^x",
            ode_eq=eq6,
            func=y(x),
            var=x,
        )

        # ------------------------------------------------------------------
        # 3. Eq 7 : d²y/dx² + y = 0
        # ------------------------------------------------------------------
        print("\n--- Equation 7  [d²y/dx² + y = 0] ---")
        logger.info("run_all_solutions() — building Eq7 symbolic form")
        eq7 = Eq(d2y_dx2 + y(x), 0)
        print(f"[Eq7] ode_eq = {eq7}")
        self.solve_equation(
            eq_label="Eq 7  — d²y/dx² + y = 0",
            ode_eq=eq7,
            func=y(x),
            var=x,
        )

        # ------------------------------------------------------------------
        # 4. Example 1(i) : dy/dx − cos(x) = 0
        # ------------------------------------------------------------------
        print("\n--- Example 1(i)  [dy/dx − cos(x) = 0] ---")
        logger.info("run_all_solutions() — building Example1i symbolic form")
        eq_ex1i = Eq(dy_dx - cos(x), 0)
        print(f"[Ex1i] ode_eq = {eq_ex1i}")
        self.solve_equation(
            eq_label="Example 1(i) — dy/dx − cos(x) = 0",
            ode_eq=eq_ex1i,
            func=y(x),
            var=x,
        )

        # ------------------------------------------------------------------
        # 5. Exercise 2 : y' + 5y = 0
        # ------------------------------------------------------------------
        print("\n--- Exercise 2  [y' + 5y = 0] ---")
        logger.info("run_all_solutions() — building Exercise2 symbolic form")
        eq_ex2 = Eq(dy_dx + 5 * y(x), 0)
        print(f"[Ex2] ode_eq = {eq_ex2}")
        self.solve_equation(
            eq_label="Exercise 2 — y' + 5y = 0",
            ode_eq=eq_ex2,
            func=y(x),
            var=x,
        )

        # ------------------------------------------------------------------
        # 6. Exercise 5 : d²y/dx² = cos(3x) + sin(3x)
        # ------------------------------------------------------------------
        print("\n--- Exercise 5  [d²y/dx² = cos(3x) + sin(3x)] ---")
        logger.info("run_all_solutions() — building Exercise5 symbolic form")
        eq_ex5 = Eq(d2y_dx2, cos(3 * x) + sin(3 * x))
        print(f"[Ex5] ode_eq = {eq_ex5}")
        self.solve_equation(
            eq_label="Exercise 5 — d²y/dx² = cos(3x) + sin(3x)",
            ode_eq=eq_ex5,
            func=y(x),
            var=x,
        )

        # ------------------------------------------------------------------
        # 7. Exercise 7 : y''' + 2y'' + y' = 0
        # ------------------------------------------------------------------
        print("\n--- Exercise 7  [y''' + 2y'' + y' = 0] ---")
        logger.info("run_all_solutions() — building Exercise7 symbolic form")
        eq_ex7 = Eq(d3y_dx3 + 2 * d2y_dx2 + dy_dx, 0)
        print(f"[Ex7] ode_eq = {eq_ex7}")
        self.solve_equation(
            eq_label="Exercise 7 — y''' + 2y'' + y' = 0",
            ode_eq=eq_ex7,
            func=y(x),
            var=x,
        )

        # ------------------------------------------------------------------
        # Summary
        # ------------------------------------------------------------------
        ok_count   = sum(1 for r in self.solution_results if r["status"] == "OK")
        fail_count = sum(1 for r in self.solution_results if r["status"] == "FAILED")

        print("\n" + "-" * 70)
        print(f"  Solution run complete.")
        print(f"    Succeeded : {ok_count}")
        print(f"    Failed    : {fail_count}")
        print("-" * 70)

        logger.info(
            "run_all_solutions() EXIT — succeeded=%d  failed=%d",
            ok_count, fail_count,
        )

    # -----------------------------------------------------------------------
    def print_summary(self):
        """
        Print a compact summary table of all classification and solution results.

        This method is optional but useful for a quick human-readable overview
        at the end of a run.  It iterates over the two result lists populated
        by run_all_classifications() and run_all_solutions().
        """
        logger.info("print_summary() ENTRY")
        print("\n" + "=" * 70)
        print("  SUMMARY — CLASSIFICATIONS")
        print("=" * 70)
        print(f"  {'Label':<55} {'Order':>5}  {'Degree':>14}")
        print("  " + "-" * 60)
        for rec in self.classification_results:
            print(
                f"  {rec['label']:<55} "
                f"{rec['order']:>5}  "
                f"{str(rec['degree']):>14}"
            )

        print("\n" + "=" * 70)
        print("  SUMMARY — SOLUTIONS")
        print("=" * 70)
        print(f"  {'Label':<50} {'Status':>8}")
        print("  " + "-" * 60)
        for rec in self.solution_results:
            print(f"  {rec['label']:<50} {rec['status']:>8}")

        logger.info(
            "print_summary() EXIT — %d classifications, %d solutions",
            len(self.classification_results),
            len(self.solution_results),
        )


# ===========================================================================
# ENTRY POINT
# ===========================================================================

if __name__ == "__main__":
    logger.info("__main__ — script started")
    print("\n" + "#" * 70)
    print("  NCERT Chapter 9 — Differential Equations (SymPy solver)")
    print("  " + "post2__DIFFERENTIAL_EQUATIONS.py")
    print("#" * 70)

    try:
        solver = DifferentialEquationSolver()

        # --- Part 1: classify all equations --------------------------------
        solver.run_all_classifications()

        # --- Part 2: solve all solvable equations --------------------------
        solver.run_all_solutions()

        # --- Part 3: compact summary table ---------------------------------
        solver.print_summary()

        print("\n[DONE] All tasks completed successfully.")
        logger.info("__main__ — all tasks completed successfully")

    except Exception as top_err:
        logger.error("__main__ — unhandled exception: %s", top_err, exc_info=True)
        print(f"\n[FATAL] Unhandled exception: {top_err}")
        sys.exit(1)

    logger.info("__main__ — script exiting normally")
