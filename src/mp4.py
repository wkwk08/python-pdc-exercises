import multiprocessing as mp
import os
from typing import List, Tuple

def count_words_in_file(file_path: str, queue: mp.Queue) -> None:
    """Worker: counts words in a file and sends result via queue."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            word_count = len(text.split())
        queue.put((file_path, word_count))
    except FileNotFoundError:
        queue.put((file_path, 0))
    except Exception:
        queue.put((file_path, 0))

def distributed_word_count(file_paths: List[str]) -> Tuple[int, List[Tuple[str, int]]]:
    """Spawns a process for each file, collects counts via a Queue, and aggregates them."""
    queue = mp.Queue()
    processes = [mp.Process(target=count_words_in_file, args=(path, queue)) for path in file_paths]

    for p in processes:
        p.start()

    results = [queue.get() for _ in file_paths]

    for p in processes:
        p.join()

    total_words = sum(count for _, count in results)
    return total_words, results

def create_dummy_files() -> List[str]:
    """Creates temporary text files for testing purposes with exactly 51 words total."""
    files_data = {
        "file1.txt": (
            "Parallel computing divides problems into tasks. "
            "Tasks run simultaneously across cores. "
            "Goal is reduced time and improved performance."
        ),
        "file2.txt": (
            "Distributed computing spreads tasks across machines. "
            "Each machine works independently. "
            "Message passing coordinates results for scalability."
        ),
        "file3.txt": (
            "Hybrid systems combine threads and processes. "
            "This balances workload and efficiency. "
            "Modern approaches demonstrate computing power effectively."
        )
    }

    paths = []
    for filename, content in files_data.items():
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        paths.append(filename)
    return paths

def cleanup_files(file_paths: List[str]) -> None:
    """Removes the temporary test files."""
    for path in file_paths:
        if os.path.exists(path):
            os.remove(path)

def main() -> None:
    test_files = create_dummy_files()
    total, _ = distributed_word_count(test_files)

    print(f"Total Words: {total}")

    cleanup_files(test_files)

if __name__ == "__main__":
    main()