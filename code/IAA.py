# -*- coding: utf-8 -*-
import json
import numpy as np
import krippendorff
import copy
import seaborn as sn
import pandas as pd
import matplotlib.pyplot as plt

confusion_matrix = {
		"exact": {"exact": 0, "related": 0, "none": 0, "narrower": 0, "broader": 0},
		"related": {"exact": 0, "related": 0, "none": 0, "narrower": 0, "broader": 0},
		"none": {"exact": 0, "related": 0, "none": 0, "narrower": 0, "broader": 0},
		"narrower": {"exact": 0, "related": 0, "none": 0, "narrower": 0, "broader": 0},
		"broader": {"exact": 0, "related": 0, "none": 0, "narrower": 0, "broader": 0}
		}

def calculate_groupe_1(directory, print_confusion_matrix=False, plot_confusion_matrix=True, is_binary=False):
	print("Annotators: Mathieu, Hee-Soo, Bruno")

	conf_matrix_1, conf_matrix_2, conf_matrix_3 = copy.deepcopy(confusion_matrix), \
												copy.deepcopy(confusion_matrix), \
												copy.deepcopy(confusion_matrix)

	with open(directory + "_MC.tsv") as f:
		ann_1 = f.read().split("\n")[1:]

	with open(directory + "_BG.tsv") as f:
		ann_2 = f.read().split("\n")[1:]

	with open(directory + "_HS.tsv") as f:
		ann_3 = f.read().split("\n")[1:]

	print("number of annotated entries: ", len(ann_1), len(ann_1) == len(ann_2) == len(ann_3))
	coder_1, coder_2, coder_3 = list(), list(), list()

	if is_binary:
		print("Binary relations")
		relations = {"none":0, "exact": 1, "related": 1, "narrower": 1, "broader": 1}
	else:
		relations = {"none":0, "exact": 1, "related": 2, "narrower": 3, "broader": 4}
	for i, j, k in zip(ann_1, ann_2, ann_3):
		if len(i.split("\t")[3]):
			coder_1.append(relations[i.split("\t")[3]])
			coder_2.append(relations[j.split("\t")[3]])
			coder_3.append(relations[k.split("\t")[3]])

			# row : MC, columns: BG
			conf_matrix_1[i.split("\t")[3]][j.split("\t")[3]] += 1
			# row : MC, columns: HS
			conf_matrix_2[i.split("\t")[3]][k.split("\t")[3]] += 1
			# row : BG, columns: HS
			conf_matrix_3[j.split("\t")[3]][k.split("\t")[3]] += 1

	if print_confusion_matrix:
		print("confusion_matrix_1 (row : MC, columns: BG) \n", conf_matrix_1)
		print("confusion_matrix_2 (row : MC, columns: HS) \n", conf_matrix_2)
		print("confusion_matrix_3 (row : BG, columns: HS) \n", conf_matrix_3)

	if plot_confusion_matrix:
		for matrix, name in zip([conf_matrix_1, conf_matrix_2, conf_matrix_3], ["MC_BG", "MC_HS", "BG_HS"]):
			df_cm = pd.DataFrame([list(i.values()) for i in list(matrix.values())],\
														index = list(relations.keys()),\
														columns = list(relations.keys()))

			# plt.figure(figsize = (10,10), frameon=False)#figsize = (10,7))
			if is_binary:
				name = directory.split("/")[-1] + "_binary_" + name
			else:
				name = directory.split("/")[-1] + "_five_" + name
			fig, ax = plt.subplots(figsize=(5, 5))
			plt.title(name)
			ax = sn.heatmap(df_cm, linewidth=0.5, annot=True, ax=ax)
			fig.savefig('%s.png'%name)

	res = krippendorff.alpha([coder_1, coder_2, coder_3])
	print("krippendorff\'s alpha is :", res)
	return [coder_1, coder_2, coder_3]


def calculate_groupe_2(directory, print_confusion_matrix=False, plot_confusion_matrix=True, is_binary=False):
	print("Annotators: Karen & Sina")

	conf_matrix = copy.deepcopy(confusion_matrix)

	with open(directory + "_SA.tsv") as f:
		ann_1 = f.read().split("\n")[1:]

	with open(directory + "_KF.tsv") as f:
		ann_2 = f.read().split("\n")[1:]

	print("number of annotated entries: ", len(ann_1), len(ann_1) == len(ann_2))

	coder_1, coder_2 = list(), list()

	if is_binary:
		print("Binary relations")
		relations = {"none":0, "exact": 1, "related": 1, "narrower": 1, "broader": 1}
	else:
		relations = {"none":0, "exact": 1, "related": 2, "narrower": 3, "broader": 4}

	for i, j in zip(ann_1, ann_2):
		if len(i.split("\t")[3]):
			coder_1.append(relations[i.split("\t")[3]])
			coder_2.append(relations[j.split("\t")[3]])
			
			# row : SA, columns: KF
			conf_matrix[i.split("\t")[3]][j.split("\t")[3]] += 1

	if print_confusion_matrix:
		print("confusion_matrix_1 (row : SA, columns: KF) \n", conf_matrix)

	if plot_confusion_matrix:
		df_cm = pd.DataFrame([list(i.values()) for i in list(conf_matrix.values())],\
													index = list(relations.keys()),\
													columns = list(relations.keys()))

		if is_binary:
			name = directory.split("/")[-1] + "_binary_SK"
		else:
			name = directory.split("/")[-1] + "_five_SK"

		plt.figure(figsize = (10,10), frameon=False)
		fig, ax = plt.subplots(figsize=(5, 5))
		plt.title(name)
		ax = sn.heatmap(df_cm, linewidth=0.5, annot=True, ax=ax)
		fig.savefig('%s.png'%name)

	res = krippendorff.alpha([coder_1, coder_2])
	print("krippendorff\'s alpha is :", res)
	return [coder_1, coder_2]

print("\nBatch 1 - Group 1 - 5-class =============")
directory = "../output/annotation/Final/Group_1_Batch_1"
m_1 = calculate_groupe_1(directory)

print("\nBatch 1 - Group 1 - 2-class =============")
m_1 = calculate_groupe_1(directory, is_binary=True)
# # print(m_1)

print("\nBatch 2 - Group 1 - 5-class =============")
directory = "../output/annotation/Final/Group_1_Batch_2"
m_1 = calculate_groupe_1(directory)

print("\nBatch 2 - Group 1 - 2-class =============")
m_1 = calculate_groupe_1(directory, is_binary=True)
# # print(m_1)

print("\n\n")

print("\nBatch 1 - Group 2 - 5-class =============")
directory = "../output/annotation/Final/Group_2_Batch_1"
m_2 = calculate_groupe_2(directory)
# print(m_2)

print("\nBatch 1 - Group 2 - 2-class =============")
m_2 = calculate_groupe_2(directory, is_binary=True)
# print(m_2)

print("\nBatch 2 - Group 2 - 5-class =============")
directory = "../output/annotation/Final/Group_2_Batch_2"
m_2 = calculate_groupe_2(directory)
# print(m_2)

print("\nBatch 2 - Group 2 - 2-class =============")
m_2 = calculate_groupe_2(directory, is_binary=True)
# print(m_2)

