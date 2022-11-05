# Cracking the blackbox of deep sequence-based protein-protein interaction prediction

This repository contains all datasets and code used to show that 
sequence-based deep PPI prediction methods only achieve phenomenal 
results due to data leakage and learning from sequence similarities
and node degrees. 

![alt text](Overview%20Figure%20Results.png)

## Datasets
The original **Guo** and **Huang** datasets were obtained from `DeepFE` 
and can be found either in their [GitHub Repository](https://github.com/xal2019/DeepFE-PPI/tree/master/dataset) 
or under [`algorithms/DeepFE-PPI/dataset/11188/`](algorithms/DeepFE-PPI/dataset/11188/) (**Guo**) and [`algorithms/DeepFE-PPI/dataset/human/`](algorithms/DeepFE-PPI/dataset/human/) (**Huang**). 
The **Guo** dataset can also be found in the [PIPR respository](https://github.com/muhaochen/seq_ppi/tree/master/yeast/preprocessed) 
or under [`algorithms/seq_ppi/yeast/preprocessed/`](algorithms/seq_ppi/yeast/preprocessed/). 

The original **Du** dataset was obtained from the [original publication](https://pubs.acs.org/doi/full/10.1021/acs.jcim.7b00028) 
and can be found under [`Datasets_PPIs/Du_yeast_DIP/`](Datasets_PPIs/Du_yeast_DIP/).

The **Pan** dataset can be obtained from the [original publication](http://www.csbio.sjtu.edu.cn/bioinf/LR_PPI/Data.htm) 
and from the [PIPR Repository](https://github.com/muhaochen/seq_ppi/tree/master/sun/preprocessed). 
It is in [`algorithms/seq_ppi/sun/preprocessed/`](algorithms/seq_ppi/sun/preprocessed/). 

The **Richoux** datasets were obtained from their [Gitlab](https://gitlab.univ-nantes.fr/richoux-f/DeepPPI/-/tree/master/data).
The **regular** dataset is in [`algorithms/DeepPPI/data/mirror/`](algorithms/DeepPPI/data/mirror/), the **strict** one in
[`algorithms/DeepPPI/data/mirror/double/`](algorithms/DeepPPI/data/mirror/double/). 

All original datasets were rewritten into the format used by SPRINT and split 
into train and test with [`algorithms/SPRINT/create_SPRINT_datasets.py`](algorithms/SPRINT/create_SPRINT_datasets.py).
They are in in [`algorithms/SPRINT/data/original`](algorithms/SPRINT/data/original).
This script was also used to **rewire** and split the datasets (`generate_RDPN`) (-> [`algorithms/SPRINT/data/rewired`](algorithms/SPRINT/data/rewired)).

### Partitions

The [human](Datasets_PPIs/SwissProt/human_swissprot.fasta) and [yeast](Datasets_PPIs/SwissProt/yeast_swissprot.fasta) proteomes were downloaded from Uniprot and sent to the 
team of SIMAP2. They sent back the similarity data which we make available under
[https://syncandshare.lrz.de/getlink/fi5AJEoSLB1DrXjxAzBne7/](https://syncandshare.lrz.de/getlink/fi5AJEoSLB1DrXjxAzBne7/) (`submatrix.tsv.gz`). 

We preprocessed this data in order to give it to the KaHIP kaffpa algorithm with [simap_preprocessing.py](simap_preprocessing.py):

1. We separated the file to obtain only human-human and yeast-yeast protein similarities
2. We converted the edge lists to networks and converted the Uniprot node labels to integer labels because KaHIP needs `METIS` files as input. These files can only handle integer node labels
3. We exported the networks as `METIS` files with bitscores as edge weights: [human](network_data/SIMAP2/human_networks/only_human_bitscore.graph), [yeast](network_data/SIMAP2/yeast_networks/only_yeast_bitscore.graph)

We fed these to the KaHIP kaffpa algorithm with the following commands: 
```
./KaHIP/deploy/kaffpa ./network_data/SIMAP2/human_networks/only_human_bitscore.graph --seed=1234 --output_filename="./network_data/SIMAP2/human_networks/only_human_partition_bitscore.txt" --k=2 --preconfiguration=strong
./KaHIP/deploy/kaffpa ./network_data/SIMAP2/yeast_networks/only_yeast_bitscore.graph --seed=1234 --output_filename="./network_data/SIMAP2/yeast_networks/only_yeast_partition_bitscore.txt" --k=2 --preconfiguration=strong
```

The output files containing the partitioning was mapped back to the original UniProt IDs in [kahip.py](kahip.py). Nodelists: [human](network_data/SIMAP2/human_networks/only_human_partition_nodelist.txt), [yeast](network_data/SIMAP2/yeast_networks/only_yeast_partition_nodelist.txt).

The PPIs from the 6 original datasets were then split according to the KaHIP partitions into blocks
Inter, Intra-0, and Intra-1 with [rewrite_datasets.py](rewrite_datasets.py) and are in [`algorithms/SPRINT/data/partitions`](algorithms/SPRINT/data/partitions).

## Methods

### Custom baseline ML methods
Our 6 implemented baseline ML methods are implemented in [`algorithms/Custom/`](algorithms/Custom). 

1. We converted the SIMAP2 similarity table into an all-against-all similarity matrix in [`algorithms/Custom/compute_sim_matrix.py`](algorithms/Custom/compute_sim_matrix.py).
2. We reduced the dimensionality of this matrix via PCA, MDS, and node2vec in [`algorithms/Custom/compute_dim_red.py`](algorithms/Custom/compute_dim_red.py):
   1. PCA [human](algorithms/Custom/data/human_pca.npy), [yeast](algorithms/Custom/data/yeast_pca.npy)
   2. MDS [human](algorithms/Custom/data/human_mds.npy), [yeast](algorithms/Custom/data/yeast_mds.npy)
   3. For node2vec, we first converted the similarity matrix into a network and exported its edgelist ([human](algorithms/Custom/data/human.edgelist), [yeast](algorithms/Custom/data/yeast.edgelist)) and nodelist ([human](algorithms/Custom/data/human.nodelist), [yeast](algorithms/Custom/data/yeast.nodelist)). Then, we called node2vec with


```
cd snap/examples/node2vec
./node2vec -i:../../../algorithms/Custom/data/yeast.edgelist -o:../../../algorithms/Custom/data/yeast.emb
./node2vec -i:../../../algorithms/Custom/data/human.edgelist -o:../../../algorithms/Custom/data/human.emb
```
The RF and SVM are implemented in [algorithms/Custom/learn_models.py](algorithms/Custom/learn_models.py). 
All tests are executed in [algorithms/Custom/run.py](algorithms/Custom/run.py).
Results were saved to the [results folder](algorithms/Custom/results).
### DeepFE
The code was pulled from their [GitHub Repository](https://github.com/xal2019/DeepFE-PPI/) and updated to the current tensorflow version.
All tests are run via [the shell slurm script](algorithms/DeepFE-PPI/run_DeepFE.sh) or [algorithms/DeepFE-PPI/train_all_datasets.py](algorithms/DeepFE-PPI/train_all_datasets.py).
Results were saved to the [results folder](algorithms/DeepFE-PPI/result).

### Richoux-FC and Richoux-LSTM
The code was pulled from their [Gitlab Repository](https://gitlab.univ-nantes.fr/richoux-f/DeepPPI). 
All tests can be run via [the shell slurm script](algorithms/DeepPPI/keras/run_DeepPPI.sh) or [algorithms/DeepPPI/keras/train_all_datasets.py](algorithms/DeepPPI/keras/train_all_datasets.py).
Results were saved to the [results folder](algorithms/DeepPPI/keras/results_custom).

### PIPR
The code was pulled from their [GitHub Repository](https://github.com/muhaochen/seq_ppi) and updated to the current tensorflow version.
All tests are run via [the shell slurm script](algorithms/seq_ppi/binary/model/lasagna/run_PIPR.sh) or [algorithms/seq_ppi/binary/model/lasagna/train_all_datasets.py](algorithms/seq_ppi/binary/model/lasagna/train_all_datasets.py).
Results were saved to the [results folder](algorithms/seq_ppi/binary/model/lasagna/results).

### SPRINT
The code was pulled from their [GitHub Repository](https://github.com/lucian-ilie/SPRINT). 
The yeast proteome fasta file was first transformed such that each sequence only occupies one line [rewrite_yeast_fasta.py](algorithms/SPRINT/rewrite_yeast_fasta.py).
Then, the proteome was preprocessed with [compute_yeast_HSPs.sh](algorithms/SPRINT/compute_yeast_HSPs.sh).
The preprocessed human proteome was downloaded from the [SPRINT website](https://www.csd.uwo.ca/~ilie/SPRINT/). 
Then tests are run via shell slurm scripts: [original](algorithms/SPRINT/run_SPRINT_original.sh), [rewired](algorithms/SPRINT/run_SPRINT_rewired.sh), [partitions](algorithms/SPRINT/run_SPRINT_custom.sh).
Results were saved to the [results folder](algorithms/SPRINT/results).
AUCs and AUPRs were calculated with [algorithms/SPRINT/results/calculate_scores.py](algorithms/SPRINT/results/calculate_scores.py).

## Visualizations
All visualizations were made with the R scripts in [visualizations](visualizations).
Plots were saved to [visualizations/plots](visualizations/plots).





