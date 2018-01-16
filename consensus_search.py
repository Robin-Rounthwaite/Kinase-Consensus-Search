"""
Kinase Consensus Search Program

author: Robin Rounthwaite (rounthrl)

Present functionality: finds and marks Aurora B kinase consensus sequences 
found on a given protein by bolding and underlining them in the sequence, and 
additionally provides a list with relevant information about each sequence 
(i.e. the protein sequence, where it is in the protein, and how evolutionarily 
conserved it is via a simple numerical ranking system). The sequence 
additionally displays evolutionary conservation data, for visually identifying 
regions of especial importance.

Programs needed to run: graphics.py in the file, Python3 bs4, and BeautifulSoup 
from bs4 installed on the computer.
Other libraries used, which should come with Python3: sys, urllib.request, and 
re.

Instructions for use: run consensus_search.py, follow instructions on the popup 
window. (i.e. copy/paste an url into the search bar, then press the green 
‘Search’ button). Then, open the file labeled ‘output.html’ and see the end-
result!

For running a test case, try the fungal alignment page for the protein ndc10:
https://www.yeastgenome.org/cache/fungi/YGR140W.html

How it works: This program scrapes conservation data and protein sequence from 
an url linking to the Saccharomyces Genome Database's fungal alignment tool. It 
then finds and marks Aurora B Kinase consensus sequences within the sequence, 
and assembles an html document with all the relevant information. 
"""

import sys
import graphics # used for interface.
import urllib.request # used to get the webpage for BeautifulSoup.
from bs4 import BeautifulSoup # used for web-scraping.
import bs4 # used to recognize the Tag type.
import re # regular expressions - primarily used for finding kinase consensus site.
def notes_to_self():
    """These are just notes to myself. Don't worry about them."""
    pass
    """Notes to self: 
        At present, this code only finds Aurora B kinase consensus sites. 
        MAYBE I SHOULD (after getting this to work): make it so that the 
        program interface accepts kinase consensus sites in general, so that 
        the user can input a different kinase consensus site via the GUI. I'd 
        have to only let the user input one consensus site at a time, so that 
        the Protein objects don't get confused.
        Also, I should consider making a single document with all the Aurora B 
        consensus sites ranked in order of usefulness, so that the user can 
        prioritize certain sites over others.
    """
    # note to self: here is the website for ndc10 fungal alignment:
    # https://www.yeastgenome.org/cache/fungi/YGR140W.html
    # using pip: py -m pip install XXX
    # about webscraping: https://www.analyticsvidhya.com/blog/2015/10/beginner-guide-web-scraping-beautiful-soup-python/
    # intro to regex: https://docs.python.org/3/howto/regex.html#more-metacharacters
    # full documentation of regex: https://docs.python.org/3/library/re.html#module-re

def mark_consensus(cons_pattern, sequence, amino_list):
    """Given a consensus sequence regex, and the sequence of the protein both as a string and as a list of AminoAcid objects, alters the AminoAcid objects so that the proper amino acids are marked for consensus."""
    cons_num = 0 # will be used to keep track of which unique consensus number this is.
    aur_regex = re.compile(cons_pattern)
    cons_search = aur_regex.finditer(sequence)
    for match_obj in cons_search:
        for amino in amino_list[match_obj.start(): match_obj.end()]:
            amino.mark_consensus(cons_num)
        cons_num += 1

def break_into_list(input_str):
    """Given a string with items listed within separated by commas (i.e. 'x,y,z'), will separate into a Python list [x,y,z].
    Currently an UNUSED function.
    """
    assert isinstance(input_str, str)
    temp_str = ''
    input_list = []
    for ch in input_str:
        if input_str[index] == ',':
            input_list.append(temp_str)
            temp_str = ''
        else:
            temp_str += ch
    input_list.append(temp_str)
    return input_list
        
