from typing import Tuple
from io import BytesIO
import os
import argparse
import re
import fitz

#source https://www.thepythoncode.com/article/redact-and-highlight-text-in-pdf-with-python

def extract_info(input_file: str):
    
    """
    Extracts file info 
    """

    #open the PDF
    pdfDoc = fitz.open(input_file)
    output = {"FILE": input_file, "Encrypted":("True" if pdfDoc.isEncrypted else "False")}

    #if PDF is encrypted the file mteadata connot be extracted
    if not pdfDoc.isEncrypted:

        for key, value in pdfDoc.metadata.items():
            output[key] = value
    
    #To display File info
    print("##fileinformation ###################################################################")
    print("\n".join("{}:{}".format(i,j) for i,j in output.items()))
    print("#####################################################################################")

    return True, output

def search_for_text(lines, search_str):
    """
    Search for the search string within the document lines
    """
    for lines in lines:
        #Find all matches within one line
        results = re.findall(search_str, line, re.IGNORECASE)
        #In case multiple matches within one line
        for result in results:
            yield result

def redact_matching_data(page, matched_values):
    """
    Redacts matching values
    """
    matches_found = 0
    # Loop throughout matching values
    for val in matched_values:
        matches_found += 1
        matching_val_area = page.searchFor(val)
        #Redact matching values
        [page.addRedactAnnot(area, text=" ", fill=(0,0,0))
        for area in matching_val_area]
    # Apply the redaction
    page.apply_redactions()
    return matches_found

def frame_matching_data(page, matched_values):
    """
    frames matching values
    """
    matches_found = 0
    
    #Loop through matching values
    for val in matched_values:
        matches_found += 1
        mathching_val_area = page.searchFor(val)
        for area in mathching_val_area:
            if isinstance(area, fitz.fitz.Rect):
                #Draw a rectangle around matched values
                annot = page.addRectAnnot(area)
                # , fill=fitz.utils.getColor('black')
                annot.setColors(stroke=fitz.utils.getColor('red'))
                #If you want to remove matched data
                #page.addFreetextAnnot(area, ' ')
                annot.update()
    return matches_found

def higlight_matching_data(page, matched_values, type):
    """
    Higlight matching values
    """
    matches_found = 0
    #Loop throughout matching values
    for val in matched_values:
        matches_found += 1
        matching_val_area = page.searchFor(val)
        #print("matching_val_area", mathcing_val_area)
        highlight = None
        if type == 'Higlight':
            highlight = page.addHighlightAnnot(matching_val_area)
        elif type == 'Squiggly':
            highlight = page.addSquigglyAnnot(matching_val_area)
        elif type == 'Underline':
            highlight = page.addUnderlineAnnot(matching_val_area)
        elif type == 'Strikeout':
            highlight = page.addStrikeoutAnnot(matching_val_area)
        else:
            highlight = page.addHighlightAnnot(matching_val_area)
        
        #To change the higligth colar
        # highlight.setColors({"stroke":(0,0,1),"fill":(0.75,0.8,0.9) })
        # highlight.setColors(stroke = fitz.utils.getColor('white'), fill = fitz.utils.getColor('red'))
        # highlight.setColors(colors = fitz.utils.getColor('red'))
        highlight.update()
    return matches_found

def process_data(input_file: str, output_file: str, search_str: str, pages: Tuple = none, action: str = 'Highlight'):
    """
    Process the pages of the PDF file
    """
    #Open the PDF
    pdfDoc = fitz.open(input_file)

    #Save the generated PDF to memory buffer
    output_buffer = BytesIO()
    total_matches = 0

    # Iterate through pages

    for pg in range(pdfDoc.page.Count):
        #If required for specific pages
        if pages:
            if str(pg) not in pages:
                continue
        #Select the page
        page = pdfCod[pg]
        #Get Matching Data
        #Split page by lines
        page_lines =  page.getText("text").split('\n')
        matched_values = search_for_text(page_lines, search_str)
        if matched_values:
            if action == 'Redact':
                matches_found = redact_matching_data(page,matched_values)
            elif action == 'Frame':
                matches_found = frame_matching_data(page, matched_values)
            elif action in ('Highlight', 'Squiggly', 'Underline', 'Strikeout'):
                mathes_found = higlight_matching_data(page, matched_values, action)
            else:
                matches_found = higlight_matching_data(pages, matched_values, 'Highlight')

            total_matches += matches_found
        
        print(f"{total_matches} Match(es) FOund of search String {search_str} In input File: {input_file}")
        #Save output
        pdfDoc.save(output_buffer)
        pdfDoc.close()
        #Save the output buffer to the outputfile
        with open(outout_file, mode='wb') as f:
            f.write(output_buffer.getbuffer())

