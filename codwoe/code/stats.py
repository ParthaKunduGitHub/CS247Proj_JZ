import json
from collections import Counter, defaultdict
from pathlib import Path

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
    Calculate and display key statistics from the dataset.
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
    calculate_stats(dataset)

if __name__ == "__main__":
    main()