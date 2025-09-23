"""
Flask backend server for Art Gallery Problem solver
"""
import os
import base64
import io
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt

# Import our computational geometry modules
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.dcel import DCEL
from src.triangulation import triangulate_ear_clipping
from src.coloring import three_color_vertices, choose_guards_from_coloring
from src.utils import signed_area

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure matplotlib for web use
plt.style.use('default')
plt.rcParams['figure.figsize'] = (10, 8)
plt.rcParams['font.size'] = 10

@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    return send_from_directory('../frontend', filename)

@app.route('/api/solve', methods=['POST'])
def solve_art_gallery():
    """
    Solve the Art Gallery Problem for a given polygon
    
    Expected JSON payload:
    {
        "vertices": [[x1, y1], [x2, y2], ...],
        "name": "Polygon Name" (optional)
    }
    
    Returns:
    {
        "success": true,
        "data": {
            "vertices": [...],
            "triangles": [...],
            "colors": {...},
            "guards": [...],
            "stats": {
                "num_vertices": int,
                "num_triangles": int,
                "num_guards": int
            },
            "plot_base64": "base64_encoded_image"
        }
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'vertices' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing vertices data'
            }), 400
        
        vertices = data['vertices']
        polygon_name = data.get('name', 'Custom Polygon')
        
        # Validate input
        if len(vertices) < 3:
            return jsonify({
                'success': False,
                'error': 'Polygon must have at least 3 vertices'
            }), 400
        
        # Check if polygon is simple (basic check)
        if len(vertices) != len(set(tuple(v) for v in vertices)):
            return jsonify({
                'success': False,
                'error': 'Polygon has duplicate vertices'
            }), 400
        
        # Convert to tuples (keep canvas coordinates)
        points = [(float(x), float(y)) for x, y in vertices]
        
        # Ensure polygon is in CCW order (in canvas coordinate system)
        from src.utils import signed_area
        area = signed_area(points)
        print(f"Debug - Polygon area: {area} (negative = CW, positive = CCW)")
        
        if area > 0:  # In canvas coordinates, positive area means CW
            # Reverse the order to make it CCW
            points = list(reversed(points))
            print("Debug - Reversed polygon order to make it CCW")
        else:
            print("Debug - Polygon is already CCW")
        
        print(f"Debug - Final points: {points}")
        
        # Run the Art Gallery algorithm
        dcel = DCEL.from_polygon(points)
        triangles = triangulate_ear_clipping(dcel)
        colors = three_color_vertices(triangles)
        guards = choose_guards_from_coloring(colors)
        
        print(f"Debug - Generated {len(triangles)} triangles")
        print(f"Debug - Triangle indices: {triangles}")
        
        # Generate step-by-step visualizations
        visualizations = generate_step_visualizations(dcel, triangles, colors, guards, polygon_name)
        print(f"Generated {len(visualizations)} visualization steps")
        
        # Prepare response data (already in canvas coordinates)
        result = {
            'success': True,
            'data': {
                'vertices': points,
                'triangles': triangles,
                'colors': colors,
                'guards': guards,
                'stats': {
                    'num_vertices': len(points),
                    'num_triangles': len(triangles),
                    'num_guards': len(guards)
                },
                'visualizations': visualizations
            }
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Processing error: {str(e)}'
        }), 500

@app.route('/api/examples', methods=['GET'])
def get_examples():
    """Get example polygons for demonstration"""
    examples = {
        'simple_triangle': {
            'name': 'Simple Triangle',
            'vertices': [[100, 300], [300, 300], [200, 100]]
        },
        'square': {
            'name': 'Square',
            'vertices': [[100, 300], [300, 300], [300, 100], [100, 100]]
        },
        'pentagon': {
            'name': 'Pentagon',
            'vertices': [
                [200, 350], [320, 280], [280, 150], [120, 150], [80, 280]
            ]
        },
        'l_shape': {
            'name': 'L-Shape',
            'vertices': [
                [100, 300], [300, 300], [300, 250], [150, 250], [150, 100], [100, 100]
            ]
        },
        'complex_polygon': {
            'name': 'Complex Polygon',
            'vertices': [
                [100, 300], [350, 300], [350, 250], [250, 250], [250, 150], [150, 150], [150, 250], [100, 250]
            ]
        }
    }
    
    return jsonify({
        'success': True,
        'examples': examples
    })

def generate_step_visualizations(dcel, triangles, colors, guards, title):
    """Generate step-by-step visualizations"""
    try:
        # Use coordinates directly from DCEL (already in canvas coordinate system)
        pts = dcel.coords_list()
        cmap = ['#FF6B6B', '#4ECDC4', '#45B7D1']  # Red, Teal, Blue
        visualizations = {}
        
        # Debug: Print the data we're working with
        print(f"Debug - Points: {pts}")
        print(f"Debug - Triangles: {triangles}")
        print(f"Debug - Colors: {colors}")
        print(f"Debug - Guards: {guards}")
        
        # Step 1: Original Polygon
        fig, ax = plt.subplots(figsize=(10, 8))
        poly_idx = dcel.boundary_vertex_indices()
        poly_coords = [pts[i] for i in poly_idx] + [pts[poly_idx[0]]]
        ax.plot([p[0] for p in poly_coords], [p[1] for p in poly_coords], 
                '-k', linewidth=3, label='Polygon Boundary')
        
        # Draw vertices
        for i, (x, y) in enumerate(pts):
            ax.scatter(x, y, s=120, c='#666', marker='o', zorder=5, edgecolors='white', linewidth=2)
            ax.text(x + 0.05, y + 0.05, f'{i}', fontsize=12, fontweight='bold', color='white')
        
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        ax.set_title(f'Step 1: Original Polygon\n{title} ({len(pts)} vertices)', fontsize=14, fontweight='bold')
        ax.set_xlabel('X', fontsize=12)
        ax.set_ylabel('Y', fontsize=12)
        
        visualizations['step1_polygon'] = save_fig_to_base64(fig)
        plt.close(fig)
        
        # Step 2: Triangulation
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.plot([p[0] for p in poly_coords], [p[1] for p in poly_coords], 
                '-k', linewidth=3, label='Polygon Boundary')
        
        # Draw triangulation lines (internal edges only)
        for tri in triangles:
            # Draw each edge of the triangle
            tri_pts = [pts[i] for i in tri]
            for i in range(3):
                p1 = tri_pts[i]
                p2 = tri_pts[(i + 1) % 3]
                ax.plot([p1[0], p2[0]], [p1[1], p2[1]], 
                        '--', color='#888', linewidth=1.5, alpha=0.8)
        
        # Draw vertices
        for i, (x, y) in enumerate(pts):
            ax.scatter(x, y, s=120, c='#666', marker='o', zorder=5, edgecolors='white', linewidth=2)
            ax.text(x + 0.05, y + 0.05, f'{i}', fontsize=12, fontweight='bold', color='white')
        
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        ax.set_title(f'Step 2: Triangulation\n{len(triangles)} triangles created', fontsize=14, fontweight='bold')
        ax.set_xlabel('X', fontsize=12)
        ax.set_ylabel('Y', fontsize=12)
        
        visualizations['step2_triangulation'] = save_fig_to_base64(fig)
        plt.close(fig)
        
        # Step 3: Three-Coloring
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.plot([p[0] for p in poly_coords], [p[1] for p in poly_coords], 
                '-k', linewidth=3, label='Polygon Boundary')
        
        # Draw triangulation (light background)
        for tri in triangles:
            tri_pts = [pts[i] for i in tri]
            for i in range(3):
                p1 = tri_pts[i]
                p2 = tri_pts[(i + 1) % 3]
                ax.plot([p1[0], p2[0]], [p1[1], p2[1]], 
                        '--', color='lightgray', linewidth=1, alpha=0.5)
        
        # Draw colored vertices
        for v_idx, col in colors.items():
            ax.scatter(pts[v_idx][0], pts[v_idx][1], 
                      s=120, c=cmap[col], marker='o', 
                      zorder=5, edgecolors='black', linewidth=2)
            ax.text(pts[v_idx][0] + 0.05, pts[v_idx][1] + 0.05, 
                   f'{v_idx}', fontsize=12, fontweight='bold', color='white')
        
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        ax.set_title(f'Step 3: Three-Coloring\n{len(colors)} vertices colored', fontsize=14, fontweight='bold')
        ax.set_xlabel('X', fontsize=12)
        ax.set_ylabel('Y', fontsize=12)
        
        # Add color legend
        legend_elements = [
            plt.scatter([], [], c=cmap[0], marker='o', s=120, label='Color 0'),
            plt.scatter([], [], c=cmap[1], marker='o', s=120, label='Color 1'),
            plt.scatter([], [], c=cmap[2], marker='o', s=120, label='Color 2')
        ]
        ax.legend(handles=legend_elements, loc='upper right')
        
        visualizations['step3_coloring'] = save_fig_to_base64(fig)
        plt.close(fig)
        
        # Step 4: Final Solution
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.plot([p[0] for p in poly_coords], [p[1] for p in poly_coords], 
                '-k', linewidth=3, label='Polygon Boundary')
        
        # Draw triangulation (light background)
        for tri in triangles:
            tri_pts = [pts[i] for i in tri]
            for i in range(3):
                p1 = tri_pts[i]
                p2 = tri_pts[(i + 1) % 3]
                ax.plot([p1[0], p2[0]], [p1[1], p2[1]], 
                        '--', color='lightgray', linewidth=1, alpha=0.5)
        
        # Draw colored vertices
        for v_idx, col in colors.items():
            ax.scatter(pts[v_idx][0], pts[v_idx][1], 
                      s=120, c=cmap[col], marker='o', 
                      zorder=5, edgecolors='black', linewidth=2)
            ax.text(pts[v_idx][0] + 0.05, pts[v_idx][1] + 0.05, 
                   f'{v_idx}', fontsize=12, fontweight='bold', color='white')
        
        # Draw guards
        for g in guards:
            ax.scatter(pts[g][0], pts[g][1], 
                      s=250, marker='*', c='gold', 
                      edgecolors='black', linewidth=3, zorder=6)
            ax.text(pts[g][0] + 0.1, pts[g][1] + 0.1, 
                   'GUARD', fontsize=10, fontweight='bold', color='darkred')
        
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        ax.set_title(f'Step 4: Final Solution\n{len(guards)} guards placed optimally', fontsize=14, fontweight='bold')
        ax.set_xlabel('X', fontsize=12)
        ax.set_ylabel('Y', fontsize=12)
        
        # Add complete legend
        legend_elements = [
            plt.Line2D([0], [0], color='black', linewidth=3, label='Boundary'),
            plt.Line2D([0], [0], color='lightgray', linestyle='--', label='Triangulation'),
            plt.scatter([], [], c=cmap[0], marker='o', s=120, label='Color 0'),
            plt.scatter([], [], c=cmap[1], marker='o', s=120, label='Color 1'),
            plt.scatter([], [], c=cmap[2], marker='o', s=120, label='Color 2'),
            plt.scatter([], [], c='gold', marker='*', s=250, label='Guards')
        ]
        ax.legend(handles=legend_elements, loc='upper right')
        
        visualizations['step4_solution'] = save_fig_to_base64(fig)
        plt.close(fig)
        
        return visualizations
        
    except Exception as e:
        print(f"Error generating step visualizations: {e}")
        return {}

def save_fig_to_base64(fig):
    """Save matplotlib figure to base64 string"""
    try:
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        return image_base64
    except Exception as e:
        print(f"Error saving figure to base64: {e}")
        return None

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
