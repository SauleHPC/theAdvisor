import gzip
import xml.etree.ElementTree as ET
from Callback import Callback
import sys

class Paper:
    def __init__(self):
        self.paper_id = None
        self.author = None
        self.doi = None
        self.year = None
        self.pages = None
        self.title = None
        self.url = None
        self.published_through = None
        self.citation_count = None
        self.file_source = None

DBLP_line_count_freq=-1

'''
@brief: used to parse through DBLP and MAG datasets. DBLP being in XML format and MAG being in txt but uses CSV

@author: Davis Spradling
'''

'''
used to parse through DBLP

@param: file_path - file path to access DBLP

@param: callback - methods you want to be executed everytime a paper is parsed

@param: count_to - paper number you want to quit performing callbacks on

@param: start_paper - paper to start performing callbacks on

since values are being parsed using xml it is suggested to make sure that you pass in 0 as the start_paper
'''
        
def parse_DBLP_file(file_path, callback, start_paper, count_to):
    """
    Parses the DBLP dataset from a given starting point, processing a specified number of papers.

    :param file_path: Path to the DBLP dataset file.
    :param callback: List of callback functions to be executed for each processed paper.
    :param start_paper: Index of the paper to start processing from.
    :param count_to: Number of papers to process in this batch.
    """
    processed_papers = 0  # Counter for the number of papers processed in this batch
    total_papers_processed = start_paper  # Counter for the total number of papers processed

    with gzip.open(file_path, 'rt', encoding='utf-8') as gz_file:
        current_paper = None
        inside_paper = False  # Flag to track if the current line is inside a paper record

        for current_line in gz_file:
            if processed_papers >= count_to:  # Stop if the batch size limit is reached
                break

            if '</article>' in current_line or '</inproceedings>' in current_line or '</incollection>' in current_line or '</book>' in current_line:
                inside_paper = False
                if current_paper is not None and current_paper.title is not None and current_paper.paper_id is not None:
                    if total_papers_processed >= start_paper:
                        # Only process the paper if we've reached the start_paper index
                        for function in callback:
                            function(current_paper)
                        processed_papers += 1
                    current_paper = None
                    total_papers_processed += 1  # Increment total papers processed

            if '<article' in current_line or '<inproceedings' in current_line or '<incollection' in current_line or '<book' in current_line:
                if not inside_paper:
                    current_paper = Paper()
                    current_paper.file_source = "DBLP"
                    inside_paper = True

            # Parse paper details here...

    return processed_papers  # Return the number of processed papers in this batch



'''
used to parse through MAG

@param: callback - methods you want to be executed everytime a paper is parsed

@param: count_to - paper number you want to quit performing callbacks on

@param: start_line - paper to start performing callbacks on
'''

def parse_MAG_file(callback,start_line, count_to):
    file_path = 'Papers.txt.gz'
    line_counter = 0

    if(start_line>=count_to):
        print("Error: Start paper is greater then or equal to end paper. Adjust so that start paper is less then the end paper.")
        sys.exit(1)

    with gzip.open(file_path, 'rt', encoding='utf-8') as file:
        for line in file:
            line_counter += 1
            if(start_line <=line_counter):
                line = line.encode('utf-8', errors='replace').decode('utf-8')
                if(line_counter > count_to):
                    return

                fields = line.strip().split('\t')
                current_paper = Paper()
                # field[0] = the paper's MAG ID
                paper_identification, doi_num, paper_title = fields[0], fields[2], fields[4]
                current_paper.paper_id = paper_identification

                if doi_num is not None:
                    current_paper.doi = doi_num
                else:
                    current_paper.doi = None

                current_paper.title = paper_title

                current_paper.file_source = "MAG"
                for fnction in callback:
                        fnction(current_paper)
    return line_counter
