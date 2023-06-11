import subprocess

# Function to extract the text content from a Kindle ebook


def extract_text_from_ebook(file_path):

    # Construct the Calibre CLI command
    command = ['ebook-convert', file_path, 'out.txt']
    # Execute the command and capture the output
    output = subprocess.check_output(command, universal_newlines=True)

    # Open the file in read mode
    with open("out.txt", 'r') as file:
        # Read the contents of the file
        output = file.read()

    # Return the extracted text content
    return output


# Main script
kindle_file_path = 'Commedia.mobi'

# Extract text content from the Kindle ebook
text_content = extract_text_from_kindle(kindle_file_path)

# Print the extracted text content
print(text_content)
