import sys
sys.path.append(r'C:\Users\matan\OneDrive\שולחן העבודה\python\project\src')
from main import Main
sys.path.append(r'C:\Users\matan\OneDrive\שולחן העבודה\python\project\src\objects')
from Woman import Woman
import sys
sys.path.append(r'C:\Users\matan\OneDrive\שולחן העבודה\python\project\src\functions')
from general import generate_numbers_with_stats
from general import split_list
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Plotting the data
localMain = Main()

groups = {
    'Responders NC': localMain.file['change_image_sAA_level'][:22],
    'Non-Responders NC': localMain.file['change_image_sAA_level'][22:42],
    'Responders HC': localMain.file['change_image_sAA_level'][42:59],
    'Non-Responders HC': localMain.file['change_image_sAA_level'][59:],
}

plt.figure(figsize=(8, 6))
plt.bar(['HC Women', 'NC Women'], [np.mean(groups['Responders HC']),np.mean(groups['Responders NC'])], capsize=5, color=['gray', 'lightgray'], alpha=0.8)
plt.title('sAA Responders: sAA Response to Slide Show', fontsize=14, weight='bold')
plt.ylabel('sAA Change (U/mL)\nSEM', fontsize=12)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.savefig("output_graph_responders.png")  

plt.figure(figsize=(8, 6))
plt.bar(['HC Women', 'NC Women'],[np.mean(groups['Non-Responders HC']),np.mean(groups['Non-Responders NC'])], capsize=5, color=['gray', 'lightgray'], alpha=0.8)
plt.title('sAA Non-Responders: sAA Response to Slide Show', fontsize=14, weight='bold')
plt.ylabel('sAA Change (U/mL)\nSEM', fontsize=12)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.axhline(0, color='black', linewidth=0.8, linestyle='-') 
plt.savefig("output_graph_nonresponders.png") 