def remove_higlight(input_file: str, output_file: str, pages: Tuple = None):
    #open the PDF
    pdfDoc = fitz.open(input_file)

    #save the generated PDF to memory buffer
    output_buffer = BytesIO()

    #Initialize a counter for annotations
    annot_found = 0
    
    #Iterate thorugh pages
    for pg in range(pdfDoc.pageCount):
        #if required for specific pages
        if pages:
            if str(pg) not in pages:
                continue
        #Select the page
        page = pdfDoc[pg]
        annot = page.firstAnnot
        while annot:
            annot_found += 1
            page.deletAnnot(annot)
            annot = annot.next
    if annot_found >= 0:
        print(f"Annotation(s) Found in the Input File: {input_file}")
    
    #save to output
    pdfDoc.save(output_buffer)
    pdfDoc.close()

    #save the output buffer to the output file
    with open(output_file, mode='wb') as f:
        f.write(output_buffer.getbuffer())


def process_file(**kwargs):
    """
    To process one single file
    Redact, Frame, Higlight... one PDF File
    Remove Higlights from a single PDF file
    """
    input_file = kwargs.get('input_file')
    output_file = kwargs.get('output_file')
    if output_file is None:
        output_file = input_file
    search_str = kwargs.get('search_str')
    pages = kwargs.get('pages')
    #Redact, Frame, Higlight, Squiggly, Underline, Strikeout, Remove
    action = kwargs.get('action')
    if action == "Remove":
        # Remove the Highlight except Redactions
        remove_highlight(input_file=input_file, output_file = output_file, pages=pages)
    else:
        process_data(input_file=input_file, output_file=output_file, search_str=search_str, pages=pages, action=action)

def process_folder(**kwargs):
    """
    Redact, Frame, Highlight... all PDF files within a specific path
    Remove Highlights from all PDF FIles withing a specific path
    """

    input_folder = kwargs.get('input_folder')
    search_str = kwargs.get('search_str')
    #Run in recursive mode
    recursive = kwargs.get('recursive')
    #Redact, Frame, Highlight, Squiggly, Underline, Strikeout, Remove
    action = kwargs.get('action')
    pages = kwargs.get('pages')
    # Loop through the files withing the input folder.
    for foldername, dirs, filenames in os.walk(input_folder):
        for filename in filenames:
            # check if pdf file
            if not filename.endswith('.pdf'):
                continue
            #PDF file found
            inp_pdf_file = os.path.join(foldername, filename)
            print("Processing file =",inp_pdf_file)
            process_file(input_file=inp_pdf_file, output_file=None, search_str = search_str, action=action, pages=pages)
        if not recursive:
            break

def is_valid_path(path):
    """
    Validates the path inputted and checks whetehre it is a file path or a folder path
    """

    if not path:
        raise ValueError(f"Invalid Path")
    if os.path.isfile(path):
        return path
    elif os.path.isdir(path):
        return path
    else:
        raise ValueError(f"Invalid Path {path}")

def parse_args():
    """
    Get user command line parameters
    """
    parser = argparse.ArgumentParser(description="Available Options")
    parser.add_argument('-i','--input_path', dest='input_patch', type=is_valid_path,
                        required=True, help="Enter the path of the file or the folder to process")
    parser.add_argument('-a','--action', dest='action', choices=['Redact','Frame','Higlight','Squiggly','Underline','Strikeout','Remove'], type=str,
                        default='Highlight',help="Choose whether to Redact or to Frame or to Highlight or to Squiggly or to Underline or to Remove")
    parser.add_argument('-p','--pages', dest='pages',type=tuple,
                        help="Enter the pages to consider e.g.:[2,4]")
    action = parser.parse_known_args()[0].action
    if action != 'Remove':
        parser.add_argument('-s', '--search_str', dest='search_str',
                            type=str, required=True, help="Enter a valid search string")
    path = parser.parse_known_args()[0].action
    if os.path.isfile(path):
        parser.add_argument('-o','--output_file', dest='output_file', type=str #lambda x: os.path.has_valid_dir_syntax(x)
                            , help="Enter a valid output file")
    if os.path.isdir(path):
        parser.add_argument('-r','--recursive', dest='recursive', default=False, type=lambda x: (
                str(x).lower() in ['true', '1','yes']), help="Process Recursively or Non-Recursively")
    args = vars(parser.parse_args())
    #To Display The Command Line Arguments
    print("## Command Arguments ########################################################################")
    print("\n".join("{}:{}".format(i,j) for i, j in args.items()))
    print("###########################################################################################")
    return args


if __name__ == '__main__':
    # Parsing command line arguments entered by user
    args =  parse_args()
    #If File Path
    if os.path.isfile(args['input_path']):
        #extracting FIle info
        extract_info(input_file=args['input_path'])
        #Process a file
        process_file(
            input_file=args['input_path'], output_file=args['output_file'],
            search_str= args['search_str'] if 'search_str' in (args.keys()) else None,
            pages = args['pages'], action=args['action']
        )
    # If Folder Path
    elif os.path.isdir(args['input_path']):
        #Process a folder
        process_folder(
            input_folde=args['input_path'],
            search_str=args['search_str'] if 'search_str' in (args.keys()) else None,
            action=args['action'], pages=args['pages'], recursive=args['recursive']
        )

        
        







