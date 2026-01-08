import requests
import matplotlib.pyplot as plt

def get_student_scores():
    """
    Fetches student data from an API.
    Uses fallback/mock data to ensure the script runs successfully.
    """
    url = "https://api.example.com/v1/scores"  # placeholder

    try:
        # Real API call (commented out for safe demo)
        # response = requests.get(url, timeout=10)
        # response.raise_for_status()
        # return response.json()

        # Fallback/mock data for demonstration
        return [
            {"name": "Alice Johnson", "score": 88},
            {"name": "Bob Smith", "score": 72},
            {"name": "Charlie Davis", "score": 95},
            {"name": "Diana Prince", "score": 84},
            {"name": "Ethan Hunt", "score": 91},
            {"name": "Fiona Gallagher", "score": 78}
        ]

    except Exception as e:
        print(f"Network error: {e}")
        print("Using fallback data instead.")
        return [
            {"name": "Alice Johnson", "score": 88},
            {"name": "Bob Smith", "score": 72},
            {"name": "Charlie Davis", "score": 95}
        ]

def main():
    # 1️⃣ Fetch data
    data = get_student_scores()
    if not data:
        print("No student data found.")
        return

    # 2️⃣ Extract names and scores safely
    names = [entry.get('name', 'Unknown') for entry in data]
    scores = [entry.get('score', 0) for entry in data]

    # 3️⃣ Calculate average score
    total_sum = 0
    for s in scores:
        total_sum += s
    avg_score = total_sum / len(scores) if scores else 0

    # 4️⃣ Output results
    print(f"Total Students: {len(names)}")
    print(f"Average Class Score: {avg_score:.2f}")

    # 5️⃣ Create bar chart
    plt.bar(names, scores, alpha=0.7)
    plt.title("Student Final Scores", fontsize=14, pad=15)
    plt.xlabel("Student Name", fontsize=12)
    plt.ylabel("Score", fontsize=12)
    plt.xticks(rotation=30, ha='right')
    plt.ylim(0, 100)
    plt.grid(axis='y', linestyle='--', alpha=0.5)

    # 6️⃣ Save chart
    plt.tight_layout()
    plt.savefig('student_chart.png')
    plt.close()  # free memory
    print("Report generated: student_chart.png")

if __name__ == "__main__":
    main()
