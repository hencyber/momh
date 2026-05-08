from langchain_text_splitters import RecursiveCharacterTextSplitter
import os


def load_chunk_text(file_path: str):
    if not os.path.exists(file_path):  # checking if file exists
        print(f"Error:{file_path} not found.")
        return []

    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    # Configure splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        separators=["\n\n", "\n", ".", " ", ""],
    )
    # Creates chunks
    chunks = text_splitter.split_text(text)
    return chunks


if __name__ == "__main__":  # testing the code locally
    path_to_data = "src/momh/backend/data/utlandsstudier/csn_utlandsstudier.txt"
    all_chunks = load_chunk_text(path_to_data)

    print(f"Amount of created chunks: {len(all_chunks)}")
    if all_chunks:
        print("n Example of first chunk:")
        print(all_chunks[0])
