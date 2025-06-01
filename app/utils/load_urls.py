
def load_links_from_file(file_path):
    with open(file_path, 'r') as file:
        links = [line.strip() for line in file if line.strip()]
    return links


if __name__ == "__main__":
    file_path = "ALL_LINKS_PATH"
    links_array = load_links_from_file(file_path)
    print(f"Loaded {len(links_array)} links.")
    print(links_array)