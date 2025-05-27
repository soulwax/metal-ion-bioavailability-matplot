# File: enhanced_micronutrient_network.py

"""
Enhanced Micronutrient Interaction Network Visualizer
This script was created using all medical and nutritional knowledge available up to October 2025. See pubmed.ncbi.nlm.nih.gov for more info.

Features:
- Color-coded functional groups
- Interactive-style layout with improved spacing
- Enhanced visual styling and typography
- Comprehensive legend system
- High-resolution output with customizable paths
- Robust error handling and logging
"""

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import Patch, FancyBboxPatch
from matplotlib.cm import get_cmap
from matplotlib.colors import to_hex
from pathlib import Path
import logging
from typing import Dict, List, Tuple, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class MicronutrientNetworkVisualizer:
    """
    A comprehensive visualizer for micronutrient interaction networks.
    """

    def __init__(self, output_dir: str = "images"):
        """
        Initialize the visualizer with configuration parameters.

        Args:
            output_dir: Directory to save the generated images
        """
        self.output_dir = Path(output_dir)
        self.setup_output_directory()

        # Visual configuration
        self.figure_size = (16, 16)
        self.node_size = 800
        self.font_size_nodes = 9
        self.font_size_edges = 12
        self.font_size_title = 16
        self.font_size_legend = 10
        self.dpi = 300

        # Network configuration
        self.layout_k = 1.2  # Spring layout parameter
        self.layout_iterations = 100
        self.connection_style_radius = 0.2

        self.initialize_data()

    def setup_output_directory(self) -> None:
        """Create output directory if it doesn't exist."""
        try:
            self.output_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Output directory ready: {self.output_dir}")
        except Exception as e:
            logger.error(f"Failed to create output directory: {e}")
            raise

    def initialize_data(self) -> None:
        """Initialize micronutrient groups and interaction data."""

        # Functional groups with enhanced categorization
        self.groups = {
            "Electrolytes & Fluid Balance": [
                "Sodium (Na)",
                "Potassium (K)",
                "Phosphorus (P)",
            ],
            "Bone Health & Structure": [
                "Calcium (Ca)",
                "Magnesium (Mg)",
                "Fluoride (F)",
                "Silicon (Si)",
                "Boron (B)",
            ],
            "Blood Formation & Oxygen Transport": [
                "Iron (Fe)",
                "Cobalt (Co)",
                "Copper (Cu)",
            ],
            "Enzymatic Cofactors": [
                "Zinc (Zn)",
                "Manganese (Mn)",
                "Chromium (Cr)",
                "Molybdenum (Mo)",
                "Nickel (Ni)",
                "Vanadium (V)",
            ],
            "Endocrine & Metabolic": ["Iodine (I)", "Selenium (Se)", "Lithium (Li)"],
        }

        # Comprehensive interaction network
        self.interactions = [
            # Calcium interactions
            ("Calcium (Ca)", "Iron (Fe)", "inhibits", "high"),
            ("Calcium (Ca)", "Magnesium (Mg)", "inhibits", "medium"),
            ("Magnesium (Mg)", "Calcium (Ca)", "boosts", "high"),
            # Zinc-related interactions
            ("Zinc (Zn)", "Copper (Cu)", "inhibits", "high"),
            ("Zinc (Zn)", "Iron (Fe)", "inhibits", "medium"),
            ("Iron (Fe)", "Zinc (Zn)", "inhibits", "medium"),
            ("Nickel (Ni)", "Zinc (Zn)", "inhibits", "low"),
            # Iron metabolism
            ("Manganese (Mn)", "Iron (Fe)", "inhibits", "medium"),
            ("Chromium (Cr)", "Iron (Fe)", "inhibits", "low"),
            ("Vanadium (V)", "Iron (Fe)", "inhibits", "low"),
            ("Cobalt (Co)", "Iron (Fe)", "inhibits", "medium"),
            # Copper interactions
            ("Molybdenum (Mo)", "Copper (Cu)", "inhibits", "high"),
            # Thyroid-related
            ("Selenium (Se)", "Iodine (I)", "boosts", "high"),
            ("Iron (Fe)", "Iodine (I)", "boosts", "medium"),
            ("Lithium (Li)", "Iodine (I)", "inhibits", "low"),
            # Electrolyte balance
            ("Sodium (Na)", "Potassium (K)", "inhibits", "high"),
            ("Potassium (K)", "Sodium (Na)", "inhibits", "high"),
            ("Sodium (Na)", "Calcium (Ca)", "inhibits", "medium"),
            ("Potassium (K)", "Calcium (Ca)", "boosts", "medium"),
            # Bone health synergies
            ("Boron (B)", "Calcium (Ca)", "boosts", "medium"),
            ("Boron (B)", "Magnesium (Mg)", "boosts", "medium"),
            ("Silicon (Si)", "Calcium (Ca)", "boosts", "medium"),
            # Calcium inhibitors
            ("Phosphorus (P)", "Calcium (Ca)", "inhibits", "medium"),
            ("Fluoride (F)", "Calcium (Ca)", "inhibits", "low"),
        ]

        # Extract all unique nodes
        self.all_nodes = list(
            set([node for group in self.groups.values() for node in group])
        )

        # Interaction strength mapping
        self.strength_weights = {"high": 2.5, "medium": 1.8, "low": 1.2}
        self.strength_alpha = {"high": 0.9, "medium": 0.7, "low": 0.5}

    def create_color_scheme(self) -> Dict[str, str]:
        """
        Create an enhanced color scheme for functional groups.

        Returns:
            Dictionary mapping group names to hex colors
        """
        # Use a more sophisticated color palette
        color_palette = [
            "#FF6B6B",  # Coral Red - Electrolytes
            "#4ECDC4",  # Teal - Bone Health
            "#45B7D1",  # Sky Blue - Blood/Oxygen
            "#96CEB4",  # Sage Green - Enzymes
            "#FFEAA7",  # Warm Yellow - Endocrine
        ]

        group_colors = {}
        for i, group in enumerate(self.groups.keys()):
            group_colors[group] = color_palette[i % len(color_palette)]

        # Map individual nodes to colors
        node_colors = {}
        for group, nodes in self.groups.items():
            for node in nodes:
                node_colors[node] = group_colors[group]

        return node_colors, group_colors

    def build_network_graph(self) -> nx.DiGraph:
        """
        Construct the network graph with nodes and weighted edges.

        Returns:
            NetworkX directed graph
        """
        G = nx.DiGraph()

        # Add all nodes
        G.add_nodes_from(self.all_nodes)

        # Add edges with attributes
        for interaction in self.interactions:
            if len(interaction) == 4:
                u, v, relation, strength = interaction
            else:
                u, v, relation = interaction
                strength = "medium"  # Default strength

            G.add_edge(
                u,
                v,
                relation=relation,
                strength=strength,
                weight=self.strength_weights[strength],
                alpha=self.strength_alpha[strength],
            )

        logger.info(
            f"Graph created with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges"
        )
        return G

    def calculate_layout(self, G: nx.DiGraph) -> Dict:
        """
        Calculate optimal node positions using spring layout with customizations.

        Args:
            G: NetworkX graph

        Returns:
            Dictionary of node positions
        """
        # Try multiple layout algorithms and choose the best
        layouts = {
            "spring": nx.spring_layout(
                G, k=self.layout_k, iterations=self.layout_iterations, seed=42
            ),
            "kamada_kawai": nx.kamada_kawai_layout(G),
            "circular": nx.circular_layout(G),
        }

        # Use spring layout as default (generally produces good results)
        pos = layouts["spring"]

        # Fine-tune positions to avoid overlaps
        pos = self.adjust_positions_for_clarity(pos)

        return pos

    def adjust_positions_for_clarity(self, pos: Dict) -> Dict:
        """
        Adjust node positions to minimize overlaps and improve readability.

        Args:
            pos: Initial position dictionary

        Returns:
            Adjusted position dictionary
        """
        # Convert to numpy arrays for easier manipulation
        positions = np.array(list(pos.values()))
        nodes = list(pos.keys())

        # Apply small random perturbations to avoid perfect overlaps
        np.random.seed(42)
        perturbations = np.random.normal(0, 0.02, positions.shape)
        positions += perturbations

        # Rebuild position dictionary
        adjusted_pos = {node: positions[i] for i, node in enumerate(nodes)}

        return adjusted_pos

    def draw_enhanced_network(
        self, G: nx.DiGraph, pos: Dict, node_colors: Dict, group_colors: Dict
    ) -> plt.Figure:
        """
        Create the main network visualization with enhanced styling.

        Args:
            G: NetworkX graph
            pos: Node positions
            node_colors: Node color mapping
            group_colors: Group color mapping

        Returns:
            Matplotlib figure object
        """
        # Create figure with enhanced styling
        plt.style.use("default")
        fig, ax = plt.subplots(figsize=self.figure_size, facecolor="white")
        ax.set_facecolor("#FAFAFA")

        # Draw nodes with enhanced styling
        node_color_list = [node_colors[node] for node in G.nodes()]

        # Draw nodes with subtle shadow effect
        nx.draw_networkx_nodes(
            G,
            pos,
            node_color=node_color_list,
            node_size=self.node_size,
            alpha=0.9,
            linewidths=2,
            edgecolors="white",
        )

        # Draw node labels with improved typography
        for node, (x, y) in pos.items():
            # Create a subtle background for text readability
            bbox_props = dict(
                boxstyle="round,pad=0.3",
                facecolor="white",
                alpha=0.8,
                edgecolor="gray",
                linewidth=0.5,
            )

            plt.text(
                x,
                y,
                node,
                fontsize=self.font_size_nodes,
                ha="center",
                va="center",
                weight="bold",
                bbox=bbox_props,
            )

        # Draw edges with relationship-based styling
        self.draw_enhanced_edges(G, pos)

        # Create comprehensive legends
        self.create_enhanced_legends(group_colors)

        # Set title with improved typography
        plt.title(
            "Micronutrient Interaction Network\n(Grouped by Biological Function)",
            fontsize=self.font_size_title,
            weight="bold",
            pad=20,
            color="#2C3E50",
        )

        # Remove axes for cleaner look
        ax.set_xlim(-1.3, 1.3)
        ax.set_ylim(-1.3, 1.3)
        ax.axis("off")

        # Add subtle grid for reference (optional)
        # ax.grid(True, alpha=0.1, color='gray', linestyle='--')

        plt.tight_layout()
        return fig

    def draw_enhanced_edges(self, G: nx.DiGraph, pos: Dict) -> None:
        """
        Draw edges with enhanced styling based on relationship type and strength.

        Args:
            G: NetworkX graph
            pos: Node positions
        """
        # Group edges by relationship type for batch drawing
        inhibits_edges = []
        boosts_edges = []

        for u, v, data in G.edges(data=True):
            if data["relation"] == "inhibits":
                inhibits_edges.append((u, v, data))
            else:
                boosts_edges.append((u, v, data))

        # Draw inhibiting relationships (dashed red lines)
        for u, v, data in inhibits_edges:
            strength = data.get("strength", "medium")
            alpha = self.strength_alpha[strength]
            width = self.strength_weights[strength]

            nx.draw_networkx_edges(
                G,
                pos,
                edgelist=[(u, v)],
                style="dashed",
                edge_color="#E74C3C",
                connectionstyle=f"arc3,rad={self.connection_style_radius}",
                arrowstyle="-|>",
                arrowsize=15,
                width=width,
                alpha=alpha,
            )

            # Add relationship symbol
            self.add_edge_symbol(pos, u, v, "−", "#E74C3C")

        # Draw boosting relationships (solid green lines)
        for u, v, data in boosts_edges:
            strength = data.get("strength", "medium")
            alpha = self.strength_alpha[strength]
            width = self.strength_weights[strength]

            nx.draw_networkx_edges(
                G,
                pos,
                edgelist=[(u, v)],
                style="solid",
                edge_color="#27AE60",
                connectionstyle=f"arc3,rad={self.connection_style_radius}",
                arrowstyle="-|>",
                arrowsize=15,
                width=width,
                alpha=alpha,
            )

            # Add relationship symbol
            self.add_edge_symbol(pos, u, v, "+", "#27AE60")

    def add_edge_symbol(
        self, pos: Dict, u: str, v: str, symbol: str, color: str
    ) -> None:
        """
        Add symbolic representation on edges.

        Args:
            pos: Node positions
            u, v: Edge endpoints
            symbol: Symbol to display
            color: Symbol color
        """
        # Calculate midpoint with slight offset for curved edges
        x_mid = (pos[u][0] + pos[v][0]) / 2
        y_mid = (pos[u][1] + pos[v][1]) / 2

        # Add slight perpendicular offset for curved edge symbols
        dx = pos[v][0] - pos[u][0]
        dy = pos[v][1] - pos[u][1]
        length = np.sqrt(dx**2 + dy**2)

        if length > 0:
            # Perpendicular vector for offset
            offset_x = -dy / length * 0.05
            offset_y = dx / length * 0.05
            x_mid += offset_x
            y_mid += offset_y

        plt.text(
            x_mid,
            y_mid,
            symbol,
            fontsize=self.font_size_edges,
            ha="center",
            va="center",
            weight="bold",
            color=color,
            bbox=dict(
                boxstyle="circle,pad=0.2",
                facecolor="white",
                alpha=0.9,
                edgecolor=color,
                linewidth=1,
            ),
        )

    def create_enhanced_legends(self, group_colors: Dict) -> None:
        """
        Create comprehensive legends for the visualization.

        Args:
            group_colors: Group color mapping
        """
        # Functional group legend
        group_patches = [
            Patch(color=color, label=group) for group, color in group_colors.items()
        ]

        # Relationship type legend
        relationship_elements = [
            Line2D(
                [0],
                [0],
                linestyle="solid",
                linewidth=2.5,
                color="#27AE60",
                label="Enhances Absorption (+)",
            ),
            Line2D(
                [0],
                [0],
                linestyle="dashed",
                linewidth=2.5,
                color="#E74C3C",
                label="Inhibits Absorption (−)",
            ),
        ]

        # Strength legend
        strength_elements = [
            Line2D(
                [0],
                [0],
                linestyle="-",
                linewidth=3,
                color="gray",
                alpha=0.9,
                label="High Impact",
            ),
            Line2D(
                [0],
                [0],
                linestyle="-",
                linewidth=2,
                color="gray",
                alpha=0.7,
                label="Medium Impact",
            ),
            Line2D(
                [0],
                [0],
                linestyle="-",
                linewidth=1.5,
                color="gray",
                alpha=0.5,
                label="Low Impact",
            ),
        ]

        # Create multiple legend boxes
        legend1 = plt.legend(
            handles=group_patches,
            title="Functional Groups",
            loc="upper left",
            fontsize=self.font_size_legend,
            title_fontsize=self.font_size_legend + 1,
            framealpha=0.95,
            fancybox=True,
            shadow=True,
        )

        legend2 = plt.legend(
            handles=relationship_elements,
            title="Interaction Types",
            loc="upper right",
            fontsize=self.font_size_legend,
            title_fontsize=self.font_size_legend + 1,
            framealpha=0.95,
            fancybox=True,
            shadow=True,
        )

        legend3 = plt.legend(
            handles=strength_elements,
            title="Interaction Strength",
            loc="lower left",
            fontsize=self.font_size_legend,
            title_fontsize=self.font_size_legend + 1,
            framealpha=0.95,
            fancybox=True,
            shadow=True,
        )

        # Add legends back to the plot
        plt.gca().add_artist(legend1)
        plt.gca().add_artist(legend2)
        plt.gca().add_artist(legend3)

    def generate_visualization(
        self, filename: str = "enhanced_micronutrient_network.svg"
    ) -> str:
        """
        Generate the complete visualization and save to file.

        Args:
            filename: Output filename

        Returns:
            Path to saved file
        """
        logger.info("Starting visualization generation...")

        try:
            # Create color scheme
            node_colors, group_colors = self.create_color_scheme()

            # Build network graph
            G = self.build_network_graph()

            # Calculate layout
            pos = self.calculate_layout(G)

            # Create visualization
            fig = self.draw_enhanced_network(G, pos, node_colors, group_colors)

            # Save with high quality
            output_path = self.output_dir / filename
            plt.savefig(
                output_path,
                dpi=self.dpi,
                bbox_inches="tight",
                facecolor="white",
                edgecolor="none",
                format="png",
                transparent=False,
                pad_inches=0.1,
            )

            plt.close()

            logger.info(f"Visualization saved successfully: {output_path}")
            return str(output_path)

        except Exception as e:
            logger.error(f"Failed to generate visualization: {e}")
            raise

    def generate_analysis_report(self) -> Dict:
        """
        Generate a summary analysis of the network structure.

        Returns:
            Dictionary containing network analysis metrics
        """
        G = self.build_network_graph()

        analysis = {
            "total_nodes": G.number_of_nodes(),
            "total_edges": G.number_of_edges(),
            "density": nx.density(G),
            "avg_degree": sum(dict(G.degree()).values()) / G.number_of_nodes(),
            "inhibiting_interactions": sum(
                1 for _, _, d in G.edges(data=True) if d["relation"] == "inhibits"
            ),
            "boosting_interactions": sum(
                1 for _, _, d in G.edges(data=True) if d["relation"] == "boosts"
            ),
            "most_connected_nodes": sorted(
                dict(G.degree()).items(), key=lambda x: x[1], reverse=True
            )[:5],
            "groups": {group: len(nodes) for group, nodes in self.groups.items()},
        }

        return analysis


def main():
    """
    Main execution function.
    """
    try:
        # Initialize visualizer
        visualizer = MicronutrientNetworkVisualizer(output_dir="images")

        # Generate visualization
        output_path = visualizer.generate_visualization(
            "micronutrient_network_enhanced.png"
        )

        # Generate analysis report
        analysis = visualizer.generate_analysis_report()

        # Print summary
        print(f"\n{'='*60}")
        print("MICRONUTRIENT NETWORK ANALYSIS COMPLETE")
        print(f"{'='*60}")
        print(f"Output saved to: {output_path}")
        print(f"Total micronutrients analyzed: {analysis['total_nodes']}")
        print(f"Total interactions mapped: {analysis['total_edges']}")
        print(f"Inhibiting interactions: {analysis['inhibiting_interactions']}")
        print(f"Enhancing interactions: {analysis['boosting_interactions']}")
        print(f"Network density: {analysis['density']:.3f}")
        print(f"\nMost connected micronutrients:")
        for node, degree in analysis["most_connected_nodes"]:
            print(f"  • {node}: {degree} connections")
        print(f"{'='*60}")

        return output_path

    except Exception as e:
        logger.error(f"Execution failed: {e}")
        raise


if __name__ == "__main__":
    main()
