#!/usr/bin/env python

import csv
import argparse
import os.path
from tqdm import tqdm
from pyvis.network import Network


def extractDataFromCSV(source_csv, fist_line_is_header):
    sources = []
    targets = []
    weights = []
    with open(source_csv) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        flag_reading_first_line = True
        for row in tqdm(csv_reader, desc="Reading data"):
            if flag_reading_first_line and fist_line_is_header:
               flag_reading_first_line = False
            else:
                sources.append(row[0])
                targets.append(row[1])
                weights.append(1)
    return zip(sources, targets, weights)


def plot(source_csv, result_file_name, fist_line_is_header, settings_mode):
    
    got_net = Network(height="100%", width="100%", bgcolor="#222222", font_color="white")
    if settings_mode:
        got_net.show_buttons()
    got_net.set_options('''
                        var options = {
                          "nodes": {
                            "physics": false
                          },
                          "edges": {
                            "arrows": {
                              "to": {
                                "enabled": true,
                                "scaleFactor": 0.75
                              }
                            },
                            "color": {
                              "inherit": true
                            },
                            "physics": false,
                            "smooth": false
                          },
                          "layout": {
                            "hierarchical": {
                              "enabled": true
                            }
                          },
                          "configure": {
                            "enabled": ''' + str(settings_mode).lower() +'''
                          },  
                          "physics": {
                            "enabled": false,
                            "hierarchicalRepulsion": {
                              "centralGravity": 0
                            },
                            "minVelocity": 0.75,
                            "solver": "hierarchicalRepulsion"
                          }
                        }''')


    
    edge_data = extractDataFromCSV(source_csv, fist_line_is_header)
    for e in tqdm(edge_data, desc="Ectracting data"):
        src = e[0]
        dst = e[1]
    
        got_net.add_node(src, src, title="<strong>" + src)
        got_net.add_node(dst, dst, title="<strong>" + dst + "</strong>")
        got_net.add_edge(src, dst, color = "red")
    
    neighbor_map = got_net.get_adj_list()
    
    
    # add neighbor data to node hover data
    for node in tqdm(got_net.nodes, desc = "Parsing data"):
        node["title"] += " Neighbors:</strong><br><ul><li>" + "</li><li>".join(neighbor_map[node["id"]]) + "</li></ul>"
        node["value"] = len(neighbor_map[node["id"]])
    
    
    got_net.show(str(result_file_name) + ".html")

def main():
    if __status__ == "Prototype":
        print("\nTHIS SCRIPT HAS THE STATE 'PROTOTYPE'!\n")
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-V","-v", "--version", help="show program version", action="store_true")
    parser.add_argument("-d", "--data", default="./exampledata/datasmall.csv", help="CSV containing data")
    parser.add_argument("-o", "--out", default="", help="Output path (DEFAULT: ./)")
    parser.add_argument("-n", "--name", default="Visualisation", help="Name of the plot")
    parser.add_argument("-C","-c", "--csvheader", help="FLAG: First line in CSV file contains header" , action="store_true")
    parser.add_argument("-S","-s", "--settings", help="FLAG: Display settings in HTML file" , action="store_true")
    # read arguments from the command line
    args = parser.parse_args()

    # check for --version or -V
    if args.version:
        print(__version__)
    else:
        if(os.path.isfile(args.data)):
            plot(source_csv = args.data, result_file_name = args.name, fist_line_is_header = args.csvheader, settings_mode = args.settings)
        else:
            print("ERROR: Source file not found! Param: "+ args.data)


if __name__ == '__main__':
    main()