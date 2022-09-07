# Fibrils
Project Fibrils

# Description
We proposed a new classifier, called ENTAIL, for the prediction of fibril deposits involved in the amyloidoses. We aggregated the sequences from four datasets: AmyLoad, WALTZ-DB 2.0, Pep424 and AmyPro. We removed all the redundant sequences obtaining a complete set composed of 1897 sequences (788 amyloid peptides and 1109 non-amyloid peptides). For subsequent analyzes, we used a balanced dataset consisting of these sequences. We have selected the 4125 sequence descriptors from iFeature. The script rebuild all.py can be used to accomplish the descriptor extraction.
All the used datasets are into the files TrainingSet.txt and TestSet.txt. 
 ENTAIL was based on the Naive Bayes Classifier with Unbounded Support and Gaussian Kernel Type. We reached an accuracy on the test set of 81.80%, SN of 100%, SP of 63.63% and an MCC of 0.683 on the balanced dataset. 


# Step 0
# Step 1

Please note that the sequence STVIIR have no predicted structure then it was removed from balanced dataset that uses YPredStuct descriptors


TODO:
Build a docking based classifier