def list_consensus(protein):
    """Uses html to create a list of consensus sequences found in the protein, 
    and lists them with relevant data (where they are in the protein, how 
    conserved they are, and the sequence itself).
    
    Parameters: protein: a protein object.
    
    preconditions: protein must be of class Protein.
    """
    assert isinstance(protein, Protein)
    consensus_seq = [] # will list each consensus sequence as a separate item.
    consensus_rank = [] # keeps track of the consensus sequence's level of 
    # importance based on conservation.
    consensus_loc = [] # keeps track of where the consensus sequence starts.
    consensus_num = -1
    amino_count = 0
    #html variable, below, will contain the information placed on the page.
    html =  '<table><tr><tt>' + 'Consensus list key, for list below: consensus seq. location; consensus sequence; consensus rank' + '</tt>' 
    for amino in protein.get_amino_list():
        if amino.get_type() != '-':
            amino_count += 1
        if amino.get_consensus() != None:
            if amino.get_consensus() == consensus_num: #i.e. if we're in the 
                # middle of a consensus sequence that we're parsing.
                consensus_seq[consensus_num] += amino.get_type()
                consensus_rank[consensus_num] += amino.get_conservation_num()
            else:
                consensus_seq.append(amino.get_type())
                consensus_rank.append(amino.get_conservation_num())
                consensus_loc.append(amino_count)
                consensus_num = amino.get_consensus() # updates the consensus 
                # number because we are in a consensus sequence.
    for index in range(len(consensus_seq)):
        html += '<table><tr><tt>' + str(consensus_loc[index]) + ' ' + consensus_seq[index] + ' ' + str(consensus_rank[index]) + '</tt></tr>'
    return html
        
        
        
def assemble_protein_html(protein):
    """
    Given a Protein object, will assemble html to display that Protein in a table 60 amino acids wide.
    preconditions: protein must be of class Protein.
    """
    assert isinstance(protein, Protein)
#    protein_html = '<table class="sequence-table"><tr>'
    protein_html = '<table><tr>'
    wrap_text_count = 0
    for amino in protein.get_amino_list():
        if amino.get_type() != '-':
            if wrap_text_count % 60 == 0: # width of table.
                #begin new table, along with the number marking where we are 
                #in the protein.
                protein_html += '<table><tr>' + str(wrap_text_count + 1) 
            if amino.get_consensus() == None:
                protein_html += '<td bgcolor=' + amino.get_conservation() + '><tt>' + amino.get_type() + '</tt></td>'
            else:
                protein_html += '<td bgcolor=' + amino.get_conservation() + '><tt><u><b>' + amino.get_type() + '</b></u></tt></td>'
            wrap_text_count += 1
    return protein_html
        
class Button:
    """Creates a button object with authentic clickable action! Receives x and y coordinates, window for display, and color. 
    """
    def __init__(self, x, y, win, color):
        """Constructor that draws the rectangle which will dictate the bounds 
        of the button.
        
        Parameters: x, y: coordinates for bottom left hand corner of button.
        win: window where button will be drawn.
        color: color of button
        
        Preconditions: x and y must be integers.
        win must be a window
        color must be a string containting a simple color name (e.g. 'green') 
        """
        assert isinstance(x, int), 'x must be an integer'
        assert isinstance(y, int), 'y must be an integer'
        assert isinstance(win, graphics.GraphWin), 'win must be a window'
        assert isinstance(color, str), 'color must be a string.'
        self.x = x
        self.y = y
        self.win = win
        p1 = graphics.Point(self.x + 50, self.y + 50)
        p2 = graphics.Point(self.x, self.y)
        c1 = graphics.Rectangle(p1, p2)
        c1.setFill(color)
        c1.draw(self.win)
    
    def click(self, pt):
        """When given a point (presumably from a mouse click), detects whether the point is within the range of the button.
        
        Parameters: pt: a point, representing a mouse click.
        
        Preconditions: pt must be a point
        """
        assert isinstance(pt, graphics.Point)
        x = pt.getX()
        y = pt.getY() 
        if self.x < x < (self.x + 50) and self.y < y < (self.y + 50):
            return True
        
    def text(self, text):
        """When given some text, displays text on button
        """
        text_pt = graphics.Point(self.x + 25, self.y + 25)
        text_obj = graphics.Text(text_pt, text)
        text_obj.draw(self.win)

