import json
from collections import Counter, defaultdict
from pathlib import Path
import matplotlib.pyplot as plt

def load_dataset(file_path):
    """
    Load the JSON dataset from the specified file path.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return None

def calculate_stats(data):
    """
    Calculate key statistics from the dataset and return them for visualization.
    """
    # Total number of entries
    total_entries = len(data)

    # Counting unique words in glosses
    unique_words = set()
    gloss_lengths = []
    embedding_types = set()

    for entry in data:
        # Extract gloss and tokenize
        gloss = entry.get("gloss", "")
        words = gloss.split()
        unique_words.update(words)
        gloss_lengths.append(len(words))
        
        # Collect embedding types
        embedding_types.update(entry.keys())

    # Remove non-embedding-related fields from embedding types
    embedding_types.difference_update({"id", "gloss", "word", "pos", "concrete", "example", "f_rnk", "counts", "polysemous"})

    # Average gloss length
    avg_gloss_length = sum(gloss_lengths) / len(gloss_lengths) if gloss_lengths else 0

    # Print statistics
    print("Dataset Statistics:")
    print(f"- Total Entries: {total_entries}")
    print(f"- Unique Words in Glosses: {len(unique_words)}")
    print(f"- Average Gloss Length: {avg_gloss_length:.2f} words")
    print(f"- Embedding Types: {', '.join(embedding_types)}")

    # Distribution of gloss lengths
    length_distribution = Counter(gloss_lengths)
    print("\nGloss Length Distribution (Number of words):")
    for length, count in sorted(length_distribution.items()):
        print(f"  {length} words: {count} entries")

    # Return stats for visualization
    return {
        "total_entries": total_entries,
        "unique_words": unique_words,
        "avg_gloss_length": avg_gloss_length,
        "gloss_lengths": gloss_lengths,
        "embedding_types": embedding_types
    }

def visualize_gloss_length_distribution(gloss_lengths):
    """
    Visualize the distribution of gloss lengths as a bar chart.
    """
    gloss_count = Counter(gloss_lengths)
    lengths, counts = zip(*sorted(gloss_count.items()))

    plt.figure(figsize=(10, 6))
    plt.bar(lengths, counts, color='skyblue', edgecolor='black')
    plt.title("Gloss Length Distribution", fontsize=16)
    plt.xlabel("Gloss Length (Number of Words)", fontsize=14)
    plt.ylabel("Number of Glosses", fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

def visualize_embedding_types(embedding_types):
    """
    Visualize embedding types as a horizontal bar chart.
    """
    plt.figure(figsize=(8, 4))
    plt.barh(list(embedding_types), [1] * len(embedding_types), color='lightcoral')
    plt.title("Embedding Types in Dataset", fontsize=16)
    plt.xlabel("Presence (1 = Available)", fontsize=14)
    plt.yticks(fontsize=12)
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

def visualize_stats(stats):
    """
    Generate visualizations for the dataset statistics.
    """
    print("Visualizing Gloss Length Distribution...")
    visualize_gloss_length_distribution(stats["gloss_lengths"])

    print("Visualizing Embedding Types...")
    visualize_embedding_types(stats["embedding_types"])

def main():
    # Update the file path to the dataset JSON file
    dataset_path = Path("../data/train-data_all/en.train.json")  # Replace with the actual path

    # Load the dataset
    print("Loading dataset...")
    dataset = load_dataset(dataset_path)
    if not dataset:
        print("Failed to load dataset. Exiting.")
        return

    # Generate statistics
    stats = calculate_stats(dataset)

    # Visualize statistics
    visualize_stats(stats)

if __name__ == "__main__":
    main()
