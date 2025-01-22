import pandas as pd
from pyvis.network import Network
import random

# search box html
custom_html = """
<input type="text" id="searchBox" placeholder="Search for a node..." onkeypress="checkEnter(event)">
<button onclick="clearSearch()">Clear</button>
<script>
    function checkEnter(event) {
        if (event.key === 'Enter') {
            searchNode();
        }
    }
    function searchNode() {
        var input = document.getElementById('searchBox').value.toLowerCase();
        var options = {
            scale: 1.5,
            animation: { duration: 1000, easingFunction: "easeInOutQuad" }
        };
        var nodes = network.body.data.nodes.get();
        var matchedNodes = nodes.filter(function(node) {
            return node.id.toLowerCase().includes(input);
        });
        if (matchedNodes.length > 0) {
            network.focus(matchedNodes[0].id, options);
        } else {
            alert("Node not found!");
        }
    }
    function clearSearch() {
        network.fit({ animation: { duration: 1000 } });
        document.getElementById('searchBox').value = '';
    }
</script>
"""

file_path = 'steam_friends.csv'
df = pd.read_csv(file_path)

df.columns = df.columns.str.strip()
df = df.rename(columns={'User': 'source', 'Friend': 'target'})

print("Renamed column names in the CSV:", df.columns.tolist())

net = Network(notebook=True, height='750px', width='100%', neighborhood_highlight=True)
net.show_buttons(filter_=['physics'])

color_dict = {}

def random_vibrant_color():
    return f'#{random.randint(0x660000, 0xFF9999):06x}'

for index, row in df.iterrows():
    source = str(row['source']).strip()
    target = str(row['target']).strip()

    if source not in color_dict:
        color_dict[source] = random_vibrant_color()
    
    net.add_node(source, color=color_dict[source])
    net.add_node(target, color='#FFDD99')  
    net.add_edge(source, target, color=color_dict[source])

net.force_atlas_2based()

output_file = 'entity_relationship_graph_vibrant_colors_highlight_search.html'
net.show(output_file)

with open(output_file, 'r') as file:
    html_content = file.read()

modified_html = html_content.replace('</body>', custom_html + '</body>')

with open(output_file, 'w') as file:
    file.write(modified_html)

print(f"Graph saved with search functionality: {output_file}")