class Interface:
    """Creates the window for user input, and can construct the output html 
    file.
    """
    def __init__(self):
        # initialize window
        self.win = graphics.GraphWin("Aurora B Consensus Seq Finder", 800, 400)
        # transform coordinates
        self.win.setCoords(0, 0, 400, 400)
        
        # draw button
        self.run_prog_button = Button(320, 20, self.win, 'green')
        self.run_prog_button.text('Search')
        
        # draw text input boxes
        self.protein_list_input = graphics.Entry(graphics.Point(200, 200), 70)
        self.protein_list_input.draw(self.win)
        
        # write instructions
        text_pt = graphics.Point(200, 300)
        text_message = """Welcome to the Aurora B Kinase Consensus Search Program!
        Please input a URL linking to the fungal alignment for a protein of interest on the SGD in the textbox below, and then click "Search".
        It may take a moment for the program to run. The window will close when the created file is saved.
        Example test URL: https://www.yeastgenome.org/cache/fungi/YGR113W.html
        """
        text_obj = graphics.Text(text_pt, text_message)
        text_obj.draw(self.win)
        
        # initialize useful variables for later
        self.protein_list = None
        
    def get_input(self):
        """ When the 'Search' button is pressed, get the string from the search 
        bar.
        """
        keep_running = True
        while keep_running == True:
            pt = self.win.getMouse()
            if self.run_prog_button.click(pt) == True:
                prot_input_str = self.protein_list_input.getText()
                self.protein_list = prot_input_str
#                protein_list = break_into_list(prot_input_str)
                keep_running = False
                
                
        
    def save_annotated_files(self):
        """saves the annotated protein sequence to a file."""
        html = SgdHtml(self.protein_list)
        prot = Protein(html.get_sequence(),\
         html.get_conservation_data_source_color())
        prot.set_aur_b_consensus()
        # write and save the file with the consensus data.
        f = open("output.html", "w")
        f.write("""
        Hello! This is your Aurora B kinase consensus data.
        Colored amino acids mark relative conservation. Gold means that it was identically conserved across species inspected, pink means strongly conserved, green means weakly conserved, and white is non-conserved.
        """ + list_consensus(prot) + assemble_protein_html(prot))
        #Note: the "success" note below doesn't actually give useful feedback 
        #yet. It'll hopefully come in handy later, though.
        return "success"
        
    
    def error(self):
        """presently unused"""
        pass
    
    def done(self):
        """Closes the window when the program is done."""
        
    
class AminoAcid:
    """An Amino Acid class, which keeps track of how conserved it is, and what 
    type of amino acid it is.
    
    Parameters: 
        amino_type: a single letter in a string, marking the amino acid type.
        conservation: the level of conservation of the amino acid, currently 
        marked by the colors 'yellow', 'pink', and 'lightgreen' for identical, 
        strong, and weak.
    """
    def __init__(self, amino_type, conservation):
        self.amino_type = amino_type
        self.conservation = conservation
        
        # Because it's helpful to also keep track of conservation_data in 
        # numerical format (i.e 3, 2, 1 instead of identical, strong, weak) so 
        # that I can rank the conservation sequences later, I'm also going to 
        # give the AminoAcid object a numerical version of conservation.
        if self.conservation == 'yellow': # identical
            self.conservation_num = 3
        elif self.conservation == 'pink': # strong
            self.conservation_num = 2
        elif self.conservation == 'lightgreen': # weak
            self.conservation_num = 1
        else:
            self.conservation_num = 0
        
        # when the consensus annotation moves through, the following variable
        # can be changed.
        self.part_of_consensus = None
        
    def get_type(self):
        return self.amino_type
    
    def get_conservation(self):
        return self.conservation
    
    def get_conservation_num(self):
        return self.conservation_num
    
    def get_consensus(self):
        return self.part_of_consensus
    
    def mark_consensus(self, cons_num):
        """Marks this amino acid as part of a consensus sequence for a kinase. 
        cons_num is the integer used to identify this amino acid as part of a 
        particular consensus sequence (0th sequence in the protein, 1st 
        sequence, etc.)"""
        self.part_of_consensus = cons_num
        
