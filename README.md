# 🎨 Art Gallery Problem Solver

An interactive web application that solves the Art Gallery Problem using computational geometry algorithms. This project implements the classic ear-clipping triangulation and three-coloring approach to find optimal guard placement.

## 🌟 Features

- **Interactive Polygon Drawing**: Draw custom polygons by clicking on a canvas
- **Example Polygons**: Try pre-defined shapes like triangles, squares, and complex polygons
- **Real-time Visualization**: See triangulation, vertex coloring, and guard placement
- **Algorithm Information**: Learn about the Art Gallery Theorem and implementation details
- **Responsive Design**: Works on desktop and mobile devices

## 🚀 Quick Start

### Option 1: Easy Startup (Recommended)
```bash
python run_server.py
```

### Option 2: Manual Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Start the server
cd backend
python app.py
```

Then open your browser and go to: **http://localhost:5000**

## 🎯 How to Use

1. **Draw a Polygon**: Click on the canvas to place vertices
2. **Close Polygon**: Click "Close Polygon" when finished
3. **Solve**: Click "Solve Art Gallery Problem" to find optimal guards
4. **Explore**: Try the example polygons or draw your own

## 🧮 Algorithm Details

### Art Gallery Theorem
Any simple polygon with n vertices can be guarded by at most ⌊n/3⌋ guards.

### Implementation Steps
1. **Triangulation**: Use ear-clipping algorithm to decompose the polygon into triangles
2. **Three-coloring**: Color vertices using BFS on the dual graph of triangles
3. **Guard Selection**: Choose guards from the smallest color class (optimal strategy)

### Complexity
- **Time**: O(n²) for ear-clipping triangulation
- **Space**: O(n) for DCEL structure

## 📁 Project Structure

```
Art_Gallery_Problem/
├── backend/
│   └── app.py              # Flask API server
├── frontend/
│   └── index.html          # Interactive web interface
├── src/
│   ├── dcel.py             # Doubly Connected Edge List
│   ├── triangulation.py    # Ear-clipping algorithm
│   ├── coloring.py         # Three-coloring algorithm
│   ├── dual_graph.py       # Triangle adjacency graph
│   ├── plotting.py         # Visualization functions
│   ├── io_utils.py         # JSON I/O utilities
│   └── utils.py            # Geometric utilities
├── main.py                 # Original command-line interface
├── run_server.py           # Web server startup script
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🔧 API Endpoints

### POST /api/solve
Solve the Art Gallery Problem for a given polygon.

**Request:**
```json
{
    "vertices": [[x1, y1], [x2, y2], ...],
    "name": "Polygon Name"
}
```

**Response:**
```json
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
            "num_guards": int,
            "polygon_area": float
        },
        "plot_base64": "base64_encoded_image"
    }
}
```

### GET /api/examples
Get example polygons for demonstration.

## 🛠️ Dependencies

### Core
- **numpy**: Numerical computations
- **matplotlib**: Visualization and plotting
- **shapely**: Geometric operations and validation

### Web Framework
- **flask**: Web server framework
- **flask-cors**: Cross-origin resource sharing

### Graph Operations
- **networkx**: Dual graph construction and operations

### Development
- **pytest**: Testing framework
- **black**: Code formatting
- **flake8**: Linting

## 🎨 Web Interface Features

### Interactive Canvas
- Click to place polygon vertices
- Visual feedback with vertex numbering
- Grid background for precision
- Clear and close polygon controls

### Example Polygons
- Simple Triangle
- Square
- Pentagon
- L-Shape
- Complex Polygon

### Results Visualization
- Triangulation display
- Three-color vertex coloring
- Guard placement (gold stars)
- Statistics panel

## 🔬 Computational Geometry Components

### DCEL (Doubly Connected Edge List)
- Minimal DCEL for simple polygon representation
- Vertex, HalfEdge, and Face classes
- Boundary traversal and coordinate extraction

### Triangulation
- Ear-clipping algorithm implementation
- Handles counter-clockwise orientation
- Numerical stability with epsilon comparisons
- Fallback for degenerate cases

### Three-Coloring
- BFS-based coloring on triangle dual graph
- Optimal guard selection from smallest color class
- Handles disconnected triangulations

## 🧪 Testing

Run the test suite:
```bash
pytest
```

## 📚 References

- Chvátal, V. (1975). "A combinatorial theorem in plane geometry"
- Fisk, S. (1978). "A short proof of Chvátal's watchman theorem"
- de Berg, M., et al. (2008). "Computational Geometry: Algorithms and Applications"

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Computational geometry community for algorithms and research
- Flask and matplotlib communities for excellent libraries
- All contributors and users of this project
