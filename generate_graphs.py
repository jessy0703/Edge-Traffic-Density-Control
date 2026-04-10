import matplotlib.pyplot as plt

# Read results file
file_path = "outputs/results.txt"

videos = []
counts = []

with open(file_path, "r") as f:
    for line in f:
        video, count, density = line.strip().split(", ")
        videos.append(video)
        counts.append(int(count))

# Plot graph
plt.figure()
plt.bar(videos, counts)

plt.xlabel("Videos")
plt.ylabel("Vehicle Count")
plt.title("Vehicle Count across Different Traffic Videos")

plt.xticks(rotation=20)

# Save graph
plt.savefig("outputs/vehicle_count_graph.png")

plt.show()