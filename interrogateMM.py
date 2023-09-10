import sys
from freeplane import Mindmap

def gather_statistics(mindmap_name):
    # Load the mind map
    mindmap = Mindmap(mindmap_name)
    
    # Extract statistics
    num_of_nodes = len(mindmap.find_nodes())
    root_node = mindmap.rootnode()
    num_of_branches = len(root_node.branches)
    
    # Display the statistics
    print(f"Statistics for mind map: {mindmap_name}")
    print(f"Number of nodes: {num_of_nodes}")
    print(f"Number of branches: {num_of_branches}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the name of the mind map as an argument.")
        sys.exit(1)
    
    mindmap_name = sys.argv[1]
    gather_statistics(mindmap_name)
