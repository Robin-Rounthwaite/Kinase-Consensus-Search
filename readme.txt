For consensus_search.py
Kinase Consensus Search Program, by Robin Rounthwaite
Present functionality: finds and marks Aurora B kinase consensus sequences found on a
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

This program is fully functional as described above. I’m planning on making a lot improvements over Winter Break, however, so that using the program greatly reduces effort on the user’s part. Here are some of my goals:
1)	Increase the scale of searches so that the user can search for multiple genes at once.
2)	Allow multiple ways to search: either copy-pasting direct urls (as in present functionality)
3)	*Prioritized* list of kinase consensus data at the top of the output page.
4)	Cleaner interface for data analysis and use. 
5)	Allow user to specify kinase consensus pattern regex.
6)	Allow the user to specify the file name.

*** If you have any advice on how to improve the functionality of this program,
please let me know! I want to make it as effective a tool as possible. ***