class Protein:
    """A Protein class, which creates and keeps track of a list of amino acid 
    objects, given a sequence list in a string and a correlary conservation 
    data list.
    
    Parameters: 
        sequence_str: a string with the protein sequence in it (dashes (-) are 
        okay, will be removed later.)
        conservation_data_list: a list of all the conservation data, with a 
        color (or an empty string) as each item. There should be one item for 
        every character in sequence_str.
    """
    def __init__(self, sequence_str, conservation_data_list):
        self.sequence = sequence_str
        self.conservation_data_clr = conservation_data_list
        
        # Combine the sequence and conservation data in AminoAcid objects.
        self.amino_list = []
        for index in range(len(self.sequence)):
            amino = AminoAcid(self.sequence[index], self.conservation_data_clr[index])
            self.amino_list.append(amino)
            
    def set_aur_b_consensus(self):
        """Returns everything the Interface needs to create a beautiful file displaying conservation data, sequence, and Aurora B consensus sites."""
        # first, mark the Aurora B consensus sites. Note that, because the 
        #AminoAcid objects in amino_list are being physically altered, there is 
        #no need to return a new list.
        aur_cons = "[KR].[ST][ILV]"
        mark_consensus(aur_cons, self.sequence, self.amino_list)
        
    def get_amino_list(self):
        return self.amino_list
    
    def get_sequence(self):
        return self.sequence
    
    def get_conservation_data(self):
        return self.conservation_data_clr
    
class SgdHtml:
    """Given an url linking to an SGD fungal alignment page, extracts the 
    sequence and conservation data. 
    
    Parameter:
        url: an url linking to an SGD fungal alignment page.
    """
    def __init__(self, url):
        page = urllib.request.urlopen(url)
        self.html = BeautifulSoup(page, "html.parser")
    
    def get_sequence(self):
        """Finds the sequence of the protein undergoing fungal alignment, and returns only that sequence. Dashes (-) are preserved so that the conservation data from get_conservation_data lines up well without having to alter the scraped sequence. The dashes are removed when assembling html in Interface via the assemble_protein_html function."""
        all_tables = self.html.find_all('table', class_='sequence-table')
        amino_str = ''
        for table in all_tables:
            first_tr = table.find('tr')
            tds = first_tr.find_all('td')
            for td in tds:
                tt = td.find('tt')
                if isinstance(tt, bs4.element.Tag):
                    amino_str += tt.get_text()
        return amino_str

#    def get_conservation_data(self):
#        """unused feature, so commented out."""
#        all_tables = self.html.find_all('table', class_='sequence-table')
#        clr_reg_ex = re.compile('bgcolor=".*?"')
#        cons_list_raw = []
#        cons_list = []
#        for table in all_tables:
#            first_tr = str(table.find('tr'))
#            temp_list = clr_reg_ex.findall(first_tr)
#            for item in temp_list:
#                cons_list_raw.append(item[9:-1])
#        for color in cons_list_raw:
#            if color == 'yellow':
#                cons_list.append('identical') #identical
#            elif color == 'pink':
#                cons_list.append('strong') #strong
#            elif color == 'lightgreen':
#                cons_list.append('weak')
#            else:
#                cons_list.append(color)
#        return cons_list

    def get_conservation_data_source_color(self):
        """
        Gets the conservation data in terms of colors from the url. 
        Gold means that it was identically conserved across species inspected, 
        pink means strongly conserved, green means weakly conserved, and white 
        is non-conserved.
        """
        all_tables = self.html.find_all('table', class_='sequence-table')
        clr_reg_ex = re.compile('bgcolor=".*?"')
        cons_list = []
        for table in all_tables:
            first_tr = str(table.find('tr'))
            temp_list = clr_reg_ex.findall(first_tr)
            for item in temp_list:
                cons_list.append(item[9:-1])
        return cons_list


class Program:
    """This class represents this program as a whole, which searches for kinase 
    consensus sites."""
    
    def __init__(self):
        """Constructor for the program"""
        self.interface = Interface()
        
    def run_program(self):
        needs_input = True
        while needs_input == True:
            prot_list = self.interface.get_input()
            success_check = self.interface.save_annotated_files()
            if success_check == "success": # right now, should always be true.
                self.interface.done()
                needs_input = False
            else:
                self.interface.error()    
        
    
def main():
    program = Program()
    program.run_program()

main()