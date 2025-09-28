import os
import re


def clean_text(text) -> str:

    # Not a comprehensive list but covers most institutions
    institutions = ['LUT University', 'IEEE', 'Springer', 'Elsevier', 'ProQuest']

    text = text.replace('ﬁ', 'fi').replace('ﬂ', 'fl')

    text = re.sub(r'\[\d+\]', '', text) # Removing citation like [1]
    text = re.sub(r'\([A-Z][a-z]+, \d{4}\)', '', text) # Removing citation (Name, Year)

    # Removing headers, footers, and page numbers
    text = re.sub(r'Page \d+', '', text, flags=re.IGNORECASE) #Removing page numbers in text where it shows up in the for "Page 1 or PAGE 22"
    #Removing lines that only consist of numbers
    text = re.sub(r'\s*\d+\s*$', '', text, flags=re.IGNORECASE)

    # Removing footers that include the institutions name that provided the material
    for institution in institutions:
        text = re.sub(institution, '', text, flags=re.IGNORECASE)

    # Converting pdf to text results in odd line breaks collapsed newlines hyphenated lines etc
    text = re.sub(r'-\n','', text)
    text = re.sub(r'\n+', '\n', text)

    # Removing repeated lines
    lines = text.split('\n')
    seen = set() # Sets are great, no repeated elements are allowed. Used to track duplicates
    unique_lines = []
    for line in lines:
        line_stripped = line.strip()
        if line_stripped and line_stripped not in seen:
            seen.add(line_stripped)
            unique_lines.append(line_stripped)
    text = '\n'.join(unique_lines)

    # Remove non-ascii and clear whitespace
    text = text.encode("ascii", errors="ignore").decode()
    text = re.sub(r'\s+',' ', text).strip()

    return text

# The function takes positional argument for input and output directories
# But there is also default arguments
def process_document(input_dir = "Documents", output_dir = "DocumentsCleaned"):
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(input_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if filename.endswith(".txt"):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)

            # Skip files that have been already cleaned
            if os.path.exists(output_path):
                print(f"Skipped (already cleaned): {filename}")
                continue

            with open(input_path, "r", encoding= "UTF-8", errors="ignore") as inputTextFile:
                rawText = inputTextFile.read()
                cleanedTextFile = clean_text(rawText)

                with open(output_path, "w", encoding="UTF-8", errors="ignore") as outputTextFile:
                    outputTextFile.write(cleanedTextFile)
        print(f"Cleaned: {filename}")

    return str(output_dir)

if __name__ == "__main__":
    process_document()