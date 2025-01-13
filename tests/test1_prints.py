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

# 1. Plotting age distribution
plt.figure(figsize=(10, 6))
plt.hist(localMain.file['age'], bins=20, edgecolor='black', color='skyblue', alpha=0.7)
plt.title('Age Distribution', fontsize=16)
plt.xlabel('Age', fontsize=14)
plt.ylabel('Frequency', fontsize=14)
plt.grid(True)
plt.show()

# נתוני הקבוצות (תואמים לפלט מסומלצ)
groups = {
    'Responders NC': localMain.file['change_image_sAA_level'][:22],
    'Non-Responders NC': localMain.file['change_image_sAA_level'][22:42],
    'Responders HC': localMain.file['change_image_sAA_level'][42:59],
    'Non-Responders HC': localMain.file['change_image_sAA_level'][59:]
   ,
}

# תרשים עמודות עבור Responders
plt.figure(figsize=(8, 6))
plt.bar(['HC Women', 'NC Women'], [np.mean(groups['Responders HC']),np.mean(groups['Responders NC'])], capsize=5, color=['gray', 'lightgray'], alpha=0.8)
plt.title('sAA Responders: sAA Response to Slide Show', fontsize=14, weight='bold')
plt.ylabel('sAA Change (U/mL)\nSEM', fontsize=12)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.savefig("output_graph_responders.png")  # שומר את הגרף של responders

# תרשים עמודות עבור Non-Responders
plt.figure(figsize=(8, 6))
plt.bar(['HC Women', 'NC Women'],[np.mean(groups['Non-Responders HC']),np.mean(groups['Non-Responders NC'])], capsize=5, color=['gray', 'lightgray'], alpha=0.8)
plt.title('sAA Non-Responders: sAA Response to Slide Show', fontsize=14, weight='bold')
plt.ylabel('sAA Change (U/mL)\nSEM', fontsize=12)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.axhline(0, color='black', linewidth=0.8, linestyle='-')  # קו אופקי ב-0
plt.savefig("output_graph_nonresponders.png")  # שומר את הגרף של non-responders



# # 3. Plotting CPS cortisol levels
# plt.figure(figsize=(10, 6))
# plt.hist(localMain.responders_CPS_corisol_level_HC, bins=15, edgecolor='black', color='skyblue', alpha=0.7, label='Responders HC')
# plt.hist(localMain.responders_CPS_cortisol_level_NC, bins=15, edgecolor='black', color='lightgreen', alpha=0.7, label='Responders NC')
# plt.hist(localMain.nonresponders_CPS_cortisol_level_HC, bins=15, edgecolor='black', color='lightcoral', alpha=0.7, label='Non-Responders HC')
# plt.hist(localMain.nonresponders_CPS_cortisol_level_NC, bins=15, edgecolor='black', color='lightyellow', alpha=0.7, label='Non-Responders NC')
# plt.title('CPS Cortisol Levels in Responders and Non-Responders', fontsize=16)
# plt.xlabel('CPS Cortisol Level', fontsize=14)
# plt.ylabel('Frequency', fontsize=14)
# plt.legend()
# plt.grid(True)
# plt.show()

# # 5. Plotting positive image recall for both HC and NC women
# plt.figure(figsize=(10, 6))
# plt.hist(localMain.responders_positive_image_CPS_HC, bins=15, edgecolor='black', color='lightblue', alpha=0.7, label='Responders HC (CPS)')
# plt.hist(localMain.responders_positive_image_CPS_NC, bins=15, edgecolor='black', color='lightgreen', alpha=0.7, label='Responders NC (CPS)')
# plt.hist(localMain.responders_positive_image_control_HC, bins=15, edgecolor='black', color='lightcoral', alpha=0.7, label='Responders HC (Control)')
# plt.hist(localMain.responders_positive_image_control_NC, bins=15, edgecolor='black', color='lightyellow', alpha=0.7, label='Responders NC (Control)')
# plt.title('Positive Image Recall in Responders HC and NC Women', fontsize=16)
# plt.xlabel('Recall Value', fontsize=14)
# plt.ylabel('Frequency', fontsize=14)
# plt.legend()
# plt.grid(True)
# plt.show()

# # 6. Plotting negative image recall for both HC and NC women
# plt.figure(figsize=(10, 6))
# plt.hist(localMain.responders_negative_image_CPS_HC, bins=15, edgecolor='black', color='lightblue', alpha=0.7, label='Responders HC (CPS)')
# plt.hist(localMain.responders_negative_image_CPS_NC, bins=15, edgecolor='black', color='lightgreen', alpha=0.7, label='Responders NC (CPS)')
# plt.hist(localMain.responders_negative_image_control_HC, bins=15, edgecolor='black', color='lightcoral', alpha=0.7, label='Responders HC (Control)')
# plt.hist(localMain.responders_negative_image_control_NC, bins=15, edgecolor='black', color='lightyellow', alpha=0.7, label='Responders NC (Control)')
# plt.title('Negative Image Recall in Responders HC and NC Women', fontsize=16)
# plt.xlabel('Recall Value', fontsize=14)
# plt.ylabel('Frequency', fontsize=14)
# plt.legend()
# plt.grid(True)
# plt.show()