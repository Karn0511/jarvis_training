
try:
    from graphviz import Digraph
except ImportError:
    Digraph = None

import os
from .logger import logger

class Architect:
    """
    Renders the Blueprint of Venom's current configuration.
    """
    def __init__(self):
        self.output_path = "data/analytics/venom_architecture"
        os.makedirs("data/analytics", exist_ok=True)

    def render_blueprint(self):
        if Digraph is None:
            logger.error("Architect: Graphviz not installed. Blueprint generation aborted.")
            return "Failed (Graphviz Missing)"

        logger.info("Architect: Drafting System Blueprint...")
        
        dot = Digraph(comment='Project Venom Architecture', format='png')
        dot.attr(rankdir='LR', bgcolor='#111111', fontcolor='white')
        
        # Style
        node_attr = {
            'shape': 'box', 
            'style': 'filled', 
            'color': '#00ff41', 
            'fontcolor': 'black',
            'fontname': 'Courier'
        }
        
        edge_attr = {
            'color': 'white',
            'arrowhead': 'vee'
        }

        # Nodes
        dot.node('U', 'USER (Karn)', shape='circle', style='filled', color='white', fontcolor='black')
        dot.node('STT', 'Venom Ears\n(Whisper)', **node_attr)
        dot.node('CR', 'Cognitive Router\n(Regex/Semantic)', **node_attr)
        dot.node('LLM', 'Neural Core\n(Gemini 1.5/Ollama)', **node_attr)
        dot.node('TTS', 'Venom Voice\n(Edge/Coqui)', **node_attr)
        dot.node('MEM', 'Proprioception\n(Memory/State)', **node_attr)
        dot.node('VIS', 'Visual Cortex\n(YOLOv8)', **node_attr)
        dot.node('ACT', 'Kinetic System\n(Tools)', **node_attr)
        dot.node('HUD', 'Overwatch HUD\n(Streamlit)', shape='box', color='#00ccff', style='dashed', fontcolor='white')

        # Edges
        dot.edge('U', 'STT', label='Audio', **edge_attr)
        dot.edge('U', 'ACT', label='Text', **edge_attr) # Direct console input
        dot.edge('STT', 'CR', label='Text', **edge_attr)
        dot.edge('ACT', 'CR', label='Input', **edge_attr)
        
        # Router logic
        dot.edge('CR', 'LLM', label='Thinking', **edge_attr)
        dot.edge('CR', 'ACT', label='Action', **edge_attr)
        dot.edge('CR', 'VIS', label='Vision Request', **edge_attr)
        
        # Feedback
        dot.edge('LLM', 'TTS', label='Response', **edge_attr)
        dot.edge('VIS', 'CR', label='Detection Data', **edge_attr)
        dot.edge('TTS', 'U', label='Audio Output', **edge_attr)
        
        # Monitoring
        dot.edge('LLM', 'MEM', style='dotted', color='gray')
        dot.edge('MEM', 'HUD', label='JSON Stream', style='dotted', color='#00ccff')
        
        try:
            output = dot.render(self.output_path, cleanup=True)
            logger.success(f"Blueprint Rendered: {output}")
            return output
        except Exception as e:
            logger.error(f"Blueprint Render Failed (Likely Graphviz Binary missing): {e}")
            return f"Failed: {e}"

if __name__ == "__main__":
    arc = Architect()
    arc.render_blueprint()


