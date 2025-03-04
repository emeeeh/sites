import os
import re
import glob
from collections import defaultdict

class TextFileCombiner:
    """
    Combines text files based on their source URL patterns.
    """
    
    def __init__(self, input_dir="scraped_docs", output_dir="combined_docs"):
        """
        Initialize the combiner with input and output directories.
        
        Args:
            input_dir (str): Directory containing the scraped text files
            output_dir (str): Directory to save the combined text files
        """
        self.input_dir = input_dir
        self.output_dir = output_dir
        
        # Define URL patterns to group by
        self.url_patterns = {
            "core-nodes": "https://docs.n8n.io/integrations/builtin/core-nodes/",
            "app-nodes": "https://docs.n8n.io/integrations/builtin/app-nodes/",
            "trigger-nodes": "https://docs.n8n.io/integrations/builtin/trigger-nodes/",
            "cluster-nodes": "https://docs.n8n.io/integrations/builtin/cluster-nodes/",
            "credentials": "https://docs.n8n.io/integrations/builtin/credentials/"
        }
        
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    def get_source_url(self, file_path):
        """
        Extract the source URL from the first line of a file.
        
        Args:
            file_path (str): Path to the text file
            
        Returns:
            str or None: The source URL if found, None otherwise
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                first_line = f.readline().strip()
                
                # Check if the first line contains a source URL
                match = re.match(r"Source URL: (.+)", first_line)
                if match:
                    return match.group(1)
                
            return None
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return None
    
    def get_file_group(self, url):
        """
        Determine which group a URL belongs to based on the patterns.
        
        Args:
            url (str): The source URL
            
        Returns:
            str or None: The group name if matched, None otherwise
        """
        if not url:
            return None
            
        for group_name, pattern in self.url_patterns.items():
            if url.startswith(pattern):
                return group_name
                
        return None
    
    def combine_files(self):
        """
        Process all text files and combine them by URL pattern groups.
        """
        # Dictionary to store files by group
        grouped_files = defaultdict(list)
        other_files = []
        
        # Get all text files in the input directory
        text_files = glob.glob(os.path.join(self.input_dir, "*.txt"))
        print(f"Found {len(text_files)} text files to process")
        
        # Group files by their source URL pattern
        for file_path in text_files:
            url = self.get_source_url(file_path)
            group = self.get_file_group(url)
            
            if group:
                grouped_files[group].append((file_path, url))
            else:
                other_files.append((file_path, url))
        
        # Process each group and create a combined file
        for group_name, files in grouped_files.items():
            output_file = os.path.join(self.output_dir, f"{group_name}.txt")
            
            print(f"Creating combined file for {group_name} with {len(files)} files")
            
            with open(output_file, 'w', encoding='utf-8') as out_f:
                out_f.write(f"### Combined Content for {group_name} ###\n\n")
                
                for file_path, url in files:
                    try:
                        with open(file_path, 'r', encoding='utf-8') as in_f:
                            content = in_f.read()
                            
                            # Write file content with a separator
                            out_f.write(f"\n{'=' * 80}\n")
                            out_f.write(content)
                            out_f.write(f"\n{'=' * 80}\n")
                    except Exception as e:
                        print(f"Error processing file {file_path}: {e}")
        
        # Create a file for unmatched content if any
        if other_files:
            output_file = os.path.join(self.output_dir, "other_content.txt")
            
            print(f"Creating file for other content with {len(other_files)} files")
            
            with open(output_file, 'w', encoding='utf-8') as out_f:
                out_f.write("### Content from Other URLs ###\n\n")
                
                for file_path, url in other_files:
                    try:
                        with open(file_path, 'r', encoding='utf-8') as in_f:
                            content = in_f.read()
                            
                            # Write file content with a separator
                            out_f.write(f"\n{'=' * 80}\n")
                            out_f.write(content)
                            out_f.write(f"\n{'=' * 80}\n")
                    except Exception as e:
                        print(f"Error processing file {file_path}: {e}")
        
        # Print summary
        print("\nCombination complete. Summary:")
        for group_name, files in grouped_files.items():
            print(f"- {group_name}: {len(files)} files")
        print(f"- other_content: {len(other_files)} files")


if __name__ == "__main__":
    # Set directories - you can modify these as needed
    input_dir = "docs"  # Directory containing scraped files
    output_dir = "combined_docs"  # Directory to save combined files
    
    # Initialize and run the combiner
    combiner = TextFileCombiner(input_dir, output_dir)
    combiner.combine_files()