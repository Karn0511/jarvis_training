
import os
import time
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.patches import Circle
import matplotlib.patches as mpatches

class VenomVisualizer:
    """
    The Neural Visualizer - Generates dynamic brain activity visualization.
    Shows the AI's neural network with real-time activity indicators.
    """
    
    def __init__(self):
        self.output_path = "storage/assets/neural_activity.png"
        os.makedirs("storage/assets", exist_ok=True)
        
        # Define the neural architecture
        self.nodes = {
            "USER": {"pos": (0, 0), "color": "#00ff00", "size": 1500},
            "EARS": {"pos": (-2, 1), "color": "#00ffff", "size": 1200},
            "VISION": {"pos": (-2, -1), "color": "#ff00ff", "size": 1200},
            "QUANTUM_GATE": {"pos": (-1, 0), "color": "#ffaa00", "size": 1000},
            "LLM_CORE": {"pos": (1, 0), "color": "#ff0000", "size": 2000},
            "MEMORY": {"pos": (2, 1), "color": "#0088ff", "size": 1200},
            "VOICE": {"pos": (2, -1), "color": "#88ff00", "size": 1200},
        }
        
        # Define connections (edges)
        self.edges = [
            ("USER", "EARS"),
            ("USER", "VISION"),
            ("EARS", "QUANTUM_GATE"),
            ("VISION", "QUANTUM_GATE"),
            ("QUANTUM_GATE", "LLM_CORE"),
            ("LLM_CORE", "MEMORY"),
            ("LLM_CORE", "VOICE"),
            ("MEMORY", "LLM_CORE"),
            ("VOICE", "USER"),
        ]
        
    def generate_frame(self, active_node: str = "LLM_CORE", intensity: float = 0.5, cpu_load: float = 0.0):
        """
        Generate a neural activity visualization frame.
        
        Args:
            active_node: Which node is currently active (EARS, LLM_CORE, VISION, etc.)
            intensity: Activity intensity (0.0 to 1.0)
            cpu_load: CPU usage percentage (0-100) affects edge thickness
        """
        start_time = time.time()
        
        # Create figure with dark background
        fig, ax = plt.subplots(figsize=(12, 8), facecolor='#0e1117')
        ax.set_facecolor('#0e1117')
        ax.axis('off')
        
        # Create graph
        G = nx.DiGraph()
        
        # Add nodes
        for node_name, node_data in self.nodes.items():
            G.add_node(node_name, pos=node_data["pos"])
        
        # Add edges
        G.add_edges_from(self.edges)
        
        # Get positions
        pos = {node: self.nodes[node]["pos"] for node in G.nodes()}
        
        # Draw edges with varying thickness based on CPU load
        edge_width = 1 + (cpu_load / 100) * 4  # 1-5 range
        nx.draw_networkx_edges(
            G, pos, 
            edge_color='#00ffaa',
            width=edge_width,
            alpha=0.6,
            arrows=True,
            arrowsize=20,
            arrowstyle='->',
            connectionstyle='arc3,rad=0.1',
            ax=ax
        )
        
        # Draw nodes with glow effect for active node
        for node in G.nodes():
            node_data = self.nodes[node]
            base_size = node_data["size"]
            base_color = node_data["color"]
            
            if node == active_node:
                # Active node: larger, glowing, pulsing
                glow_size = base_size * (1 + intensity * 0.5)
                
                # Draw glow layers
                for i in range(3):
                    alpha = 0.3 - (i * 0.1)
                    size = glow_size * (1 + i * 0.3)
                    nx.draw_networkx_nodes(
                        G, pos,
                        nodelist=[node],
                        node_size=size,
                        node_color=base_color,
                        alpha=alpha,
                        ax=ax
                    )
                
                # Draw core
                nx.draw_networkx_nodes(
                    G, pos,
                    nodelist=[node],
                    node_size=glow_size,
                    node_color=base_color,
                    alpha=0.9,
                    edgecolors='white',
                    linewidths=2,
                    ax=ax
                )
            else:
                # Inactive nodes: normal
                nx.draw_networkx_nodes(
                    G, pos,
                    nodelist=[node],
                    node_size=base_size,
                    node_color=base_color,
                    alpha=0.5,
                    edgecolors='#444444',
                    linewidths=1,
                    ax=ax
                )
        
        # Draw labels
        nx.draw_networkx_labels(
            G, pos,
            font_size=10,
            font_color='white',
            font_weight='bold',
            ax=ax
        )
        
        # Add title with metrics
        title = f"VENOM NEURAL ACTIVITY | Active: {active_node} | Intensity: {intensity:.2f}"
        ax.text(0.5, 0.98, title, 
                transform=ax.transAxes,
                fontsize=14,
                color='#00ffaa',
                weight='bold',
                ha='center',
                va='top')
        
        # Add timestamp
        timestamp = time.strftime("%H:%M:%S")
        ax.text(0.02, 0.02, f"TIMESTAMP: {timestamp}", 
                transform=ax.transAxes,
                fontsize=10,
                color='#888888',
                ha='left',
                va='bottom')
        
        # Save with high quality
        plt.tight_layout()
        plt.savefig(self.output_path, 
                   dpi=100, 
                   facecolor='#0e1117',
                   edgecolor='none',
                   bbox_inches='tight')
        plt.close()
        
        elapsed = (time.time() - start_time) * 1000
        return elapsed  # Return generation time in ms

# Global instance
visualizer = VenomVisualizer()


