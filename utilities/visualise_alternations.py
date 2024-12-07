import matplotlib.pyplot as plt
import os

times_path = "times.txt"
alignments_path = "alignments.txt"
concealments_path = "concealments.txt"
untils_path = "untils.txt"


times = []
alignment_scores = []
concealment_scores = []
untils = []

with open(times_path, "r") as file:
    for line in file:
        stripped_line = line.strip()
        if stripped_line:
            times.append(float(stripped_line))

with open(alignments_path, "r") as file:
    for line in file:
        stripped_line = line.strip()
        if stripped_line:
            alignment_scores.append(float(stripped_line))

with open(concealments_path, "r") as file:
    for line in file:
        stripped_line = line.strip()
        if stripped_line:
            concealment_scores.append(float(stripped_line))

with open(untils_path, "r") as file:
    for line in file:
        stripped_line = line.strip()
        if stripped_line:
            untils.append(float(stripped_line))

alignments_dict = dict()
concealments_dict = dict()
times_dict = dict()

for i in range(len(untils)):
    alignments_dict[untils[i]] = 0
    concealments_dict[untils[i]] = 0
    times_dict[untils[i]] = 0

for i in range(len(untils)):
    alignments_dict[untils[i]] += alignment_scores[i]
    concealments_dict[untils[i]] += concealment_scores[i]
    times_dict[untils[i]] += times[i]

for i in range(len(alignments_dict.items())):
    alignments_dict[untils[i]] = alignments_dict[untils[i]] / (len(untils) / len(alignments_dict.items()))
    concealments_dict[untils[i]] = len(concealments_dict.items()) * concealments_dict[untils[i]] / len(untils)
    times_dict[untils[i]] = len(times_dict.items()) * times_dict[untils[i]] / len(untils)



alignment_scores = list(alignments_dict.values())
concealment_scores = list(concealments_dict.values())
times = list(times_dict.values())
untils = untils[:len(alignment_scores)]

plt.figure()
scatter = plt.scatter(untils, times, c=alignment_scores, cmap='viridis', s=100, edgecolor='k')
plt.colorbar(scatter, label='alignment')

plt.xlabel('alternate until')
plt.ylabel('processing time')
plt.title('Alignment Score and processing time plotted against alternate until')

plt.savefig(os.path.join(os.path.dirname(os.path.realpath(__file__)), "visualisations/alignment.png"))

plt.clf()
plt.figure()
scatter = plt.scatter(untils, times, c=concealment_scores, cmap='viridis', s=100, edgecolor='k')
plt.colorbar(scatter, label='concealment')

plt.xlabel('alternate until')
plt.ylabel('processing time')
plt.title('Concealment Score and processing time plotted against alternate until')

plt.savefig(os.path.join(os.path.dirname(os.path.realpath(__file__)), "visualisations/concealment.png"))
