For consensus_search.py
Kinase Consensus Search Program, by Robin Rounthwaite
Present functionality: Creates an html file, which finds and marks Aurora B kinase consensus sequences found on a
 given protein by bolding and underlining them in the sequence, and additionally provides
 a list with relevant information about each sequence (i.e. the protein sequence, where
 it is in the protein, and how evolutionarily conserved it is via a simple numerical
 ranking system). The sequence additionally displays evolutionary conservation data,
 for visually identifying regions of especial importance.

Programs needed to run: graphics.py in the file, Python3 bs4, and BeautifulSoup
from bs4 installed on the computer.

Other libraries used, which should come with Python3: sys, urllib.request, and re.

Instructions for use: run consensus_search.py, follow instructions on the popup window.
(i.e. copy/paste an url into the search bar, then press the green ‘Search’ button).
Then, open the file labeled ‘output.html’ and see the end-result!

For running a test case, try the fungal alignment page for the protein ndc10:
https://www.yeastgenome.org/cache/fungi/YGR140W.html

How it works: This program scrapes conservation data and protein sequence from an url linking to the Saccharomyces Genome Database's fungal alignment tool. It then finds and marks Aurora B Kinase consensus sequences within the sequence, and assembles an html document with all the relevant information. 

Potential Future Goals:
1) Improvement of kinase consensus ranking so that the conservation of the serine/threonine 
   is given priority when calculating consensus rank.
2)	Increase the scale of searches so that the user can search for multiple genes at once.
3)	Allow multiple ways to search: either copy-pasting direct urls (as in present functionality) or by protein name.
4)	*Prioritized* list of kinase consensus data at the top of the output page.
5)	Cleaner interface for data analysis and use. (make the kinase consensus sites more visible).
6)	Allow user to specify kinase consensus pattern regex.
7)	Allow the user to specify the file name.
8) Fix html table formatting so that it is preserved when sent as an email attachment.

*** If you have any advice on how to improve the functionality of this program,
please let me know! I want to make it as effective a tool as possible. ***
