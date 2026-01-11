
import pennylane as qml
from pennylane import numpy as np
from ai_core.core.logger import logger
from ai_core.core.event_bus import bus

class QuantumCortex:
    """
    Quantum-Enhanced Decision Engine.
    Uses a Variational Quantum Circuit to determine 'System State' (Urgency, Sentiment).
    
    The User requested 'Quantum Convolutional Neural Network' vibes.
    We implement a Parameterized Quantum Circuit (PQC) that acts as a classifier/filter.
    """
    def __init__(self):
        self.dev = qml.device("default.qubit", wires=4)
        self.qnode = qml.QNode(self._circuit, self.dev)
        # Random weights initialization (In a real system, these would be trained)
        self.weights = np.random.rand(3, 4) 
        
        # Subscribe to inputs
        bus.subscribe("SENSORY_INPUT", self.process_input)

    def _circuit(self, inputs, weights):
        """
        Quantum Circuit Structure:
        1. Embedding (AngleEmbedding) - Encodes classical data to quantum state.
        2. QCNN-like layers (Entanglement + Rotation).
        """
        # 1. Encoding
        # Pad inputs to match wires (4)
        padded_inputs = np.pad(inputs, (0, 4 - len(inputs)), mode='constant') if len(inputs) < 4 else inputs[:4]
        qml.templates.AngleEmbedding(padded_inputs, wires=range(4))
        
        # 2. Variational Layers (The "Network")
        qml.templates.BasicEntanglerLayers(weights, wires=range(4))
        
        # 3. Measurement (Expectation values of PauliZ on each wire)
        return [qml.expval(qml.PauliZ(i)) for i in range(4)]

    def pulse(self, text_input):
        """
        Converts text features to quantum pulse.
        """
        # Feature Extraction (Simple)
        urgency_score = 1.0 if any(w in text_input.lower() for w in ["quick", "fast", "urgent", "now"]) else 0.1
        complexity_score = len(text_input.split()) / 50.0  # Normalize
        sentiment_score = 0.5 # Placeholder
        
        # Input Vector
        input_vec = np.array([urgency_score, complexity_score, sentiment_score, 0.0])
        
        # Execute Quantum Circuit
        quantum_state = self.qnode(input_vec, self.weights)
        
        # Interpret
        # Wire 0 = Urgency Bias
        # Wire 1 = Complexity Bias
        decision_val = float(np.mean(quantum_state))
        
        return {
            "urgency": decision_val, 
            "quantum_state": [float(f) for f in quantum_state]
        }

    async def process_input(self, data):
        """Event Handler"""
        if isinstance(data, str):
            result = self.pulse(data)
            logger.organ("CORTEX", f"Quantum State: {result['urgency']:.2f}")
            # Emit decision event
            # await bus.emit("CORTEX_DECISION", result)


