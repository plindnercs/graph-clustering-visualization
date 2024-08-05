Steps to create dummy community:
1) Create dummy_communities.metis manually or with script
2) Create pairs_to_compare file by: "python3 graph-clustering-3d-histogram-member-overlap-parallel.py dummy_communities.metis"
3) Create overlap triples file by: "python3 graph-clustering-3d-histogram-visualization.py pairs_to_compare_file dummy_communities.metis false"
4) Now we can use the community file and triples file to do random matching etc.
