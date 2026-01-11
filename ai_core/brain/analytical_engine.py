
import asyncio
import sympy
import matplotlib.pyplot as plt
import numpy as np
import re
from ai_core.core.logger import logger

class AnalyticalEngine:
    """
    Advanced Mathematics & Data Visualization Engine.
    Handles calculations (SymPy), graphing (Matplotlib), and Logic.
    """
    def __init__(self):
        # We don't verify Brain here to avoid circular imports if possible, 
        # or we inject it later.
        pass
        
    async def process_math(self, query):
        """
        Detects if query is mathematical and computes it locally.
        """
        query_lower = query.lower()
        math_trigger = any(x in query_lower for x in ["calculate", "solve", "math", "derivative", "integral"])
        graph_trigger = any(x in query_lower for x in ["graph", "plot", "chart"])

        if math_trigger:
            return await self.solve_symbolic(query)
        
        if graph_trigger:
            return await self.generate_plot(query)
                
        return None

    async def solve_symbolic(self, query):
        """
        Extracts math expression and solves using SymPy.
        """
        logger.print(f"Analytical Engine Parsing: {query}", style="brain")
        
        try:
            # 1. Regex Extraction (Naive but fast for "calculate 2+2")
            # Be careful with eval/sympify!
            # Look for patterns like "integrate x**2" or "derivative of sin(x)"
            
            # Simple Case: basic arithmetic
            # Remove non-math words roughly
            expression = re.sub(r'[a-zA-Z\s\?]', '', query) # Only keep numbers/operators? Too aggressive.
            
            # Better: Let's assume the user says "Calculate <expr>"
            if "calculate" in query.lower():
                expr_str = query.lower().split("calculate")[-1].strip(" .?")
                
                # Check for specific operations
                if "derivative" in query.lower():
                    # "derivative of x^2"
                    target = query.lower().split("derivative of")[-1].strip()
                    x = sympy.symbols('x')
                    result = sympy.diff(target, x)
                    return f"Derivative: {result}"
                
                # Default calculate
                result = sympy.sympify(expr_str).evalf()
                return f"Computed Result: {result}"

        except Exception as e:
            logger.error(f"Math Parse Error: {e}")
            return None # Let the Brain handle it if Engine fails

        return None

    async def generate_plot(self, query, save_path="./data/latest_graph.png"):
        """
        Generates a plot based on keywords or expressions.
        """
        try:
            import os
            logger.print("Plotting Data Stream...", style="brain")
            x = np.linspace(-10, 10, 400)
            
            # Dynamic Parsing logic (Basic)
            title = "Graph"
            if "sin" in query:
                y = np.sin(x)
                title = "Sine Wave"
            elif "cos" in query:
                y = np.cos(x)
                title = "Cosine Wave"
            elif "tan" in query:
                y = np.tan(x)
                title = "Tangent"
            elif "square" in query or "x^2" in query:
                y = x**2
                title = "Parabola (x^2)"
            elif "cube" in query or "x^3" in query:
                y = x**3
                title = "Cubic Function (x^3)"
            else:
                y = x
                title = "Linear"

            plt.figure(figsize=(10, 6))
            plt.plot(x, y, color='#00ffcc', linewidth=2, label=title)
            plt.title(f"VENOM ANALYTICS: {title}", color='white', fontweight='bold')
            plt.grid(True, linestyle='--', alpha=0.3)
            plt.legend()
            
            # Dark Mode Style (Venom Theme)
            ax = plt.gca()
            ax.set_facecolor('#1e1e1e')
            plt.gcf().patch.set_facecolor('#121212')
            ax.tick_params(colors='white')
            ax.xaxis.label.set_color('white')
            ax.yaxis.label.set_color('white')
            
            # Ensure dir exists
            os.makedirs("./data", exist_ok=True)
            plt.savefig(save_path)
            plt.close()
            
            # Open the graph immediately for the user
            os.startfile(os.path.abspath(save_path))
            return f"Visualization projected to screen."
            
        except Exception as e:
            logger.error(f"Plotting Failed: {e}")
            return None

engine = AnalyticalEngine()


